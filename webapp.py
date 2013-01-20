#!/usr/bin/python2
# -*- coding: utf-8 -*-

__appname__ = 'sensnode-webapp'

# TODO:
# - odczyt z yaml - desc, unit
# - SSE
# - polskie znaki

rootSN ='/home/artek/http/sensnode.suwalki.pl'

from sensnode import *
import simplejson
from bottle import route, abort, error, template, response, request, run, static_file, jinja2_view as view, jinja2_template as template

debug = False

try:
	f = open('daemon.yml')
	config = yaml.load(f)
except IOError:
	sys.exit('No config file. Bye')

timerange = {
		'1':'24h',
		'2':'48h',
		'7':'tydzien',
		'14':'2 tygodnie',
		'30':'miesiac',
		'90':'3 miesiace',
		'180':'6 miesiecy',
		'365':'rok'
}

########################################################

@route('/')
def home():
	base = Base()
	cfg = Config()

	nodes = cfg.getNodesNames()
	nodeinfo = cfg.crNodeInfo()

	last = base.queryLast(nodes)
	
	return template('home', active = 'home', last=last, node_info=nodeinfo, title="senscms")

########################################################

@route('/graph/<node>/<limit:int>')
def graph(node, limit):
	labels = []
	units = []
	cfg = Config()
	base = Base()

	sensors = cfg.getSensorsNames(node)
	nodeinfo = cfg.crNodeInfo()

	grange = timerange[str(limit)]

	local = config[node]['desc']
	labels = [config[node]['sensors'][s]['desc'] for s in sensors]
	units = [config[node]['sensors'][s]['unit'] for s in sensors]

	return template('graph', active = 'graph', node_info=nodeinfo, node=node, sensors=sensors, labels=labels, units=units, local=local, limit=limit, title='%s' % (grange))

########################################################

@route('/api/<node>', method='GET')
@route('/api/<node>/<sensor>/<limit:int>', method='GET')
def get(node, sensor=None, limit=None):
	'''
	todo: dodac obsluge bledow
	'''
	response.content_type = 'text/json'
	base = Base()
	cfg = Config()
	nodes = cfg.getNodesNames()

	try:
		if node == 'all':
			result = base.queryLast(nodes)
		else:
			result = base.query(node, sensor, limit)
	except Exception:
		abort(404)
	return result

########################################################

@route('/contact')
def contact():
	cfg = Config()
	nodeinfo = cfg.crNodeInfo()
	
	return template('contact', active = 'kontakt', node_info=nodeinfo, title="Kontakt")	

########################################################

@route('/live')
def live():
	cfg = Config()
	nodeinfo = cfg.crNodeInfo()

	return template('es', active = 'live', node_info=nodeinfo, title="Live!")

########################################################

@route('/event')
def event():
	response.content_type = 'text/event-stream'
	response.set_header('Cache-Control', 'no-cache');

	cfg = Config()
	base = Base()

	last = base.queryLast(cfg.getNodesNames())

	return "data: %s" % (str(last))

########################################################

@route('/js/:filename#.*#')
def static_js(filename):
	return static_file(filename, root=rootSN + '/static/js/')

########################################################

@route('/static/:filename#.*#')
def static_files(filename):
	return static_file(filename, root=rootSN + '/static/')

########################################################

@error(404)
def error404(error):
    return 'Data not retrived'
########################################################

@route('/tables', method='get')
def tables():
	'''
	todo: poprawic sortowanie po dacie
	http://www.datatables.net/forums/discussion/2467/need-help-for-sorting-date-with-ddmmyyyy-format/p1
	'''
	cfg = Config()
	b = Base()

	nodes = cfg.getNodesNames()
	descs = cfg.getSensorDesc()

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

		datatables = b.query(form_node, form_sensor, form_timerange, '1') # utc=1 wiec data 'normalna'

		return template('tables', active = 'tables', nodes_menu=nodes, descs_menu = descs, nodes=cfg.getNodesNames(), done = form_done, datatables = datatables, timeranges = timeranges, title="Tabele")
	return template('tables', active = 'tables', nodes_menu=nodes, descs_menu = descs, nodes=cfg.getNodesNames(), done = form_done, timeranges = timeranges,  title="Tabele")

########################################################

run(host=config['settings']['webapp']['host'], 
	port=config['settings']['webapp']['port'], 
	server=config['settings']['webapp']['server']
	)
