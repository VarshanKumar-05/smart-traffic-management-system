from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np


class VehicleTracker:
    def __init__(self):
        print("Initializing DeepSORT tracker...")
        self.tracker = DeepSort(max_age=30)
        print("Tracker ready.")

    def update(self, detections, frame):
        """
        Update tracker with YOLO detections
        Returns tracked objects
        """
        tracks_input = []

        for box in detections.boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0].item()
            cls = int(box.cls[0])

            width = x2 - x1
            height = y2 - y1

            tracks_input.append((
                [x1.item(), y1.item(), width.item(), height.item()],
                conf,
                cls
            ))

        tracks = self.tracker.update_tracks(tracks_input, frame=frame)

        return tracks