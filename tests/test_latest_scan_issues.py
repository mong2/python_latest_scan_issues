import pytest
import sys
import os
import datetime
import cloudpassage
sys.path.append(os.path.join(os.path.dirname(__file__), '../', 'lib'))

from api_controller import ApiController


class TestLastScanIssues:

	def build_api_object(self):
		return ApiController()

	def build_test_timestamp(self):
		return (datetime.datetime.utcnow() - datetime.timedelta(days=10)).strftime("%Y-%m-%d")

	def test_server_filter(self):
		api = self.build_api_object()
		resp = api.get("/v1/servers?state=deactivated")
		assert resp["servers"]

		for server in resp["servers"]:
			assert server["state"] == "deactivated"

	def test_issue_filter(self):
		api = self.build_api_object()
		resp = api.get("/v2/issues?issue_type=sva")
		assert resp["issues"]

		for issue in resp["issues"]:
			assert issue["issue_type"] == "sva"
