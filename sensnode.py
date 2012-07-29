#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'Artur Wronowski'
__version__ = '0.4'
__appname__ = 'sensnode-core'
__license__ = 'GPL3'

# HELP:
# http://shallowsky.com/software/scripts/ardmonitor
# http://mysql-python.sourceforge.net/MySQLdb.html
# http://www.python.org/dev/peps/pep-0249/
# http://www.python.org/dev/peps/pep-0257/
# http://simplejson.readthedocs.org/en/latest/index.html#exceptions
# http://stackoverflow.com/questions/455580/json-datetime-between-python-and-javascript
# http://datatables.net/index
# SELECT DATE(date) AS theday, AVG(press) AS avgtmp FROM node2 WHERE DATE(date) BETWEEN NOW() - INTERVAL 7 DAY AND NOW() GROUP BY theday;
# http://www.voidspace.org.uk/python/configobj.html
# http://www.jqplot.com/index.php
# http://www.thomasfrank.se/mysql_to_json.html
# http://www.mongodb.org/display/DOCS/Home
# http://api.mongodb.org/python/current/

# TODO:
# - testy, testy
# - mongodb
# - wysyłanie do sesnnode

from socket import *
import MySQLdb
import time
import datetime
import calendar
import sys
import yaml
import simplejson

debug = False

try:
	f = open('daemon.yml')
	config = yaml.load(f)
except IOError:
	sys.exit('No config file. Bye')

class Config(object):
	"""Zarzdzanie konfiguracja w yaml"""
	def __init__(self, debug=False):
		self.config = config
		self.debug = debug

	def getNodesIds(self):
		"""Pobiera numery id nodow z konfiguracji"""
		self.nodes = []

		for node in self.config.viewkeys():
			if 'node' in node:
				self.nodes.append(str(node)[4:])
		return self.nodes

	def getSensorsNames(self, node):
		"""Pobiera nazwy czjnników dla noda"""
		self.node = node
		return self.config[node]['sensors'].viewkeys();

	def getNodesNames(self):
		"""Pobiera nazwy nodow z konfiguracji"""
		self.nodes = []

		for node in self.config.viewkeys():
			if 'node' in node:
				self.nodes.append(node)
		return self.nodes

class Reader(object):
	"""Odczyt danych z punktow"""
	def __init__(self, debug=False):
		self.config = config
		self.debug = debug
		self.running = False

		try:
			self.host = self.config['settings']['server']['host']
			self.port = self.config['settings']['server']['port']
			if self.debug:
				print "Trying connect to %s:%s" % (self.host, str(self.port))
		except:
			print "Can't read from config."
			sys.exit(3)

		try:
			self.soc = socket(AF_INET, SOCK_STREAM)
			self.soc.connect((self.host, self.port))
			if self.debug:
				print "Connected to %s:%s" % (self.host, str(self.port))
			self.running = True
		except socket.timeout:
			if self.debug:
				print "Socket timeout."
			self.running = False
		except IOError as ioe:
			if debug:
				print "IOError catched and ignored: ", type(ioe), ioe
		except:
			print "Can't connect."
			sys.exit(3)

	def read(self):
		ret = ''
		if self.running:
			while True:
				c = self.soc.recv(1)			
				if c == '\n' or c == '':
					break
				else:
					ret += c
			return ret
		else:
			print "Not connected."
			sys.exit(3)

	def __del__(self):
		self.soc.close()

class Base(object):
	"""Zarzadzanie baza danych"""
	def __init__(self, debug=False):
		self.config = config
		self.debug = debug
		self.data = {}
		try:
			self.conn = MySQLdb.connect(host=self.config['settings']['mysql']['host'], \
										port=3306, \
										user=self.config['settings']['mysql']['username'], \
										passwd=self.config['settings']['mysql']['password'], \
										db=self.config['settings']['mysql']['dbase_name'])
			
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit (1)
		if self.debug:
				print "Connected to %s database" % (self.config['settings']['mysql']['dbase_name'])
		self.cur = self.conn.cursor()
		
	def createTable(self, tname):
		self.tname = tname
		self.nodename = tname

		# sprawdz czy instnieje tabela
		self.cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (self.tname))
		if not bool(self.cur.rowcount):  
			try:
				# twórz nową
				slist = []
				try:
					if self.nodename in self.config.viewkeys():
						for i in self.config[self.nodename]['sensors'].viewkeys():
							slist.append(i)
				except Exception, e:
					sys.exit(e)
				SQL = "CREATE TABLE %s (id serial PRIMARY KEY, date timestamp, %s varchar(10))" % (self.tname, " varchar(10), ".join(str(x) for x in slist))
				if self.debug:
					print 'Query %s' % SQL
				try:
					self.cur.execute(SQL);
				except MySQLdb.DatabaseError, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					print "Cannot to create table, check your configuration file"
					sys.exit (1)
				if self.debug:		
					print ('Create table %s') % (self.nodename)
			except Exception, e:
				sys.exit(e)
		else:
			if self.debug:
				print ('Table %s exist') % (self.nodename)

	def addRow(self, data):
		c = Config(debug)
		self.values = []
		self.tnow = datetime.datetime.now()
		self.tnow = self.tnow.strftime("%Y-%m-%d %H:%M:%S")
		self.tname = None
		self.nodes = c.getNodesIds()
		self.nodata = False
		
		try:
			self.jdata = simplejson.loads(data)
		except (simplejson.decoder.JSONDecodeError, ValueError):
			if debug:
				print 'Decoding JSON has failed'
			self.nodata = True
		if self.nodata:
			pass
			if self.debug:
				print "No data from node"
		else:
			i = str(self.jdata['nodeid'])[0]
			if self.debug:
				print 'Reading from %s' % i
			if i in self.nodes:
#				if self.debug:
#					print 'Nodes in config %s' % self.nodes			
				self.tname = "node%s" % (i)
				self.cols = self.config['node'+i]['sensors'].keys()
				for j in self.cols:
					self.values.append(self.jdata[j])
				SQL = "INSERT INTO %s (%s,%s) VALUES ('%s','%s')" % (self.tname, "date", ",".join(str(x) for x in self.cols), self.tnow, "','".join(str(x) for x in self.values))
				del self.values[:]
				try:
					self.cur.execute(SQL)
					if self.debug:
						print "Data added to table %s" % self.tname
				except MySQLdb.ProgrammingError, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
				self.conn.commit()
			else:
				if self.debug:
					print "No node in config"
				pass

	def query(self, node, sensor, limit=0):
		self.sensor = sensor
		self.node = node
		self.limit = limit
		
		dthandler = lambda obj: calendar.timegm(obj.timetuple())*1000 if isinstance(obj, datetime.datetime) else None

		if limit == 0:
			SQL = "SELECT date, %s FROM %s" % (self.sensor, self.node)
		else:
			SQL = "SELECT date, %s FROM %s WHERE date > NOW() - INTERVAL %s DAY" % (self.sensor, self.node, self.limit)
		self.cur.execute(SQL)
				
		return simplejson.dumps(self.cur.fetchall(), default=dthandler)

	def queryLast(self, nodes):
		"""Pobiera ostatnie odczyty dla wybranych nodow - dane dla DataTables"""
		self.nodes = nodes
		self.data = []
		dthandler = lambda obj: obj.strftime("%d/%m/%Y %H:%M") if isinstance(obj, datetime.datetime) else None
		
		for n in self.nodes:
			SQL = "SELECT * FROM %s ORDER BY ID DESC LIMIT 0,1" % n
			self.cur.execute(SQL)
		
			try:
				self.query_result = [dict(line) for line in [zip([ column[0] for column in self.cur.description], row) for row in self.cur.fetchall()]]
				del self.query_result[0]['id']
				self.query_result[0]['nodeid'] = n
				self.data.append(self.query_result[0])
			except Exception, e:
				print "Error [%r]" % (e)
				sys.exit(1)
		return simplejson.dumps(self.data, default=dthandler)

	def __del__(self):
		self.cur.close()
		self.conn.close()
