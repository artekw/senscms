<html>
 <head>
    <meta charset="utf-8">
    <title>{{title or 'No title'}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="senscms">
    <meta name="author" content="arteq">
	
    <link href="/static/bootstrap.min.css" rel="stylesheet" type="text/css"></link>
    <link href="/static/DT_bootstrap.css" rel="stylesheet" type="text/css"></link>
    <style type="text/css">
      body {
        padding-top: 60px;
        padding-bottom: 40px;
      }
      
    </style>
    <link rel="shortcut icon" href="/style/favicon.ico">
    <link href="/static/bootstrap-responsive.min.css" rel="stylesheet" type="text/css"></link>
    <link href="/static/custom.css" rel="stylesheet" type="text/css"></link>
    <script language="javascript" type="text/javascript" src="http://code.jquery.com/jquery.min.js"></script>
    <script language="javascript" type="text/javascript" src="http://d3js.org/d3.v2.min.js"></script>
    <script language="javascript" type="text/javascript" src="/js/highstock.js"></script>
    <script language="javascript" type="text/javascript" src="/js/jquery.dataTables.js"></script>
    <script language="javascript" type="text/javascript" src="/js/bootstrap.min.js"></script>
    <script language="javascript" type="text/javascript" src="/js/underscore-min.js"></script>
    <script language="javascript" type="text/javascript" src="/js/gauge.js"></script>
 </head>
 <body>
 <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container-fluid">
          <a class="brand" href="/">senscms<sup><em>alpha</em></sup></a>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li {% if active == 'home' %} class="active"{% endif %}><a href="/">Status</a></li>
              <li  class="dropdown">
                <a href="#" class="dropdown-toggle" data-toggle="dropdown">Wykresy <b class="caret"></b></a>
                <ul class="dropdown-menu">
                  {% for k, v in node_info.iteritems() %}
                    <li><a href="/graph/{{k}}/2">{{k}}({{v}})</a></li>
                  {% endfor %}
                </ul>
              </li>
              <li {% if active == 'kontakt' %}class="active"{% endif %}><a  href="/contact">Kontakt</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
 <div class="container-fluid">
	<div class="row-fluid">
	
 
