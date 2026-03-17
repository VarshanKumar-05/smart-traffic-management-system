import config


class LaneManager:
    def __init__(self):
        self.num_lanes = config.LANE_SPLITS

    def get_lane(self, x_center, frame_width):
        """
        Determine which lane the vehicle belongs to
        """
        lane_width = frame_width // self.num_lanes
        lane_index = int(x_center // lane_width)
        return min(lane_index, self.num_lanes - 1)

    def count_vehicles_per_lane(self, tracks, frame_width):
        """
        Count tracked vehicles per lane
        """
        lane_counts = [0] * self.num_lanes

        for track in tracks:
            if not track.is_confirmed():
                continue

            bbox = track.to_ltrb()
            x1, y1, x2, y2 = bbox

            x_center = (x1 + x2) / 2

            lane_id = self.get_lane(x_center, frame_width)
            lane_counts[lane_id] += 1

        return lane_counts