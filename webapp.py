#!/usr/bin/python2
# -*- coding: utf-8 -*-

__appname__ = 'sensnode-webapp'

# http://twitter.github.com/bootstrap/
# http://dygraphs.com/
# http://datatables.net/forums/discussion/6655/dynamically-apply-datatables-for-subsequent-requests/p1

# TODO:
# - odczyt z yaml - desc, unit
# - SSE
# - tabelki

rootSN ='/home/artek/http/sensnode.suwalki.pl'

from sensnode import *
import simplejson
from bottle import route, error, template, response, request, run, static_file, jinja2_view as view, jinja2_template as template
from collections import OrderedDict
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

@route('/tables', method='get')
def tables():
	'''
	todo: poprawic sortowanie po dacie
	http://www.datatables.net/forums/discussion/2467/need-help-for-sorting-date-with-ddmmyyyy-format/p1
	'''
	cfg = Config()
	b = Base()

	# hours to days
	timeranges = OrderedDict([
				('24h','1'),
				('48h','2'),
				('week','7'),
				('month','30'),
				('3 months','90'),
				('year','365')
				])

	form_node = request.GET.get('node','').strip()
	form_sensor = request.GET.get('sensor','').strip()
	form_timerange = request.GET.get('timerange','').strip()
	form_done = request.GET.get('done','').strip()

	if request.GET.get('send','').strip():
		try:
			form_timerange = timeranges[form_timerange]
		except:
			return "error"

		datatables = b.query(form_node, form_sensor, form_timerange, '1') # t=1 wiec data 'normalna'

		return template('tables', nodes=cfg.getNodesNames(), done = form_done, datatables = datatables, timeranges = timeranges, title="Tabele")
	return template('tables', nodes=cfg.getNodesNames(), done = form_done, timeranges = timeranges,  title="Tabele")

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

run(host='0.0.0.0', port=8080, server='gunicorn')
