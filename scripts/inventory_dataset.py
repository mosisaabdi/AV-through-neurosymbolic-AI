"""Create a safe inventory and small schema samples for a dataset directory."""
import argparse, csv, json
from pathlib import Path

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
VIDEO_EXT = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
ANN_EXT = {".json", ".jsonl", ".csv", ".txt"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--sample-lines", type=int, default=3)
    a = p.parse_args(); root = Path(a.root)
    if not root.exists(): raise SystemExit(f"Dataset root does not exist: {root}")
    files=[]
    for path in sorted(root.rglob("*")):
        if not path.is_file(): continue
        item={"relative_path":str(path.relative_to(root)),"suffix":path.suffix.lower(),"size_bytes":path.stat().st_size}
        if path.suffix.lower() in IMAGE_EXT:
            try:
                from PIL import Image
                with Image.open(path) as im: item["image"]={"width":im.width,"height":im.height,"mode":im.mode}
            except Exception as e: item["image_inspection_error"]=str(e)
        if path.suffix.lower() in VIDEO_EXT:
            try:
                import cv2
                cap=cv2.VideoCapture(str(path)); item["video"]={"fps":cap.get(cv2.CAP_PROP_FPS),"frame_count":int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),"width":int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),"height":int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}; cap.release()
            except Exception as e: item["video_inspection_note"]="Install opencv-python to inspect video metadata: "+str(e)
        if path.suffix.lower() in ANN_EXT and path.stat().st_size < 50_000_000:
            try:
                if path.suffix.lower()==".jsonl":
                    with path.open(encoding="utf-8-sig") as f: item["sample_records"]=[json.loads(line) for line in f if line.strip()][:a.sample_lines]
                elif path.suffix.lower()==".json":
                    obj=json.loads(path.read_text(encoding="utf-8-sig")); item["json_top_level_type"]=type(obj).__name__; item["sample"]=(obj[:a.sample_lines] if isinstance(obj,list) else {k:obj[k] for k in list(obj)[:a.sample_lines]} if isinstance(obj,dict) else obj)
                elif path.suffix.lower()==".csv":
                    with path.open(newline="",encoding="utf-8-sig") as f: item["csv_headers"]=next(csv.reader(f),[])
            except Exception as e: item["annotation_inspection_error"]=str(e)
        files.append(item)
    counts={}
    for f in files: counts[f["suffix"]]=counts.get(f["suffix"],0)+1
    report={"root":str(root.resolve()),"file_count":len(files),"extension_counts":counts,"files":files,"warning":"Schema samples are for inspection only; no labels were inferred or modified."}
    out=Path(a.out); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Inventoried {len(files)} files; extension counts={counts}; report={out}")
if __name__=="__main__": main()
