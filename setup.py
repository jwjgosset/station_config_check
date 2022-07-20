from setuptools import setup  # type: ignore
from setuptools import find_packages

setup(
    name='acquisition_nagios',
    version='0.0.1',
    description=('A tool for checking for changes in station device ' +
                 'configuration files'),
    author='Jonathan Gosset',
    author_email='jonathan.gosset@nrcan-rncan.gc.ca',
    packages=find_packages(exclude=('tests')),
    package_data={
    },
    python_requires='>3.7',
    # Requires python packages
    install_requires=[
        'requests',
        'click'
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
        ]
    }
)
