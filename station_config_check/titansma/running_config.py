import logging
from typing import List
from dataclasses import dataclass
from station_config_check.titansma import digitizer_interface
from station_config_check.nagios import nagios_api
import configparser


class CredFileError(Exception):
    pass


@dataclass
class TitanSMACred():
    username: str
    password: str


def get_titansma_list(
    nagios_ip: str,
    api_key: str
) -> List[nagios_api.NagiosHost]:
    '''
    Get a list of all members of the TitanSMA hostgroup from nagios

    Parameters
    ----------
    nagios_ip: str
        The ip address of the nagios server

    api_key: str
        The api key used to retrieve the information from Nagios

    Returns
    -------
    List: A list of NagiosHost objects containing hostnames, ip addresses, etc
    '''
    titansma_list = nagios_api.fetch_hostgroup_members(
        hostgroup_name='titan-sma',
        nagios_ip=nagios_ip,
        api_key=api_key
    )

    host_list: List[nagios_api.NagiosHost] = []

    for titansma in titansma_list:
        nagioshost = nagios_api.fetch_host_information(
            host_name=titansma,
            nagios_ip=nagios_ip,
            api_key=api_key
        )
        host_list.append(nagioshost)
    return host_list


def get_running_config(
    titan_sma: nagios_api.NagiosHost,
    credentials: TitanSMACred
) -> str:
    '''
    Download the running config from a TitanSMA

    Parameters
    ----------
    titan_sma: NagiosHost
        NagiosHost object containing hostname ip address, etc

    cred_file: str
        The path to the cred_file

    Returns
    -------

    str: The running config of the TitanSMA as a single string
    '''
    cookieJar = digitizer_interface.GlobalCookieJar()
    cookieJar = cookieJar.addCookieToAllRequests()

    digitizerInterface = digitizer_interface.DigitizerInterface(
        address=titan_sma.ip_address,
        username=credentials.username,
        password=credentials.password)

    logging.debug(f"Trying to log into {titan_sma.hostname}")
    response = digitizerInterface.login(cookieJar)

    logging.debug(response.read().decode())

    logging.debug(f'Trying to download config for {titan_sma.hostname}')
    config = digitizerInterface.getConfiguration()

    return config


def fetch_credentials(
    install_type: str,
    config: configparser.ConfigParser
) -> TitanSMACred:
    '''
    Fetch the login credentials for a specified install type

    Parameters
    ----------
    install_type: str
        The install type for the host as it appears in the cred_filessh

    cred_file: str
        The path to the cred_file

    Returns
    -------
    TitanSMACred: The credentials extracted from the cred_file
    '''
    username = config['TitanSMA']['username']

    password = config['TitanSMA'][install_type]

    return TitanSMACred(
        username=username, password=password)
