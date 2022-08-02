import logging
import urllib
import click
import configparser
from station_config_check.config import LogLevels
from station_config_check.nagios.models import NagiosOutputCode
from station_config_check.nagios.nrdp import NagiosCheckResult, \
    NagiosCheckResults, submit
from station_config_check.titansma.compare_config import \
    get_config_check_results
from station_config_check.titansma.golden_image import GoldenImageMissing, \
    load_golden_image, write_golden_image

from station_config_check.titansma.running_config import fetch_credentials, \
    get_running_config, get_titansma_list


@click.command()
@click.option(
    '--nagios-ip',
    help=('The IP address of the Nagios server to query and push results to')
)
@click.option(
    '--goldenimg-dir',
    help=('Parent directory of config golden images')
)
@click.option(
    '--cred-file',
    help=('File where credentials are stored')
)
@click.option(
    '--log-level',
    type=click.Choice([v.value for v in LogLevels]),
    help="Log more information about the program's execution",
    default=LogLevels.WARNING
)
def main(
    nagios_ip: str,
    goldenimg_dir: str,
    cred_file: str,
    log_level: str
):

    logging.basicConfig(
        format='%(asctime)s:%(levelname)s:%(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_level)
    # Read the cred file
    config = configparser.ConfigParser()
    config.read(cred_file)

    # Extract api_key from cred_file
    api_key = config['nagios']['api_key']

    # Get a list of all members of the Titan-SMA hostgroup
    titans = get_titansma_list(
        nagios_ip=nagios_ip,
        api_key=api_key
    )

    checkresults = NagiosCheckResults()

    for titan in titans:
        # Try to download the running config from the TitanSMA
        logging.debug(
            f'Trying to download running config from {titan.hostname}')
        try:
            running_config = get_running_config(
                titan_sma=titan,
                credentials=fetch_credentials(
                    install_type=titan.install_type,
                    config=config
                )
            )
        except urllib.error.URLError as e:
            # If for some reason the config cannot be downloaded, log the
            # error and move on to the next TitanSMA
            logging.warning(e)
            checkresults.append(NagiosCheckResult(
                hostname=titan.hostname,
                servicename='Config Check',
                state=NagiosOutputCode.critical.value,
                output='Host unreachable when downloading running config'
            ))
            continue

        try:
            logging.debug(f'Searching for {titan.hostname} in {goldenimg_dir}')
            # Try loading the goldem image from file
            golden_image = load_golden_image(
                goldenimg_dir=goldenimg_dir,
                host_name=titan.hostname
            )
        # If there is no golden image for this Titan
        except GoldenImageMissing as e:
            logging.warning(e)
            write_golden_image(
                goldenimg_dir=goldenimg_dir,
                host_name=titan.hostname,
                config=running_config
            )
            checkresults.append(NagiosCheckResult(
                hostname=titan.hostname,
                servicename='Config Check',
                output='No Golden Image present. New golden image saved.'
            ))
            continue

        # If a golden image was found, proceed with comparing it to the
        # running config
        logging.debug(f'Comparing config for {titan.hostname}')
        checkresults.append(get_config_check_results(
            hostname=titan.hostname,
            golden_image=golden_image,
            running_config=running_config
        ))

    submit(
        nrdp=checkresults,
        nagios=nagios_ip,
        token=config['nagios']['nrdp_token'])
    return


if __name__ == '__main__':
    main()
