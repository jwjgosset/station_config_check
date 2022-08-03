from typing import List
import requests
from station_config_check.nagios import nagios_api
from station_config_check.nagios.nagios_api import NagiosHost


def get_fortimus_list(
    nagios_ip: str,
    api_key: str
) -> List[nagios_api.NagiosHost]:
    '''
    Get a list of all members of the Fortimus hostgroup from nagios

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
    fortimus_list = nagios_api.fetch_hostgroup_members(
        hostgroup_name='fortimus',
        nagios_ip=nagios_ip,
        api_key=api_key
    )

    host_list: List[nagios_api.NagiosHost] = []

    for fortimus in fortimus_list:
        nagioshost = nagios_api.fetch_host_information(
            host_name=fortimus,
            nagios_ip=nagios_ip,
            api_key=api_key
        )
        host_list.append(nagioshost)
    return host_list


def get_running_config(
    fortimus: NagiosHost
) -> str:
    url = f'http://{fortimus.ip_address}/config.txt'

    request = requests.get(url)

    return request.text
