import logging
import click

from station_config_check.config import LogLevels
from station_config_check.titansma.parse_config import parse_titan_config
from station_config_check.titansma.running_config import enter_credentials, \
    get_running_config


@click.command()
@click.option(
    '-i',
    '--titansma-ip',
    type=str,
    help=('The IP address of the TitanSMA to retrieve config from')
)
@click.option(
    '-l',
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help="Log more information about the program's execution",
    default=LogLevels.WARNING
)
@click.option(
    '-c',
    '--config-output',
    type=str,
    help=("Specify location to store raw titansma config file. If none, " +
          "config file is not stored"),
    default=None
)
@click.option(
    '-o',
    '--output-file',
    type=str,
    help=("Specify a file to store human-readable output in. If none is" +
          " specified, configuration is output to screen"),
    default=None
)
def main(
    titansma_ip: str,
    log_level: str,
    config_output: str,
    output_file: str
):
    # Set logging config
    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_level)

    # Get credentials from user
    credentials = enter_credentials()

    # Download config file
    running_config = get_running_config(
        ip_address=titansma_ip,
        credentials=credentials
    )

    # Translate config file
    parsed_config = parse_titan_config(
        running_config=running_config
    )

    # Write config file to disk if path specified
    if config_output is not None:
        with open(config_output, mode='w') as f:
            f.write(running_config)

    # Either print parsed output to stdout or file
    if output_file is not None:
        with open(output_file, mode='w') as f:
            f.write(str(parsed_config))

    else:
        print(str(parsed_config))

    return


if __name__ == '__main__':
    main()
