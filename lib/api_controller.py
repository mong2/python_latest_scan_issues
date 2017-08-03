import re
import cloudpassage
from config import CONFIG


class ApiController():
    @staticmethod
    def build_http_session():
        key_id = CONFIG['key_id']
        secret_key = CONFIG['secret_key']

        session = cloudpassage.HaloSession(key_id,
                                           secret_key,
                                           api_port=CONFIG["api_port"],
                                           api_host=CONFIG["api_hostname"])
        return cloudpassage.HttpHelper(session)

    def get(self, endpoint):
        return self.build_http_session().get(endpoint)

    def find_primary_key(self, keys):
        blacklist = set(['count', 'pagination'])
        primary_key = list(set(keys) - blacklist)[0]
        return primary_key

    def get_paginated(self, endpoint, **kwargs):
        aggregate_result = []
        endpoint = endpoint + self.form_filter(**kwargs)
        index = self.get(endpoint)
        primary_key = self.find_primary_key(index.keys())
        while "pagination" in index:
            aggregate_result.extend(index[primary_key])
            if "next" in index["pagination"]:
                index = self.get(self.parse_next_endpoint(index["pagination"]["next"]))
            else:
                index[primary_key] = aggregate_result
                return index
        return self.get(endpoint)

    def parse_next_endpoint(self, next_url):
        return re.sub(r'^h.+om(:\d*)?', "", next_url)

    def form_filter(self, **kwargs):
        filter_list = []
        for filt in kwargs:
            if type(kwargs[filt]) is list:
                filter_list.append("%s=%s" % (filt, ','.join(kwargs[filt])))
            else:
                filter_list.append("%s=%s" % (filt, kwargs[filt]))
        return "?%s" % ("&".join(filter_list))
