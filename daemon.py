#!/usr/bin/python2
# -*- coding: utf-8 -*-

from sensnode import *

debug = False

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)

def main():
	print "sensnodeDaemon v%s started" % (get_version())
	r = Reader(debug)
	cfg = Config(debug)
	b = Base(debug)
	
	try:
		for Node in cfg.getNodesNames():
			b.createTable(Node)
	except Exception, e:
		sys.exit(e)

	try:	
		while True:
			raw = r.read()
			b.addRow(raw)

	except KeyboardInterrupt:
		print "Bye"
		sys.exit()

if __name__ == "__main__":
    main()
