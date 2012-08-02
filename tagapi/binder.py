import json
import requests


def bind_api(**config):

    # class APIMethod(object):

    #     path = config['path']
    #     api_version = config.get('api_version', None)

    #     def __init__(self, api):
    #         self.api = api
    #         if self.api_version is None:
    #             self.api_version = self.api.api_version
    #         self.url = "%s/api/%s/%s" % (api.host, self.api_version, self.path)

    #     def execute(self):
    #         reply = requests.post(self.url,
    #             data=json.dumps(data),
    #             cookies=self.api.auth)
    #         return reply.content

    def _call(api, data):
        path = config['path']
        api_version = config.get('api_version', api.api_version)

        url = "%s/api/%s/%s" % (api.host, api_version, path)

        reply = requests.post(url,
            data=json.dumps(data),
            cookies=api.auth)
        return reply.content

    return _call
