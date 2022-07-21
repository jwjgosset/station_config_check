from typing import List
from dataclasses import dataclass
from station_config_check.titansma import digitizer_interface
from station_config_check.nagios import nagios_api
import pathlib
import configparser


class CredFileError(Exception):
    pass


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
    api_key: str,
    cred_file: str
):
    titansma_ip = nagios_api.fetch_host_ip(
        host_name=host_name,
        nagios_ip=nagios_ip,
        api_key=api_key
    )

    credentials = fetch_credentials(host_name, cred_file)

    cookieJar = digitizer_interface.GlobalCookieJar().addCookieToAllRequests()

    digitizerInterface = digitizer_interface.DigitizerInterface(
        address=titansma_ip,
        username=credentials.username,
        password=credentials.password)

    digitizerInterface.login(cookieJar)

    config = digitizerInterface.getConfiguration()

    # To be continued
    return config


def fetch_credentials(
    install_type: str,
    cred_file: str
) -> TitanSMACredentials:

    cred_path = pathlib.Path(cred_file)

    if not cred_path.exists():
        raise CredFileError('Could not read specified file')

    config = configparser.ConfigParser()

    config.read(cred_path)

    username = config['TitanSMA']['username']

    password = config['TitanSMA'][install_type]

    return TitanSMACredentials(
        username=username, password=password)
