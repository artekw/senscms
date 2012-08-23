{% include 'header_template.tpl' %}

<div class="page-header">
	<h2>{{title}}</h2>
	<h6>Lokalizacja czunika: {{local}}</h6>
	<h6>Ilość czujników: {{ units|length }}</h6>
</div>

<div class="span7">
	<div class="btn-group" data-toggle="buttons-radio">
		{% for s in sensors %}
		<button class="btn {{s}}">{{labels[loop.index0]}}</button>
		{% endfor %}
	</div>
</div>
<div class="span11">
      <div id="graph"></div>
</div>

<script type="text/javascript">
var chart;
var days = 2; //history
var sens = "{{ sensors|first() }}"; // load first sensors data
$('.' + sens).addClass('active');
function requestData(sens) {
$.ajax({
    url: '/api/{{node}}/'+ sens + '/' + days,
    success: function(data) {
		chart.series[0].setData(data);
//		setTimeout(requestData(this), 1000);    
    },
    cache: false
   });
 }
$(document).ready(function() {

	Highcharts.setOptions({
	lang: {
		months: ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'May', 'Czerwiec', 
			'Lipiec', 'Śierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
		weekdays: ['Nie', 'Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob']
	}
	});
		chart = new Highcharts.StockChart({
		    chart: {
		        renderTo: 'graph',
		        events: { load: requestData(sens) },
		    },	
			
            credits: {
                enabled: 0
            },
			scrollbar: {
				enabled: 0
			},
			navigator: {
				enabled: false
			},
			rangeSelector : {
				enabled : false
			},
			plotOptions: {
				line: {
					connectNulls: false,
					lineWidth: 2
				}
			},
            xAxis: {
				type: 'datetime',
				gridLineWidth: 1,
				gridLineDashStyle: 'ShortDot',
				dateTimeLabelFormats: {
					second: '%Y-%m-%d<br/>%H:%M:%S',
					minute: '%Y-%m-%d<br/>%H:%M',
					hour: '%Y-%m-%d<br/>%H:%M',
					day: '%Y<br/>%m-%d',
					week: '%Y<br/>%m-%d',
					month: '%Y-%m',
					year: '%Y'
				},
				labels: {
					style: {
						color: '#000',
						fontSize: '13px',
						fontFamily: '"Droid Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
					}
				},

				title: {
					style: {
						color: '#333',
						fontWeight: 'normal',
						fontSize: '15px',
						fontFamily: '"Droid Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
					}
				}
			},
			yAxis: {
				minorTickInterval: 'auto',
				gridLineWidth: 1,
				gridLineDashStyle: 'ShortDot',
				minorGridLineDashStyle: 'ShortDot',
				lineColor: '#000',
				lineWidth: 1,
				tickWidth: 1,
				tickColor: '#000',
				labels: {
					style: {
						color: '#000',
						fontSize: '13px',
						fontFamily: '"Droid Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
					}
				},

				title: {
					style: {
						color: '#333',
						fontWeight: 'normal',
						fontSize: '15px',
						fontFamily: '"Droid Sans", "Helvetica Neue", Helvetica, Arial, sans-serif'
					}
				}
				
			},
			tooltip: {
            backgroundColor: {
                linearGradient: {
                    x1: 0, 
                    y1: 0, 
                    x2: 0, 
                    y2: 1
                },
                stops: [
                    [0, 'white'],
                    [1, '#EEE']
                ]
            },
            borderColor: 'gray',
            borderWidth: 1
			},
		    series: [{
				name: 'Odczyt',
		        data: [],
				color: '#287AA9',
		        tooltip: {
		        	valueDecimals: 2
		        }
		    }],
		});
	});		
{% for s in sensors %}
$(".{{s}}").click(function () 
     { 
       requestData("{{s}}")
     });
{% endfor %}
</script>

{% include 'footer_template.tpl' %}
