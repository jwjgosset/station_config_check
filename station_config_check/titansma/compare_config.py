import difflib
from typing import List
from station_config_check.nagios.models import NagiosOutputCode, \
    NagiosPerformance, NagiosResult, NagiosVerbose

from station_config_check.nagios.nrdp import NagiosCheckResult


def diff_percentage(
    golden_image: str,
    running_config: str
) -> float:
    '''
    Compares the running config to the golden image and reports a percentage
    of how similar they are.

    Parameters
    ----------
    golden_image: str
        Contents of the golden image config file as a single string

    running_config: str
        Contents of the current running config file as a single string

    Returns
    -------
    Float:
        The percentage of similarities between the two configurations.
    '''
    difference = difflib.SequenceMatcher(
        a=golden_image,
        b=running_config)

    return (difference.ratio())*100


def diff_list(
    golden_image: str,
    running_config: str
) -> List[str]:
    '''
    Compares the running config to the golden image and reports a list of the
    changes

    Parameters
    ----------
    golden_image: str
        Contents of the golden image config file as a single string

    running_config: str
        Contents of the current running config file as a single string

    List: List of lines that have changed
    '''

    golden = golden_image.split('\n')
    running = running_config.split('\n')
    differences = []

    d = difflib.Differ()

    for line in list(d.compare(golden, running)):
        if '+' in line[0]:
            differences.append(line.lstrip('+'))

    return differences


def get_config_check_results(
    hostname: str,
    golden_image: str,
    running_config: str
) -> NagiosCheckResult:
    percentage = diff_percentage(
        golden_image=golden_image,
        running_config=running_config
    )
    differences = diff_list(
        golden_image=golden_image,
        running_config=running_config
    )

    performance = NagiosPerformance(
        label='Config',
        value=percentage,
        uom='%'
    )

    if percentage < 100:
        state = NagiosOutputCode.critical
    else:
        state = NagiosOutputCode.ok

    result = NagiosResult(
        summary=f'Similarity between config files: {percentage}%',
        verbose=NagiosVerbose.multiline,
        status=state,
        performances=[performance],
        details='\n'.join(differences)
    )

    return NagiosCheckResult(
        hostname=hostname,
        servicename='Config Check',
        state=state.value,
        output=str(result))
