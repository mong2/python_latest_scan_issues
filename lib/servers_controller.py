from api_controller import ApiController


class ServersController(object):
    def __init__(self):
        self.api = ApiController()

    def index(self, **kwargs):
        return self.api.get_paginated("/v1/servers", **kwargs)

    def show(self, agent_id):
        return self.api.get("/v1/servers/%s" % agent_id)
