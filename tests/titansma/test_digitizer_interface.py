from station_config_check.config_check import web_interface


def test_getHash():
    hash = web_interface.getHash('some string')
    assert hash == '5ac749fbeec93607fc28d666be85e73a'


def test_digitizer_interface():
    address = '8.8.8.8'
    username = 'someone'
    password = 'fakepass'

    digint = web_interface.DigitizerInterface(
        address=address,
        username=username,
        password=password
    )

    url = digint.getUrl('config')

    assert url == 'http://8.8.8.8/config'
