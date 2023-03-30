from typing import Any, Dict, List

from video_verticalization.helpers import get_crop_sizes
from video_verticalization.video_metadata import VideoMetadata


class Verticalizer:
    def predict(self, input_video_path: str, video_features: List[List[Dict[str, Any]]]) -> List[int]:
        """
        Predict framewise vertical crop coordinates.

        :param input_video_path: path to the input video file
        :param video_features: framewise features
        :return: list of frame coordinates for each frame
        """
        video_metadata = VideoMetadata(input_video_path)

        crop_coordinates = []

        # Here is your code that calculates crop coordinates for each frame.
        # As the baseline we just place crop in the middle of each frame.
        for frame_index, frame_features in zip(range(video_metadata.total_frames), video_features):
            crop_width, crop_height = get_crop_sizes(video_metadata.frame_height)
            frame_crop_coordinate = int((video_metadata.frame_width / 2) - (crop_width / 2))
            crop_coordinates.append(frame_crop_coordinate)

        return crop_coordinates
