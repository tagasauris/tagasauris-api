import json
import logging
import requests
from functools import wraps

from tools import flat_list
from error import TagasaurisApiException, TagasaurisUnauthorizedException

log = logging.getLogger(__file__)


def authenticated_call(func):
    """ In case of HTTP 401 response, tries to authenticate and send the call
        again.
    """
    @wraps(func)
    def wrapper(api, *args, **kwargs):
        try:
            return func(api, *args, **kwargs)
        except TagasaurisUnauthorizedException:
            log.info("Unauthorized call. Re-authorizing and retrying.")
            api.authenticate()
            return func(api, *args, **kwargs)
    return wrapper


def bind_api(**config):

    def _call(api, *args, **kwargs):
        path = config['path']
        method = config['method']
        sending_list = config.get('list', False)
        dump_json = config.get('json', True)
        url_params = config.get('url_params', [])
        required_params = config.get('required_params', [])
        optional_params = config.get('optional_params', [])
        timeout = config.get('timeout', None)
        api_version = config.get('api_version', api.api_version)

        if sending_list:
            # We are sending list of objects. We can pass list of these as
            # first argument or each as consecutive arg.
            if type(args[0]) is list:
                kwargss = args[0]
            else:
                kwargss = args
        else:
            # To keep checking mechanics same as for checking whole list of
            # objects.
            kwargss = [kwargs, ]

        # Check if we have all required params provided across all dicts (if
        # list) or in kwargs.
        for kw in kwargss:
            for r in required_params:
                if not isinstance(r, list):
                    r = [r]
                if not any([x in kw.keys() for x in r]):
                    raise TagasaurisApiException(
                        'Required parameter "%s" not provided!' % r[0])

        # We don't want to send garbage to api.
        allowed_parameters = list(flat_list(required_params)) +\
            list(flat_list(optional_params)) +\
            list(flat_list(url_params))
        for kw in kwargss:
            for k in kw.keys():
                if k not in allowed_parameters:
                    raise TagasaurisApiException("Unknown argument: %s." % k)

        # Filling path with arguments.
        format_data = {}
        try:
            for param in url_params:
                format_data.update({param: kwargs[param]})
        except KeyError, e:
            raise TagasaurisApiException(
                'Required parameter "%s" not provided!' % e.args[0])
        path = path.format(**format_data)

        # Formatting api endpoint.
        url = "%s/api/%s/%s" % (api.host, api_version, path)

        # Filter arguments contained in url path
        if sending_list:
            data = kwargss
        else:
            data = dict([(k, v) for k, v in kwargs.items()\
                if k not in url_params])

        data_serializer = lambda x: x
        if dump_json:
            data_serializer = json.dumps

        try:
            if method is 'post':
                reply = api.session.post(url,
                    data=data_serializer(data), timeout=timeout)

            if method is 'get':
                reply = api.session.get(url,
                    params=data, timeout=timeout)
        except requests.exceptions.Timeout:
            raise TagasaurisApiException("Tagasauris call %s timed out." % url)
        except requests.exceptions.ConnectionError:
            raise TagasaurisApiException("Tagasauris call %s failed." % url)

        if reply.status_code >= 400:
            exc_type = TagasaurisApiException
            if reply.status_code == 401:
                exc_type = TagasaurisUnauthorizedException

            raise exc_type(
                "Tagasauris call %s failed: %s." % (url, reply.content),
                response=reply)

        try:
            return json.loads(reply.content)
        except ValueError:
            return reply.content

    auth_required = config.get('auth_required', True)
    return authenticated_call(_call) if auth_required else _call
