import config


class SignalController:
    def __init__(self):
        self.base_time = config.BASE_GREEN_TIME
        self.weight = config.WEIGHT_PER_VEHICLE
        self.max_time = config.MAX_GREEN_TIME
        self.min_time = config.MIN_GREEN_TIME

    def calculate_lane_times(self, lane_counts):
        """
        Calculate green signal time for each lane
        """
        lane_times = []

        for count in lane_counts:
            green_time = self.base_time + (count * self.weight)

            if green_time > self.max_time:
                green_time = self.max_time

            if green_time < self.min_time:
                green_time = self.min_time

            lane_times.append(green_time)

        return lane_times

    def get_priority_lane(self, lane_counts):
        """
        Select lane with highest traffic
        """
        if not lane_counts:
            return 0

        return lane_counts.index(max(lane_counts))