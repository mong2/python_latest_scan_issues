import json

class ScansController(object):
	def clean_good_findings(self, scan_data):
		scan_data = [ x for x in scan_data["scan"]["findings"] if x["status"] == "bad" ]
		return scan_data

	def load_age(self, issue_data, param):
		for issue in issue_data["issues"]:
			if issue["name"] == param[0]:
				return issue["age"]
			elif len(param) > 1 and issue["name"] == ("%s.%s" % (param[0],param[1])):
				return issue["age"]

	def insert_age(self, scan_data, issue_data):
		self.clean_good_findings(scan_data)
		scan_type = scan_data["scan"]["module"]
		for finding in scan_data["scan"]["findings"]:
			if scan_type == "sca":
				finding["age"] = self.load_age(issue_data, [finding["rule_name"]])
			elif scan_type == "svm":
				finding["age"] = self.load_age(issue_data, [finding["package_name"],finding["package_version"]])
			elif scan_type == "fim":
				finding["age"] = self.load_age(issue_data, [finding["rule"]["target"]])
		return scan_data