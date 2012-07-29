{% include 'header_template.tpl' %}

<div class="page-header">
	<h2>{{title}}</h2>
	<h6>Lokalizacja czunika: {{local}}</h6>
	<h6>Ilość czujników: {{ units|length }}</h6>
</div>

{% for d in data %}
<div class="alert alert-info">
	<h3>{{ labels[loop.index0] }} [{{ units[loop.index0] }}]</h3>
</div>

<div id="graph_bound-{{ loop.index }}" style="height:500px;">
      <div id="graph-{{ loop.index }}"></div>
</div>

<script type="text/javascript">
$(function() {

		// Create the chart
		Highcharts.setOptions({
	lang: {
		months: ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'May', 'Czerwiec', 
			'Lipiec', 'Śierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
		weekdays: ['Nie', 'Pon', 'Wt', 'Śr', 'Czw', 'Pt', 'Sob']
	}
});
		window.chart = new Highcharts.Chart({
		    chart: {
		        renderTo: 'graph-{{ loop.index }}',
				type: 'spline'
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
				name: '{{ labels[loop.index0] }}',
		        data: {{d}}
		    }],
		});
	});
</script>

{% endfor %}
{% include 'footer_template.tpl' %}
