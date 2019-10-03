"""
Tool for 'leave-one-out' testing features in dataset.
Adds use_column parameter for lightgbm CLI, which works
like an opposite one to ignore_columns.

Example usage
--------------
>>> python lgbm_tool.py --use_column=column1,column2,column3 \
>>>                     config=path_to_config data=path_to_data valid=path_to_valid
"""
import argparse
import subprocess
from typing import List, TextIO


def _get_all_features(data_file: TextIO) -> List[str]:
    features = data_file.readline().strip().split(',')
    return features


def _generate_ignore_string(features: List[str],
                            features_left: List[str]) -> str:

    for feature in features_left:
        features.remove(feature)

    ignore_string = 'name:' + ','.join([f"{feature}" for feature in features])

    return ignore_string


def _parse_lgbm_config(config_file: str) -> dict:
    config = {}
    f = open(config_file, 'r')
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            continue
        parameter_name, parameter_value = line.split('=')
        config[parameter_name] = parameter_value
    f.close()
    return config


def _get_label_column(lightgbm_cli_args: dict):
    """Checks whether label column is either in CLI arguments or lgbm config
    file and gets it. If not, raises an exception.
    """

    if 'label_column' in lightgbm_cli_args:
        label_column = lightgbm_cli_args['label_column'].replace('name:', '')
        return label_column

    config = lightgbm_cli_args.get('config')
    if not config:
        raise ValueError('No label column provided')

    lightgbm_config_args = _parse_lgbm_config(config)
    if 'label_column' not in lightgbm_config_args:
        raise ValueError('No label column provided')

    label_column = lightgbm_config_args['label_column'].replace('name:', '')
    return label_column


def run_lgbm(args: dict) -> None:
    """Asynchronously runs lightgbm"""

    lightgbm_args = {
        key: value for key, value in
        map(lambda x: x.split('='), args['lightgbm_args'])
    }
    label_column = _get_label_column(lightgbm_args)

    with open(lightgbm_args['data'], 'r') as f:
        features = _get_all_features(f)

    use_columns = args['use_column'].split(',')
    use_columns.append(label_column)

    ignore_string = _generate_ignore_string(features, use_columns)

    subprocess.call(
        [
            'lightgbm',
            f'ignore_column={ignore_string}',
            *args['lightgbm_args']
        ],
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--use_column', type=str, required=False,
        help='Features to use for training'
    )
    parser.add_argument(
        'lightgbm_args', nargs='+',
        help='Any arguments for lightgbm cli'
    )

    args = parser.parse_args()
    run_lgbm(vars(args))


if __name__ == '__main__':
    main()
