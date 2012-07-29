{% include 'header_template.tpl' %}

<div class="page-header">
	<h2>{{title}}</h2>
	<h6>Lokalizacja czunika: {{local}}</h6>
	<h6>Ilość czujników: {{ units|length }}</h6>
</div>

<div class="alert alert-info">
	<h3>aaa</h3>
</div>

<div id="graph_bound" style="height:500px;">
      <div id="graph"></div>
</div>

<script type="text/javascript">
var chart; // global
function requestData() {
$.ajax({
    url: 'http://192.168.88.245:2233/api/node2/press/1',
    datatype: "json",
    success: function(data) {
		chart.series[0].setData(data);
		setTimeout(requestData, 1000);    
    },
    cache: false
   });
 }
 $(document).ready(function() {

		// Create the chart
		chart = new Highcharts.Chart({
		    chart: {
		        renderTo: 'graph',
				type: 'spline',
				events: { load: requestData }
		    },	
			title: {
				text: null
		},
			plotOptions: {
            series: {
                marker: {enabled: false},
				states: {
                    hover: {
                        enabled: false
                    }
                },
            }
			},
            xAxis: { type: 'datetime'},
			legend: { enabled: false },
		    series: [{
				name: 'press',
		        data: []
		    }],
		});
	});
</script>

{% include 'footer_template.tpl' %}
