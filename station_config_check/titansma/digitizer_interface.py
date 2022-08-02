import http
import logging
import os
import hashlib
import http.cookiejar
import urllib.request
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
        request = urllib.request.Request(self.getUrl('/key'))
        response = urllib.request.urlopen(request)
        cookiejar.addCookieToJar(response, request)
        return response.read().decode('ascii')

    def login(self, cookiejar):
        '''
        Login to the digitizer interface

        Parameters
        ----------
        cookiejar:
            The cookiejar to store cookies about the login session in
        '''

        key = self.getKey(cookiejar)
        encodedPassword = getHash(getHash(self.password) + key)

        login_url = self.getUrl('/login')

        logging.debug(f'Sending request to {login_url}')

        login_request = urllib.request.Request(
            login_url, method='POST')
        login_request.add_header('X-NMX-USERNAME', self.username)
        login_request.add_header('X-NMX-PASSWORD', encodedPassword)
        return urllib.request.urlopen(login_request)

    def getConfiguration(self) -> str:
        '''
        Download the current running config of the digitizer

        Returns
        -------
        str:
            Dump of the running config file as a single string
        '''

        config_url = self.getUrl('/config')
        logging.debug(f'Sending request to {config_url}')
        request = urllib.request.Request(config_url, method='POST')
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e)
        logging.debug(response)
        return response.read().decode()
