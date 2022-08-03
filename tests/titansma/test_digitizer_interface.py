from station_config_check.titansma import digitizer_interface


def test_getHash():
    hash = digitizer_interface.getHash('some string')
    assert hash == '5ac749fbeec93607fc28d666be85e73a'


def test_digitizer_interface():
    address = '8.8.8.8'
    username = 'someone'
    password = 'fakepass'

    digint = digitizer_interface.DigitizerInterface(
        address=address,
        username=username,
        password=password
    )

    url = digint.getUrl('config')

    assert url == 'http://8.8.8.8/config'
