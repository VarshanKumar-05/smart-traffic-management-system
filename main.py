import cv2
import time
import config

from detector import VehicleDetector
from tracker import VehicleTracker
from lane_manager import LaneManager
from signal_controller import SignalController
from emergency_handler import EmergencyHandler
from logger import TrafficLogger


def main():

    print("Starting Smart Traffic AI System...")

    # Initialize Modules
    detector = VehicleDetector()
    tracker = VehicleTracker()
    lane_manager = LaneManager()
    signal_controller = SignalController()
    emergency_handler = EmergencyHandler()
    logger = TrafficLogger()

    cap = cv2.VideoCapture(config.VIDEO_PATH)   

    if not cap.isOpened():
        print("Error opening video file")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        config.OUTPUT_PATH,
        fourcc,
        20.0,
        (config.FRAME_WIDTH, config.FRAME_HEIGHT)
    )

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))

        # -----------------------------
        # Detection
        # -----------------------------
        detections = detector.detect(frame)

        # -----------------------------
        # Tracking
        # -----------------------------
        tracks = tracker.update(detections, frame)

        # -----------------------------
        # Lane Counting
        # -----------------------------
        lane_counts = lane_manager.count_vehicles_per_lane(
            tracks,
            config.FRAME_WIDTH
        )

        total_vehicles = sum(lane_counts)

        # -----------------------------
        # Emergency Check
        # -----------------------------
        emergency = emergency_handler.check_emergency(
            detections,
            detector.model.names
        )

        # -----------------------------
        # Signal Logic
        # -----------------------------
        green_times = signal_controller.calculate_lane_times(lane_counts)
        priority_lane = signal_controller.get_priority_lane(lane_counts)

        if emergency:
            priority_lane = 0
            green_times = [config.MAX_GREEN_TIME] * config.LANE_SPLITS

        # -----------------------------
        # Logging
        # -----------------------------
        logger.log(
            lane_counts,
            total_vehicles,
            priority_lane,
            green_times
        )

        # -----------------------------
        # Draw Tracking Boxes
        # -----------------------------
        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = map(int, track.to_ltrb())

            cv2.rectangle(frame, (l, t), (r, b), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"ID {track_id}",
                (l, t - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # -----------------------------
        # FPS
        # -----------------------------
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time

        # -----------------------------
        # Dashboard Panel
        # -----------------------------
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (450, 200), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

        cv2.putText(frame, "SMART TRAFFIC AI SYSTEM",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2)

        cv2.putText(frame, f"Lane Counts: {lane_counts}",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2)

        cv2.putText(frame, f"Total Vehicles: {total_vehicles}",
                    (20, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2)

        cv2.putText(frame, f"Priority Lane: {priority_lane}",
                    (20, 130),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2)

        cv2.putText(frame, f"Green Times: {green_times}",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2)

        cv2.putText(frame, f"FPS: {int(fps)}",
                    (config.FRAME_WIDTH - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2)

        if emergency:
            cv2.putText(frame, "EMERGENCY MODE ACTIVATED",
                        (config.FRAME_WIDTH // 3, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (0, 0, 255),
                        3)

        # Draw lane divider
        lane_width = config.FRAME_WIDTH // config.LANE_SPLITS
        for i in range(1, config.LANE_SPLITS):
            cv2.line(frame,
                     (i * lane_width, 0),
                     (i * lane_width, config.FRAME_HEIGHT),
                     (255, 255, 255),
                     1)

        out.write(frame)
        cv2.imshow("Smart Traffic AI", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print("Processing Complete. Output saved.")


if __name__ == "__main__":
    main()