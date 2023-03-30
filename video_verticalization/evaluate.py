from typing import List, Tuple

import argparse
import json
import os
import sys

import numpy as np
from sklearn.metrics import mean_squared_error
from tqdm import tqdm

from video_verticalization.model import Verticalizer
from video_verticalization.helpers import save_crop, absolute_coordinates_to_relative


def parse_args(sys_args: List[str]) -> argparse.Namespace:  # pylint: disable=R0912,R0915
    """
    Parse command line args.

    :param sys_args: command line args.
    :return: argparse result.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--validation_set',
        dest='validation_set_dir',
        type=str,
        required=True,
        help='Path to input video.'
    )
    parser.add_argument(
        '--videos',
        dest='videos_dir',
        type=str,
        required=True,
        help='Path to json file with features.'
    )
    parser.add_argument(
        '--results_dir',
        dest='results_dir',
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


def create_output_dirs(results_dir: str, visualize: bool) -> Tuple[str, str, str]:
    """
    Create output dirs.

    :param results_dir: root output dir path
    :param visualize: if True, create dirs for video crops saving
    :return: path to the three output subdirs
    """
    predicted_crops_dir = os.path.join(results_dir, 'pred_crops')
    
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(predicted_crops_dir, exist_ok=True)

    true_video_crops_dir = os.path.join(results_dir, 'true_crop_videos')
    predicted_video_crops_dir = os.path.join(results_dir, 'pred_crop_videos')

    if visualize:   
        os.makedirs(true_video_crops_dir, exist_ok=True)
        os.makedirs(predicted_video_crops_dir, exist_ok=True)

    return predicted_crops_dir, true_video_crops_dir, predicted_video_crops_dir


def evaluate() -> None:
    """Predict crops for validation set and calculate metrics."""
    args = parse_args(sys.argv[1:])
    validation_set_dir=args.validation_set_dir
    source_videos_dir=args.videos_dir
    results_dir=args.results_dir
    visualize=args.visualize

    (
        predicted_crops_dir,
        true_video_crops_dir,
        predicted_video_crops_dir
    ) = create_output_dirs(results_dir, visualize)
    
    metrics_path = os.path.join(results_dir, 'metrics.json')

    features_files = os.listdir(validation_set_dir)

    verticalizer = Verticalizer()

    mses_abs = []
    mses_rel = []
    for features_file in tqdm(features_files):
        video_file_name = features_file[:-len('.json')] + '.mp4'
        features_file_path = os.path.join(validation_set_dir, features_file)
        video_file_path = os.path.join(source_videos_dir, video_file_name)
        
        with open(features_file_path, 'r') as fp:
            features_with_labels = json.load(fp)

        features = [frame['faces'] for frame in features_with_labels]
        true_crop_coordinates = [frame['x_crop'] for frame in features_with_labels]

        predicted_crop_coordinates = verticalizer.predict(
            input_video_path=video_file_path,
            video_features=features
        )

        true_crop_coordinates_relative = absolute_coordinates_to_relative(
            video_file_path,
            true_crop_coordinates
        )
        predicted_crop_coordinates_relative = absolute_coordinates_to_relative(
            video_file_path,
            predicted_crop_coordinates
        )

        predicted_crops_file_path = os.path.join(predicted_crops_dir, features_file)
        with open(predicted_crops_file_path, 'w') as fp:
            json.dump(predicted_crop_coordinates, fp)

        mses_abs.append(
            mean_squared_error(true_crop_coordinates, predicted_crop_coordinates)
        )

        mses_rel.append(
            mean_squared_error(true_crop_coordinates_relative, predicted_crop_coordinates_relative)
        )

        if visualize:
            true_cropped_video_path = os.path.join(true_video_crops_dir, video_file_name)
            predicted_cropped_video_path = os.path.join(predicted_video_crops_dir, video_file_name)

            save_crop(video_file_path, true_cropped_video_path, true_crop_coordinates)
            save_crop(video_file_path, predicted_cropped_video_path, predicted_crop_coordinates)

    mean_mse_abs = np.mean(mses_abs)
    mean_mses_rel = np.mean(mses_rel)
    with open(metrics_path, 'w') as fp:
        json.dump(
            {
                'mse_absolute': mean_mse_abs,
                'mse_relative': mean_mses_rel
            }, 
            fp
        )


if __name__ == '__main__':
    evaluate()
