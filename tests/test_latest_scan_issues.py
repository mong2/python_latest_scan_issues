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
		return (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

	def test_server_filter():
		api = self.build_api_object()
		resp = api.get("/v1/servers?last_state_change_gte=%s" % self.build_test_timestamp())
		assert resp["servers"]

		for server in resp["servers"]:
			assert server["last_state_change"] >= self.build_test_timestamp

	def test_issue_filter():
		api = self.build_api_object()
		resp = api.get("/v2/issues?issue_type=sva")
		assert resp["issues"]

		for issue in resp["issues"]:
			assert issue["issue_type"] == "sva"
