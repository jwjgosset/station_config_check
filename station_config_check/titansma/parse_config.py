from typing import Dict, List
from dataclasses import dataclass

from station_config_check.titansma.models import CONFIG_VALUES, NP_CONFIG, \
    TITANSMA_CONFIG, WEBSOCKET_CONFIG


@dataclass
class TitanSMAConfig:
    device_config: Dict
    streamer_config: List


@dataclass
class TSMAStreamerConfig(Dict):
    self: Dict


def parse_titan_config(
    running_config: str
):
    # Break the config file string into lines
    config_lines = running_config.splitlines()

    config_dict: Dict = {}

    # Extract only the identifier and value of each line and put them into a
    # list of tuples
    for line in config_lines:
        line_parts = line.split(' ')
        config_dict[line_parts[0]] = line_parts[2].rstrip('.')

    titan_config: Dict = {}

    for index in TITANSMA_CONFIG:
        if index in config_dict:
            titan_config[index] = get_value(config_dict[index])

    streamers: List[TSMAStreamerConfig] = []

    # Loop through possible np streamers
    for n in range(1, 5, 1):
        # Check if the _exists value of a potential streamer is true
        if config_dict["<streamingDataLibrary/table/_exists#_{i}>".format(
                i=n)] == '"true"^^xsd:boolean.':
            streamer_config: Dict = {}
            for index in NP_CONFIG:
                streamer_config[index] = get_value(
                    config_value=config_dict[index.format(i=n)])
            streamers.append(TSMAStreamerConfig(streamer_config))

    # Loop through possible websocket np streamers
    ws_exists = "<streamingDataLibrary/table/filtered/websocket/_exists#_{i}>"
    for n in range(1, 9, 1):
        # Check if the _exists value of a potential streamer is true
        if config_dict[ws_exists.format(
                i=n)] == '"true"^^xsd:boolean.':
            ws_streamer_config: Dict = {}
            for index in WEBSOCKET_CONFIG:
                ws_streamer_config[index] = get_value(
                    config_value=config_dict[index.format(i=n)])
            streamers.append(TSMAStreamerConfig(streamer_config))


def get_value(
    config_value: str
):
    value: str = ''

    # Translate special values
    if config_value in CONFIG_VALUES:
        value = CONFIG_VALUES[config_value]
    # Extract value from variable types
    elif '^^xsd:' in config_value:
        split_value = config_value.split('^^xsd:')
        value = (split_value[0]).strip('"')
    # Strip trailing period and quotes off of string values
    else:
        value = config_value.strip('."')

    return value
