import requests

from binder import bind_api
from error import TagasaurisApiException


class API(object):
    """ Tagasauris api client """

    def __init__(self, auth=None, login=None, password=None,
            host='devel.tagasauris.com', api_version=2):

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
            raise TagasaurisApiException('Authentication required!')

    """ Job creation """
    create_job = bind_api(
        path='job/',
        method='post',
        required_params=['id', 'title', 'task', ['mediaobject', 's3']]
    )

    """ Transform result """
    transform_result = bind_api(
        path='transformresult/',
        method='get',
        optional_params=['job_id', 'created', 'correct', 'page', 'per_page'],
        api_version=3
    )
