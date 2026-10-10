from dataclasses import dataclass
from typing import Any

@dataclass
class PerceptionOutput:
    detections: list[dict[str, Any]]
    lane_output: Any = None
    drivable_area_output: Any = None
    feature_tensors: Any = None

class YOLOPAdapter:
    """Adapter contract. Implement using the exact YOLOP fork and checkpoint."""
    def __init__(self, repository_path: str, checkpoint_path: str, device: str = "cuda"):
        self.repository_path = repository_path
        self.checkpoint_path = checkpoint_path
        self.device = device
        # TODO: import the exact YOLOP code, load config/checkpoint, eval mode.
        # Record upstream commit and checkpoint SHA256 in the experiment manifest.

    def predict(self, rgb_image) -> PerceptionOutput:
        raise NotImplementedError(
            "Connect the actual YOLOP implementation/checkpoint. Do not fabricate outputs."
        )
