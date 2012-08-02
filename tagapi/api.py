import requests

from binder import bind_api
from error import TagApiException


class API(object):
    """ Tagasauris api client """

    def __init__(self, auth=None, login=None, password=None,
            host='tagasauris.com', api_version=2):

        self.host = host
        self.api_version = api_version
        self.auth = auth

        # Unless we provide auth cookies we must use login & pass.
        # Each api call is authenticated!
        if self.auth is None and login is not None and password is not None:
            credentials = {
                "login": login,
                "password": password
            }
            reply = requests.post("%s/api/2/login/" % self.host,
                data=credentials)
            self.auth = reply.cookies

        if not self.auth:
            raise TagApiException('Authentication required!')

    """ Job creation """
    create_job = bind_api(path='job/')
