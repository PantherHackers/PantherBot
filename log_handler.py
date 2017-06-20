import logging, sys

class PBLogHandler(logging.StreamHandler):

	def __init__(self):
		logging.StreamHandler.__init__(self)
		fmt = '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
		format_date = '%m/%d/%Y %I:%M:%S %p'
		formatter = logging.Formatter(fmt, format_date)
		self.setFormatter(formatter)