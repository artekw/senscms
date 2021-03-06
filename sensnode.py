#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'Artur Wronowski'
__version__ = '0.4-dev'
__appname__ = 'sensnode-core'
__license__ = 'GPL3'
__email__ = 'arteqw@gmail.com'

# TODO:
# - testy, testy
# - wysyłanie do sesnbase- OOK (On-Off-Keyring)
# - alery na maila, jabbera
# - ujenolicic plik konfiguracyjny
# - dodawanie kolumn do istniejacej tabeli
# - OperationalError: (1054, "Unknown column 'press' in 'field list'")
# - slownik NodeInfo - tylko to stosowac
# - power@home


import socket
import MySQLdb
import time
import datetime
import calendar
import sys
import yaml
import simplejson
import logging

debug = False
logging.basicConfig(
        format='%(asctime)-25s %(threadName)-15s %(levelname)-10s %(message)s',
        level=logging.DEBUG,
        datefmt='%d/%m/%Y %H:%M:%S')

try:
	f = open('daemon.yml')
	config = yaml.load(f)
except IOError:
	sys.exit('No config file. Bye')

#########################################################

def get_version():
		return __version__

def get_author():
		return __author__

def get_license():
		return __license__

def get_email():
		return __email__

########################################################

class Config(object):
	"""Zarzdzanie konfiguracja w yaml"""
	def __init__(self, debug=False):
		self.config = config
		self.debug = debug

	def getNodesIds(self):
		"""Pobiera numery id nodow z konfiguracji - lista"""

		self.nodes = [ str(node)[4:] for node in self.config.viewkeys() if 'node' in node ]
		return self.nodes

	def getSensorsNames(self, node):
		"""Pobiera nazwy czujnników dla noda"""
		self.node = node
		return self.config[node]['sensors'].viewkeys();

	def getNodesNames(self):
		"""Pobiera nazwy nodow z konfiguracji - lista"""

		self.nodes = [node for node in self.config.viewkeys() if 'node' in node ]
		return self.nodes

	def getSensorDesc(self):
		"""Pobiera opisy nodow z konfiguracji - lista"""
		self.descs = []
		self.nodes = self.getNodesNames()

		for node in self.nodes:
			desc = self.config[node]['desc']
			self.descs.append(desc)
		return self.descs

	def crNodeInfo(self):
		"""Tworzy slownik nodeid:opis"""
		return dict(zip(self.getNodesNames(), self.getSensorDesc()))

########################################################

class Reader(object):
	"""Odczyt danych z punktow"""
	def __init__(self, debug=False):
		self.config = config
		self.debug = debug
		self.connected = False

		try:
			self.host = self.config['settings']['daemon']['host']
			self.port = self.config['settings']['daemon']['port']
			if self.debug:
				logging.debug('Trying connect to %s:%s' % (self.host, str(self.port)))
		except:
			print "Can't read from config."
			sys.exit(3)

		try:
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.soc.connect((self.host, self.port))
			if self.debug:
				logging.debug('Connected to %s:%s' % (self.host, str(self.port)))
			self.connected = True
	
		except socket.error:
			logging.warning("Can't connect to %s:%s" % (self.host, str(self.port)))
			self.connected = False
			sys.exit(3)

	def is_connected(self):
		return self.connected

	def serialread(self):
		"""Czyta z konsoli szeregowej"""
		ret = ''
		if self.connected:
			while True:
				c = self.soc.recv(1)			
				if c == '\n' or c == '':
					break
				else:
					ret += c
			return ret

	def __del__(self):
		self.soc.close()

########################################################

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
				logging.debug('Connected to %s database' % (self.config['settings']['mysql']['dbase_name']))
		self.cur = self.conn.cursor()
		
	def createTable(self, tname):
		"""Tworzy tabele"""
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
					# float temp ?
				SQL = "CREATE TABLE %s (id serial PRIMARY KEY, date timestamp, %s varchar(10))" % (self.tname, " float, ".join(str(x) for x in slist))
				# czemu ostatia to varint ?
				try:
					print SQL
					self.cur.execute(SQL);
				except MySQLdb.DatabaseError, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
					print "Cannot to create table, check your configuration file"
					sys.exit (1)
				if self.debug:		
					logging.debug('Create table %s' % (self.nodename))
			except Exception, e:
				sys.exit(e)
		else:
			if self.debug:
				logging.debug('Table %s exist. Aborted.' % (self.nodename))

	def addRow(self, data):
		"""Dodaje dane do tabeli"""
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
				logging.debug('Decoding JSON has failed')
			self.nodata = False
		if self.nodata:
			pass
			if self.debug:
				logging.debug('No data from node')
		else:
			i = str(self.jdata['nodeid']).rstrip('.0')
			if self.debug:
				logging.debug('Get data from %s' % i)
			if i in self.nodes:		
				self.tname = "node%s" % (i)
				self.cols = self.config['node'+i]['sensors'].keys()
				for j in self.cols:
					self.values.append(self.jdata[j])
				SQL = "INSERT INTO %s (%s,%s) VALUES ('%s','%s')" % (self.tname, "date", ",".join(str(x) for x in self.cols), self.tnow, "','".join(str(x) for x in self.values))
				del self.values[:]
				try:
					self.cur.execute(SQL)
					if self.debug:
						logging.debug('Data added to table %s' % self.tname)
				except MySQLdb.ProgrammingError, e:
					print "Error %d: %s" % (e.args[0], e.args[1])
				self.conn.commit()	
			else:
				if self.debug:
					logging.debug('No node in config')
				pass

	def query(self, node, sensor, limit=0, utc=0):
		"""Wysyla zapytanie do bazy"""
		self.sensor = sensor
		self.node = node
		self.limit = limit

		if utc: # data dla 'datatables'
			dthandler = lambda obj: obj.strftime("%d/%m/%Y %H:%M") if isinstance(obj, datetime.datetime) else None
		else:
			dthandler = lambda obj: calendar.timegm(obj.timetuple())*1000 if isinstance(obj, datetime.datetime) else None

		if limit == 0: # wszystkie 
			SQL = "SELECT date, %s FROM %s" % (self.sensor, self.node)
		elif limit == -1: # ostatni 
			SQL = "SELECT date, %s FROM %s ORDER BY ID DESC LIMIT 0,1" % (self.sensor, self.node)
		else: # okreslone dni
			SQL = "SELECT date, %s FROM %s WHERE date > NOW() - INTERVAL %s DAY" % (self.sensor, self.node, self.limit)
		self.cur.execute(SQL)

		return simplejson.dumps(self.cur.fetchall(), default=dthandler)

	def queryLast(self, nodes):
		"""Pobiera ostatnie odczyty dla wybranych nodow - dane dla DataTables
		todo: wyjatek - gdy pusta baza = brak danych = crash
		"""
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