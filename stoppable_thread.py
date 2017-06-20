import threading, sys, logging
import log_handler
# class StopThread(StopIteration): pass

# threading.SystemExit = SystemExit, StopThread

# class StoppableThread(threading.Thread):

# 	def stop(self):
# 		raise StopThread()


class StoppableThread(threading.Thread):
	def __init__(self, websocket=None, kwargs=None):
		self._stop_event = threading.Event()
		self.ws = websocket
		self.kwargs = kwargs


		super(StoppableThread, self).__init__()

	def stop(self):
		logger = logging.getLogger('PantherBot')
		logger.setLevel(logging.INFO)
		logger.addHandler(log_handler.PBLogHandler())

		self.ws.keep_running = False
		logger.info("Stopping thread")

	def run(self):
		print "lmao"
		# self.ws = websocket
		self.ws.keep_running = True
		self.wst = threading.Thread(target=self.ws.run_forever)
		self.wst.start()
