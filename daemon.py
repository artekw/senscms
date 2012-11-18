#!/usr/bin/python2
# -*- coding: utf-8 -*-

__appname__ = 'sensnode-daemon'

from sensnode import *
import threading
import signal
import pyinotify
import subprocess
import os

debug = True

def get_appname():
		return __appname__

class EventHandler(pyinotify.ProcessEvent):
	def start_read(self):
		'''
		Start main thread
		'''
		self.s = main_app()
		self.s.setName('main-thread')
		self.s.setDaemon(True)
		self.s.test()
		self.s.start()
		self.s.webapp()

	def process_IN_CLOSE_WRITE(self, event):
		'''
		Event after close saved file
		'''
		logging.info('File saved %s' % (event.pathname))
		if self.s.isAlive():
			self.s.stop()
			self.s.join()
			os.kill(self.s.webappp.pid, signal.SIGKILL)
			# restart thread - ugly, know better way ?
			self.s = main_app()
			self.s.setName('main-thread')
			self.s.setDaemon(True)
			self.s.test()
			self.s.start()
			self.s.webapp()

class main_app(threading.Thread):
	'''
	Main thread class
	'''
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True

	def test(self):
		'''
		Test connection to host
		'''
		r = Reader()

		if r.is_connected():
			self.running = True
		else:
			self.running = False

	def stop(self):
		'''
		Set stop flag for thread
		'''
		self.running = False

	def webapp(self):
		'''
		Function to start webapp
		'''
		if self.running:
			logging.info('Start WebApp')
			# todo: config webapp filename
			self.webappp = subprocess.Popen(args=["python2", "webapp.py"], shell=False)
			time.sleep(2)
			logging.info('WebApp pid is %s' % (self.webappp.pid))

	def run(self):
		'''
		Main thread Function
		'''
		logging.info('Start SerialReader')
		r = Reader(debug)
		cfg = Config(debug)
		b = Base(debug)

		try:
			for Node in cfg.getNodesNames():
				b.createTable(Node)
		except Exception, e:
			sys.exit(e)

		while self.running:
			raw = r.serialread()
			b.addRow(raw)
			

class file_monitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		logging.info('Start FileMon')
		eh = EventHandler()
		eh.start_read()

		wm = pyinotify.WatchManager()
		wm.add_watch('daemon.yml', pyinotify.IN_CLOSE_WRITE)
		notifier = pyinotify.Notifier(wm, eh)
		notifier.loop()

def main():
	'''
	Main daemon function
	'''
	print "%s v%s started" % (get_appname(), get_version())
	print "Author: %s <%s>" % (get_author(), get_email())
	print "License: %s" % (get_license())
	m = file_monitor()
	m.setName('file-monitor')
	m.setDaemon(True)
	m.start()

	try:
		while True: time.sleep(100)
	except (KeyboardInterrupt, SystemExit):
  		print '\n! Received keyboard interrupt, quitting threads.\n'

if __name__ == "__main__":
	main()