"""Extract frames at fixed time intervals for qualitative inspection only."""
import argparse, csv
from pathlib import Path

def main():
    p=argparse.ArgumentParser(); p.add_argument('--input',required=True); p.add_argument('--out',required=True); p.add_argument('--every-seconds',type=float,default=1.0); p.add_argument('--max-frames',type=int,default=0); a=p.parse_args()
    if a.every_seconds<=0: raise SystemExit('--every-seconds must be positive')
    try: import cv2
    except ImportError: raise SystemExit('Install opencv-python to extract video frames')
    src=Path(a.input)
    if not src.exists(): raise SystemExit(f'Video not found: {src}')
    out=Path(a.out); out.mkdir(parents=True,exist_ok=True); cap=cv2.VideoCapture(str(src))
    if not cap.isOpened(): raise SystemExit(f'Could not open video: {src}')
    fps=cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps<=0: cap.release(); raise SystemExit('Video FPS unavailable; cannot sample by seconds safely')
    stride=max(1,round(fps*a.every_seconds)); rows=[]; frame_idx=0; saved=0
    while True:
        ok,frame=cap.read()
        if not ok: break
        if frame_idx % stride==0:
            name=f'frame_{frame_idx:08d}.jpg'; path=out/name
            if not cv2.imwrite(str(path),frame): raise SystemExit(f'Failed to write {path}')
            rows.append((name,frame_idx,frame_idx/fps)); saved+=1
            if a.max_frames and saved>=a.max_frames: break
        frame_idx+=1
    cap.release()
    with (out/'manifest.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['filename','source_frame_index','timestamp_seconds']); w.writerows(rows)
    print(f'Saved {saved} frames to {out}. These are unlabeled samples, not evaluation ground truth.')
if __name__=='__main__': main()
