import logging
import pathlib
from os import makedirs


class GoldenImageMissing(Exception):
    pass


def load_golden_image(
    goldenimg_dir: str,
    host_name: str
) -> str:
    '''
    Load the golden image of a digitizer

    Parameters
    ----------
    goldenimg_dir: str
        The parent directory where golden images for station devices are
        located

    host_name: str
        The Nagios hostname for the digitizer

    Returns
    -------
    str:
        The contents of the golden image config file as a single string
    '''
    network, station = host_name.split('-')[:2]

    goldenimg_path = pathlib.Path(
        f"{goldenimg_dir}/{network}/{station}/titansma/latest.ttl")

    if not goldenimg_path.exists():
        raise GoldenImageMissing()

    with open(goldenimg_path, mode='r') as f:
        golden_img = f.read()

    return golden_img


def write_golden_image(
    goldenimg_dir: str,
    host_name: str,
    config: str
):
    '''
    Write or overwrite the golden image config for a TitanSMA

    Parameters
    ----------
    goldenimg_dir: str
        The parent directory where golden images are stored

    host_name: str
        The nagios hostname for the TitanSMA to write a golden image for

    config: str
        The configuration as a single string
    '''
    network, station = host_name.split('-')[:2]

    subdir = pathlib.Path(
        f"{goldenimg_dir}/{network}/{station}/titansma")

    if not subdir.exists():
        logging.debug(f'Creating directory {subdir}')
        makedirs(str(subdir))

    goldenimg_path = pathlib.Path(
        f"{goldenimg_dir}/{network}/{station}/titansma/latest.ttl")

    with open(goldenimg_path, mode='w') as f:
        f.writelines(config)
