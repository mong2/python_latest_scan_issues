from config import CONFIG
from servers_controller import ServersController
import datetime

class FilteredServer():
	def __init__ (self):
		self.server = ServersController()

	def filtered_srvs(self):
		kwargs = { "state": 'deactivated',
				   "last_state_change_gte": datetime.datetime.utcnow().strftime("%Y-%m-%d")}
		return self.server.index(**kwargs)["servers"]

	def active_srvs(self):
		return self.server.index()["servers"]

	def aggregated_srvs(self):
		active_srvs = self.active_srvs()
		if CONFIG["last_24_hours"]:
			filtered_srvs = self.filtered_srvs()
			for filtered_srv in filtered_srvs:
				active_srvs.append(filtered_srv)
		return active_srvs

