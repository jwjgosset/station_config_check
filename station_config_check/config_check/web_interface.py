import http
import logging
import os
import hashlib
import http.cookiejar
from urllib import parse
import urllib


class GlobalCookieJar:
    def __init__(
        self,
        filename: str = None
    ):
        '''
        Initialize the CookieJar

        Parameters
        ----------
        Filename: str
            Specify a filename to store cookies in to keep it persistent.
            Default: None
        '''
        self.cookiejar = http.cookiejar.MozillaCookieJar(filename)
        if filename is not None and os.path.exists(filename):
            self.cookiejar.load(ignore_discard=True)

    def addCookieToJar(
        self,
        response: http.client.HTTPResponse,
        request: urllib.request.Request
    ):
        '''
        Add cookies from an http request and response to the cookie jar

        Parameters
        ----------
        response:
            An http response
        request:
            The http request that generated the response

        '''
        self.cookiejar.extract_cookies(response, request)
        if self.cookiejar.filename is not None:
            self.cookiejar.save(ignore_discard=True)

    def addCookieToAllRequests(self):
        '''
        Enables the addition of cookies to http requests

        Returns
        -------
        Self: This change is not done in place. The results of this function
        must be assigned to a new (or the same) GlobalCookieJar object
        '''
        urllib.request.install_opener(
            urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.cookiejar)))
        return self

    def addCookieToRequest(
        self,
        request: urllib.request.Request
    ):
        self.cookiejar.add_cookie_header(request)
        return self


def getHash(
    string: str
) -> str:
    '''
    Hashes an a string into md5 format

    Parameters
    ----------
    string: str
        The string to be hashed

    Returns
    -------
    str: The resulting hash
    '''
    return hashlib.md5(bytearray(string, 'ascii')).hexdigest()


class PowerManagerInterface:
    def __init__(
        self,
        address: str,
        username: str,
        password: str
    ):
        self.address = address
        self.username = username
        self.password = password

    def login(
        self,
        cookiejar: GlobalCookieJar
    ):
        url = f"http://{self.address}/login.php"
        data = parse.urlencode({
            'username': self.username,
            'password': self.password
        }).encode()
        login_request = urllib.request.Request(
            url, data=data, method='POST')
        login_response = urllib.request.urlopen(login_request)
        cookiejar.addCookieToJar(login_response, login_request)
        logging.debug(
            f'Response to login request: {login_response.read().decode()}')

    def get_config(self):
        url = f"http://{self.address}/system/exportSettings.php"
        config_request = urllib.request.Request(url)
        config_response = urllib.request.urlopen(config_request)
        return config_response.read().decode()


class DigitizerInterface:
    def __init__(
        self,
        address: str,
        username: str,
        password: str
    ):
        '''
        Initialize the digitizer interface

        Parameters
        ----------
        address: str
            The IP address or hostname for the digitizer

        username: str
            The username to log in as

        password: str
            The password for the user
        '''
        self.address = address
        self.username = username
        self.password = password

    def getUrl(
        self,
        relative: str
    ) -> str:
        '''
        Assemble the url for a page on the digitizer's web interface

        Parameters
        ----------
        relative: str
            The page on the digitizer interface to assemble a url for
        '''
        return 'http://' + self.address + '/' + relative

    def getKey(
        self,
        cookiejar: GlobalCookieJar
    ):
        '''
        Request a key from the digitizer and store it in a cookie jar

        Parameters
        ----------
        cookiejar:
            The cookie jar to store the key in
        '''

        key_url = self.getUrl('key')
        logging.debug(f'Sending request to {key_url}')
        request = urllib.request.Request(key_url)
        response = urllib.request.urlopen(request)
        cookiejar.addCookieToJar(response, request)
        key = response.read().decode('ascii')
        return key

    def login(
        self,
        cookiejar: GlobalCookieJar
    ):
        '''
        Login to the digitizer interface

        Parameters
        ----------
        cookiejar:
            The cookiejar to store cookies about the login session in
        '''

        key = self.getKey(cookiejar)
        encodedPassword = getHash(getHash(self.password) + key)

        login_url = self.getUrl('login')

        logging.debug(f'Sending request to {login_url}')

        login_request = urllib.request.Request(
            login_url, method='POST')
        login_request.add_header('X-NMX-USERNAME', self.username)
        login_request.add_header('X-NMX-PASSWORD', encodedPassword)
        login_response = urllib.request.urlopen(login_request)
        cookiejar.addCookieToJar(login_response, login_request)
        logging.debug(
            f'Response to login request: {login_response.read().decode()}')

    def getConfiguration(self) -> str:
        '''
        Download the current running config of the digitizer

        Returns
        -------
        str:
            Dump of the running config file as a single string
        '''

        config_url = self.getUrl('config')
        logging.debug(f'Sending request to {config_url}')
        request = urllib.request.Request(config_url)
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            logging.error(e)

        return response.read().decode()
