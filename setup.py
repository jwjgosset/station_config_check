from setuptools import setup  # type: ignore
from setuptools import find_packages

setup(
    name='station_config_check',
    version='0.2.0',
    description=('A tool for checking for changes in station device ' +
                 'configuration files'),
    author='Jonathan Gosset',
    author_email='jonathan.gosset@nrcan-rncan.gc.ca',
    packages=find_packages(exclude=('tests')),
    package_data={
    },
    python_requires='>3.6',
    # Requires python packages
    install_requires=[
        'requests',
        'click',
        'dataclasses',
        'getpass'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'mypy'
        ]
    },
    entry_points={
        'console_scripts': [
            'check_all_titansma_config = \
                station_config_check.bin.check_all_titansma:main',
            'check_all_fortimus_config = \
                station_config_check.bin.check_all_fortimus:main',
            'get_titansma_config =\
                station_config_check.bin.get_titansma_config:main'
        ]
    }
)
