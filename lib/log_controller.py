import logbook


LOGGER = logbook.Logger('archive')
LOG = logbook.FileHandler('monitoring.log')
LOG.push_application()


class LogController(object):
	def __init__(self):
		pass
	def write_log(self, msg):
		LOGGER.info(msg)
