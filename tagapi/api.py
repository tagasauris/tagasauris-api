import requests

from binder import bind_api
from error import TagasaurisApiException


class TagasaurisClient(object):
    """ Tagasauris api client """

    def __init__(self, login, password, host='http://devel.tagasauris.com',
            api_version=2):

        self.host = host
        self.api_version = api_version
        self.session = requests.session()

        # Each api call is authenticated with login & pass!
        if login is not None and password is not None:
            credentials = {
                "login": login,
                "password": password
            }
            self.session.post("%s/api/2/login/" % self.host,
                data=credentials)

        # No auth data provided.
        else:
            raise TagasaurisApiException('Authentication required!')

    """ Job creation """
    create_job = bind_api(
        path='job/',
        method='post',
        required_params=['id', 'title', 'task', ['mediaobjects', 's3']]
    )

    """ Progress tracking """
    status_progress = bind_api(
        path='status/progress/{status_key}/',
        method='get',
        url_params=['status_key'],
        api_version=1
    )

    """ Messages tracking """
    status_messages = bind_api(
        path='status/messages/{status_key}/',
        method='get',
        url_params=['status_key'],
        optional_params=['page'],
        api_version=1
    )

    """ Transform result """
    transform_result = bind_api(
        path='transformresult/',
        method='get',
        optional_params=['job_id', 'created', 'correct', 'page', 'per_page'],
        api_version=3
    )

    """ Media object import """
    mediaobject_send = bind_api(
        path='mediaobject/import/',
        method='post',
        required_params=['mimetype', 'id', ['content', 'url']],
        optional_params=['title', 'labels', 'attributes'],
    )

    """ Media object validation """
    mediaobject_validate = bind_api(
        path='mediaobject/import/validate_only/',
        method='post',
        required_params=['mimetype', 'id', ['content', 'url']],
        optional_params=['title', 'labels', 'attributes'],
    )
