{% include 'header_template.tpl' %}

<div class="hero-unit">
  <h1>senscms<sup><small>alpha</small></sup></h1>
  <p>opensource low power sensors node</p>
  <p>
    <a class="btn btn-primary btn-large" href="http://lab.digi-led.pl" TARGET="_blank">
      Więcej..
    </a>
  </p>
</div>
{# todo: tabelka generowania z konfiguracji #}
<h3>Aktualne odczyty:</h3>
<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="ttable">
        <thead>
        <tr>
				  <th>Ost. odczyt</th>
				  <th>Naz. punktu</th>
          <th>Temperatura</th>
          <th>Jasność</th>
          <th>Ciśnienie</th>
          <th>Wilgotność</th>
          <th>Nap. zasilania</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
<script language="javascript">
//	console.log({{ last }});
	$('#ttable').dataTable({
    "aaData":{{ last }},
		"bFilter": false,
		"bSearchable":false,
		"bInfo":false,
		"bPaginate": false,
 
    "aoColumns":[
				{"mDataProp":"date"},
				{"mDataProp":"nodeid"},
        // todo: można to poprawić pobierając nazwy czujników z plik konfiguracyjnego - najwieksza ilośc z któregoś noda
				{"mDataProp":"temp", "sDefaultContent":"-"},
        {"mDataProp":"light", "sDefaultContent":"-"},
        {"mDataProp":"press", "sDefaultContent":"-"},
        {"mDataProp":"humi", "sDefaultContent":"-"},
        {"mDataProp":"batvol", "sDefaultContent":"-"}
    ]
    });
</script>

{% include 'footer_template.tpl' %}
