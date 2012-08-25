#!/usr/bin/python2
# -*- coding: utf-8 -*-

from sensnode import *

debug = True
ver = 0.4

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)

def main():
	print "sensnodeDaemon v%s started" % (ver)
	r = Reader(debug)
	cfg = Config(debug)
	b = Base(debug)
	
	try:
		for cfgNode in cfg.getNodesNames():
			b.createTable(cfgNode)
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
