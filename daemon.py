#!/usr/bin/python2
# -*- coding: utf-8 -*-

__appname__ = 'sensnode-daemon'

from sensnode import *
import logging
import threading
import signal
import pyinotify
import subprocess
import os

debug = True

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def get_appname():
		return __appname__

def log(header, body):
	'''
	Simple log function. Need find better way
	'''
	printout (header + " ", GREEN)
	print body
	time.sleep(1)

# http://blog.mathieu-leplatre.info/colored-output-in-console-with-python.html
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

def printout(text, colour=WHITE):
        if has_colours:
                seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
                sys.stdout.write(seq)
        else:
                sys.stdout.write(text)

class EventHandler(pyinotify.ProcessEvent):
	def start_read(self):
		'''
		Start main thread
		'''
		self.s = main_app()
		self.s.setDaemon(True)
		self.s.start()
		self.s.webapp()

	def process_IN_CLOSE_WRITE(self, event):
		'''
		Event after close saved file
		'''
		printout ("[File saved] ", GREEN)
		print event.pathname
		if self.s.isAlive():
			self.s.stop()
			self.s.join()
			os.kill(self.s.webappp.pid, signal.SIGKILL)
			# restart thread - ugly, know better way ?
			self.s = main_app()
			self.s.setDaemon(True)
			self.s.start()
			self.s.webapp()

class main_app(threading.Thread):
	'''
	Main thread class
	'''
	def __init__(self):
		threading.Thread.__init__(self)
		self.running = True

	def stop(self):
		'''
		Set stop flag for thread
		'''
		self.running = False

	def webapp(self):
		'''
		Function to start webapp
		'''
		log("[Start]", "Webapp")
		self.webappp = subprocess.Popen(args=["python2", "webapp.py"], shell=False)
		time.sleep(2)
		print 'webapp\'s pid =',self.webappp.pid

	def run(self):
		'''
		Main thread Function
		'''
		log("[Start]", "Serial reader")
		r = Reader(debug)
		cfg = Config(debug)
		b = Base(debug)
		try:
			for Node in cfg.getNodesNames():
				b.createTable(Node)
		except Exception, e:
			sys.exit(e)

		while self.running:
			raw = r.read()
			b.addRow(raw)

class file_monitor(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		log("[Start]", "File monitor")

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
	m.setDaemon(True)
	m.start()

	try:
		while True: time.sleep(100)
	except (KeyboardInterrupt, SystemExit):
  		print '\n! Received keyboard interrupt, quitting threads.\n'

if __name__ == "__main__":
	main()