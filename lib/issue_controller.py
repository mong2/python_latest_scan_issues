from api_controller import ApiController
import dateutil.parser


class IssuesController(object):
    def __init__(self):
        self.api = ApiController()

    def index(self, **kwargs):
        return self.api.get_paginated("/v2/issues", **kwargs)

    def show(self, issue_id):
        return self.api.get("/v2/issues/%s" % issue_id)

    def age(self, created_at, last_see_at):
        age = dateutil.parser.parse(last_see_at) - dateutil.parser.parse(created_at)
        return str(age.days)

    def insert_age(self, issue_data):
        for issue in issue_data["issues"]:
            issue["age"] = self.age(issue["created_at"], issue["last_seen_at"])
        return issue_data
