from getpass import getpass
import logging
from typing import List
from dataclasses import dataclass
from station_config_check.config_check import web_interface
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
            api_key=api_key,
            get_type=True
        )
        host_list.append(nagioshost)
    return host_list


def get_running_config(
    ip_address: str,
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
    cookieJar = web_interface.GlobalCookieJar()
    cookieJar = cookieJar.addCookieToAllRequests()

    digitizerInterface = web_interface.DigitizerInterface(
        address=ip_address,
        username=credentials.username,
        password=credentials.password)

    logging.debug(f"Trying to log into {ip_address}")
    digitizerInterface.login(cookieJar)

    logging.debug(f'Trying to download config for {ip_address}')
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
        username=username,
        password=password)


def enter_credentials() -> TitanSMACred:
    '''
    Prompts the user for the login credentials for a TitanSMA

    Returns
    -------
    TitanSMACred: The credentials entered by the user
    '''
    username = input('Enter the TitanSMA Username: ')
    # Use getpass to avoid password peeking
    password = getpass('Enter the TitanSMA Password: ')
    return TitanSMACred(
        username=username,
        password=password)
