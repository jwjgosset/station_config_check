from typing import Dict, List
from station_config_check.titansma.models import CONFIG_VALUES, NP_CONFIG, \
    TITANSMA_CONFIG, WEBSOCKET_CONFIG, TSMAStreamerConfig, TitanSMAConfig


def parse_titan_config(
    running_config: str
) -> TitanSMAConfig:
    '''
    Parse a TitanSMA config file and convert the relevent parameters into
    human readable format

    Parameters
    ----------
    running_config: str
    A dump of the entire config file in string format

    Returns
    -------
    TitanSMAConfig
        An object containing the relevent configuration parameters and their
        values
    '''
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
            streamer_config['NP Streamer'] = str(n)
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
            ws_streamer_config['Websocker NP Streamer'] = str(n)
            for index in WEBSOCKET_CONFIG:
                ws_streamer_config[index] = get_value(
                    config_value=config_dict[index.format(i=n)])
            streamers.append(TSMAStreamerConfig(streamer_config))

    # Assemble TitanSMAConfig object
    return TitanSMAConfig(
        device_config=titan_config,
        streamer_config=streamers)


def get_value(
    config_value: str
) -> str:
    '''
    Convert a configuration value from a TitanSMA config file to human
    readable format

    Parameters
    ----------
    config_value: str
        The value as it appears in the config file

    Returns
    -------
    str
        The human readable format
    '''
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
