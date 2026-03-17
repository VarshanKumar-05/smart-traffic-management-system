import config


class EmergencyHandler:
    def __init__(self):
        self.emergency_classes = config.EMERGENCY_CLASSES

    def check_emergency(self, detections, model_names):
        """
        Check if emergency vehicle is present
        """
        for box in detections.boxes:
            cls = int(box.cls[0])
            class_name = model_names[cls]

            # Normalize name for safety
            class_name = class_name.lower()

            if class_name in self.emergency_classes:
                return True

        return False