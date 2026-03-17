# -------------------------------
# SMART TRAFFIC AI CONFIGURATION
# -------------------------------

# Video Settings
VIDEO_PATH = "videos/mm.mp4"
OUTPUT_PATH = "output/output.mp4"

# Model Settings
MODEL_PATH = "yolov8m.pt"
CONFIDENCE_THRESHOLD = 0.4

# Frame Settings
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Signal Timing Settings
BASE_GREEN_TIME = 20
WEIGHT_PER_VEHICLE = 2
MAX_GREEN_TIME = 60
MIN_GREEN_TIME = 15

# Lane Settings (Vertical Split Example)
LANE_SPLITS = 2   # Number of lanes (2 = left & right)

# Logging
LOG_FILE = "data/traffic_log.csv"

# Heatmap Settings
ENABLE_HEATMAP = True

# Emergency Vehicle Classes
EMERGENCY_CLASSES = ["ambulance", "fire truck"]