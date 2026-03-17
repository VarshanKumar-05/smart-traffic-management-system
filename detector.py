from ultralytics import YOLO
import config


class VehicleDetector:
    def __init__(self):
        print("Loading YOLO model...")
        self.model = YOLO(config.MODEL_PATH)
        print("Model loaded successfully.")

    def detect(self, frame):
        """
        Runs YOLO detection on a frame
        Returns detection results
        """
        results = self.model(frame, conf=config.CONFIDENCE_THRESHOLD)[0]
        return results