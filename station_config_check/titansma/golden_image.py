import pathlib
from typing import List


class GoldenImageMissing(Exception):
    pass


def load_golden_image(
    goldenimg_dir: str,
    host_name: str
) -> List[str]:
    network, station = host_name.split('-')[:2]

    goldenimg_path = pathlib.Path(
        f"{goldenimg_dir}/{network}/{station}/titansma/latest.ttl")

    if not goldenimg_path.exists():
        raise GoldenImageMissing()

    with open(goldenimg_path, mode='r') as f:
        golden_img = f.read().splitlines()

    return golden_img
