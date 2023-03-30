from typing import List

import argparse
import json
import os
import sys
import time

from video_verticalization.helpers import logger, save_crop
from video_verticalization.model import Verticalizer


def parse_args(sys_args: List[str]) -> argparse.Namespace:  # pylint: disable=R0912,R0915
    """
    Parse command line args.

    :param sys_args: command line args.
    :return: argparse result.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_video_path',
        dest='input_video_path',
        type=str,
        required=True,
        help='Path to input video.'
    )
    parser.add_argument(
        '--input_features_path',
        dest='input_features_path',
        type=str,
        required=True,
        help='Path to json file with features.'
    )
    parser.add_argument(
        '--output_dir_path',
        dest='output_dir_path',
        type=str,
        required=True,
        help='Path to the result folder.'
    )
    parser.add_argument(
        '--visualize',
        dest='visualize',
        action='store_true',
        help='If set, save cropped video along with crop coordinates.'
    )

    return parser.parse_args(sys_args)


def verticalize() -> None:
    """Find vertical crops for each frame of the video."""
    start_time = time.time()
    args = parse_args(sys.argv[1:])

    with open(args.input_features_path, 'r') as fp:
        video_features = json.load(fp)

    verticalizer = Verticalizer()
    crop_coordinates = verticalizer.predict(args.input_video_path, video_features)

    os.makedirs(args.output_dir_path, exist_ok=True)
    crop_coordinates_path = os.path.join(args.output_dir_path, 'crops.json')
    with open(crop_coordinates_path, 'w') as fp:
        json.dump(crop_coordinates, fp)

    if args.visualize:
        cropped_video_path = os.path.join(args.output_dir_path, 'cropped_video.mp4')
        save_crop(args.input_video_path, cropped_video_path, crop_coordinates)

    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
    logger.info('Ready. Total time: %s', elapsed_time_str)


if __name__ == '__main__':
    verticalize()
