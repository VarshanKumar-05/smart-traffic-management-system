import csv
import os
import time
import config


class TrafficLogger:
    def __init__(self):
        self.log_file = config.LOG_FILE
        self.initialize_file()

    def initialize_file(self):
        """
        Create CSV file with headers if not exists
        """
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Timestamp",
                    "Lane_Counts",
                    "Total_Vehicles",
                    "Priority_Lane",
                    "Green_Times"
                ])

    def log(self, lane_counts, total, priority_lane, green_times):
        """
        Log traffic data into CSV
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                lane_counts,
                total,
                priority_lane,
                green_times
            ])