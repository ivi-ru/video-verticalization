from typing import Tuple, List

import logging
import subprocess
import sys

from video_verticalization.video_metadata import VideoMetadata


def get_logger(level: int = logging.INFO) -> logging.Logger:
    """
    Create logger.

    :param level: logger level
    :return: logger object
    """
    logger_object = logging.getLogger()
    logger_object.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(filename)-25.25s:%(lineno)-4d | %(message)s'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    if logger_object.hasHandlers():
        logger_object.handlers.clear()

    logger_object.addHandler(handler)
    return logger_object


def get_crop_sizes(original_height: int) -> Tuple[int, int]:
    """
    Calculate vertical crop sizes from original height.

    :param original_height: Height of the original video
    :return: width and height of the crop
    """
    return int((original_height / 16.) * 9.), original_height


def save_crop(
        source_video_file_path: str,
        cropped_video_file_path: str,
        crop_coordinates: List[int]
) -> None:
    """
    Crop video source_video_file_path and save it to cropped_video_file_path.

    :param source_video_file_path: source video path
    :param cropped_video_file_path: cropped video path
    :param crop_coordinates: distances from the left side of the frame to left side of the crop
    """
    video_metadata = VideoMetadata(source_video_file_path)
    crop_width, crop_height = get_crop_sizes(video_metadata.frame_height)

    crop_x_str = ''
    for i, x in enumerate(crop_coordinates):
        crop_x_str += f'eq(n,{i})*{x}+'
    crop_x_str = crop_x_str[:-1]
    cmd = [
        'ffmpeg',
        '-i', source_video_file_path,
        '-filter:v',
        f"crop=w={crop_width}:h={crop_height}:x='{crop_x_str}':y=0",
        cropped_video_file_path
    ]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        out, err = process.communicate()
        return_code = process.poll()
        if return_code != 0:
            raise Exception('ffmpeg', out, err)


def absolute_coordinates_to_relative(
        video_file_path: str,
        coordinates: List[int]
) -> List[float]:
    """
    Convert absolute coodrinates in pixels to relative coordinates.

    :param video_file_path: path to video file
    :param coordinates: source absolute coordinates in pixels
    :return: relative coordinates in range [0 .. 1]
    """
    video_metadata = VideoMetadata(video_file_path)
    return [x / video_metadata.frame_width for x in coordinates]


logger = get_logger()
