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
	testdata = {{ last }};
	console.log(testdata);
	$('#ttable').dataTable({
        "aaData":testdata,
		"bFilter": false,
		"bSearchable":false,
		"bInfo":false,
		"bPaginate": false,
 
         "aoColumns":[
				{"mDataProp":"date"},
				{"mDataProp":"nodeid"},
				{"mDataProp":"temp"},
                {"mDataProp":"light"},
                {"mDataProp":"press"},
                {"mDataProp":"humi"},
                {"mDataProp":"batvol"}]
    });
</script>

{% include 'footer_template.tpl' %}
