from typing import List
from dataclasses import dataclass
from station_config_check.titansma import digitizer_interface
from station_config_check.nagios import nagios_api
import pathlib


@dataclass
class TitanSMACredentials():
    username: str
    password: str


def get_titansma_list(
    nagios_ip: str,
    api_key: str
) -> List:
    titansma_list = nagios_api.fetch_hostgroup_members(
        hostgroup_name='titan-sma',
        nagios_ip=nagios_ip,
        api_key=api_key
    )
    return titansma_list


def get_running_config(
    host_name: str,
    nagios_ip: str,
    api_key: str
):
    titansma_ip = nagios_api.fetch_host_ip(
        host_name=host_name,
        nagios_ip=nagios_ip,
        api_key=api_key
    )

    credentials = fetch_credentials(host_name)

    cookieJar = digitizer_interface.GlobalCookieJar().addCookieToAllRequests()

    digitizerInterface = digitizer_interface.DigitizerInterface(
        address=titansma_ip,
        username=credentials.username,
        password=credentials.password)

    digitizerInterface.login(cookieJar)

    config = digitizerInterface.getConfiguration()

    # To be continued
    return config


def load_golden_image(
    goldenimg_dir: str,
    host_name: str
) -> List[str]:
    network, station = host_name.split('-')[:2]

    goldenimg_path = pathlib.Path(
        f"{goldenimg_dir}/{network}/{station}/titansma/latest.ttl")

    with open(goldenimg_path, mode='r') as f:
        golden_img = f.read().splitlines()

    return golden_img


def fetch_credentials(
    host_name: str
) -> TitanSMACredentials:
    return TitanSMACredentials('', '')
