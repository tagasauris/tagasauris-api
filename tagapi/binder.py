import json

from tools import flat_list
from error import TagasaurisApiException


def bind_api(**config):

    def _call(api, *args, **kwargs):
        path = config['path']
        method = config['method']
        required_params = config.get('required_params', [])
        optional_params = config.get('optional_params', [])
        api_version = config.get('api_version', api.api_version)

        # Check if we have all required params provided
        for r in required_params:
            if not isinstance(r, list):
                r = [r]
            if not any([x in kwargs.keys() for x in r]):
                raise TagasaurisApiException(
                    'Required parameter "%s" not provided!' % r[0])

        # We don't want to send garbage to api.
        allowed_paams = list(flat_list(required_params)) +\
            list(flat_list(optional_params))
        for k in kwargs.keys():
            if k not in allowed_paams:
                raise TagasaurisApiException("Unknown argument: %s." % k)

        url = "%s/api/%s/%s" % (api.host, api_version, path)

        if method is 'post':
            reply = api.session.post(url,
                data=json.dumps(kwargs))

        if method is 'get':
            reply = api.session.get(url,
                params=kwargs)

        return reply.content

    return _call
