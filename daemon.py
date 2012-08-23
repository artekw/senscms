#!/usr/bin/python2
# -*- coding: utf-8 -*-

from sensnode import *

debug = False

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)

def main():
	print "sensnodeDaemon v0.4 started"
	r = Reader(debug)
#	cfg = Config(debug)
	b = Base(debug)
	
	b.createTable('node5')
	b.createTable('node2')
	b.createTable('node9')

	try:	
		while True:
			raw = r.read()
			b.addRow(raw)

	except KeyboardInterrupt:
		print "Bye"
		sys.exit()

if __name__ == "__main__":
    main()
