#!/usr/bin/python2
# -*- coding: utf-8 -*-


# http://twitter.github.com/bootstrap/
# http://dygraphs.com/
# http://datatables.net/forums/discussion/6655/dynamically-apply-datatables-for-subsequent-requests/p1

# TODO:
# - odczyt z yaml - desc, unit
# - SSE
# - tabelki

rootSN ='/home/artek/pycode/senscms'

from sensnode import *
import simplejson
from bottle import route, error, template, response, run, static_file, jinja2_view as view, jinja2_template as template
# import string

debug = False

try:
	f = open('daemon.yml')
	config = yaml.load(f)
except IOError:
	sys.exit('No config file. Bye')
	
@route('/')
def home():
	base = Base()
	
	last = base.queryLast(['node2','node5'])
	
	return template('home', last=last, title="senscms")

@route('/graph/<node>')
def graph(node):
	labels = []
	units = []
	cfg = Config()
	base = Base()
	
	sensors = cfg.getSensorsNames(node)

	
	local = config[node]['desc']
		
	labels = [config[node]['sensors'][s]['desc'] for s in sensors]
	units = [config[node]['sensors'][s]['unit'] for s in sensors]

	return template('graph', node=node, sensors=sensors, labels=labels, units=units, local=local, title='Ostatnie 48h dla %s' % (node.upper()))

@route('/api/<node>/<sensor>/<limit:int>', method='GET')
def get(node, sensor, limit):
	response.content_type = 'text/json'
	base = Base()

	result = base.query(node, sensor, limit)
	if not result:
		abort(400, 'No data reveived')
	return result

@route('/tables')
def tables():
	
	return template('tables', title="Tabele")

@route('/contact')
def contact():
	
	return template('contact', title="Kontakt")	

@route('/live')
def live():
	return template('es', title="Live!")

@route('/event')
def event():
	response.content_type = 'text/event-stream'
	response.set_header('Cache-Control', 'no-cache');

	cfg = Config()
	base = Base()

	last = base.queryLast(cfg.getNodesNames())

	return "data: %s" % (str(last))

@route('/js/:filename#.*#')
def static_js(filename):
	return static_file(filename, root=rootSN + '/static/js/')
	
@route('/style/:filename#.*#')
def static_style(filename):
	return static_file(filename, root=rootSN + '/static/')

run(host='192.168.88.245', port=2233, server='bjoern')
