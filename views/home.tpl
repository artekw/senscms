{% include 'header_template.tpl' %}

<div class="span12">
<div class="page-header">
  <h1>senscms <small>opensource low power sensors node</small></h1>
</div>
{# todo: tabelka generowania z konfiguracji #}
<h3>Aktualne odczyty:</h3>
<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="wtable">
        <thead>
        <tr>
				  <th>Ost. odczyt</th>
				  <th>Naz. punktu</th>
          <th>Temperatura</th>
          <th>Jasność</th>
          <th>Ciśnienie</th>
          <th>Wilgotność</th>
          <th>Nap. zasilania</th>
          <th>Bateria</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
<h3>power@house</h3>
<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="ptable">
        <thead>
        <tr>
          <th>Ost. odczyt</th>
          <th>Naz. punktu</th>
          <th>Napiecie</th>
          <th>Moc L1</th>
          <th>Moc L2</th>
          <th>Moc L3</th>
          <th>Suma mocy</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
{#
<body onload="initialize()">
    <span id="powerGaugeContainer"></span>
</body>
#}
<br />
<div id="loader">
    <div class="alert alert-info">
        <b>Wczytywanie...</b> <img src="/static/img/ajax-loader.gif">
    </div>
</div>

<div id="done">
    <div class="alert alert-success">
        </i><b>Gotowe!</b>
    </div>
</div>

<script language="javascript">
// todo: odświeżanie po dodaniu do bazy danych
  function requestData() {
  $.ajax({
    url: '/api/all',
    dataType: 'JSON',
    cache: false,
    asyn: false,
    beforeSend: function() {
      $('#loader').show();
      $('#done').hide();
    },
    complete: function(){
      $('#loader').hide();
      $('#done').show();
    },
    success: function(json) {
    console.log(json);
    // odzielamy dane
    // todo: node mierzący moc pobrać z pliku konfiguracyjnego
    var power_json = jQuery.grep(json, function(element, index) {
      return (element.nodeid == 'node25');
    });

    var condition_json = jQuery.grep(json, function(element, index) {
      return (element.nodeid != 'node25');
    });

  $('#wtable').dataTable().fnDestroy();
  $('#ptable').dataTable().fnDestroy();

  // condition
  $('#wtable').dataTable({
    "aaData": condition_json,  
    "bFilter": false,
    "bSearchable":false,
    "bInfo":false,
    "bPaginate": false,
    "bAutoWidth": false,
    "aaSorting": [[1, "asc"]], // sortowanie wg nodów
 
    "aoColumns":[
        {"mDataProp":"date"},
        {"mDataProp":"nodeid"},
        {"mDataProp":"temp", "sDefaultContent":"-"},
        {"mDataProp":"light", "sDefaultContent":"-"},
        {"mDataProp":"press", "sDefaultContent":"-"},
        {"mDataProp":"humi", "sDefaultContent":"-"},
        {"mDataProp":"batvol", "sDefaultContent":"-"},
        {"mDataProp":"lobat", "sDefaultContent":"-"}
    ],
    "aoColumnDefs": [{
       "aTargets": [7], // <- kolumna 'bateria'
       "mData": "lobat",
       "mRender": function (data, type, full) {
          if (data == "0") {
            return '<span class="label label-success">OK</span>'; 
          } else {
            return '<span class="label label-important">Słaba</span>'; 
          }
        }
    },
    {
      "aTargets": [1], // <- kolumna 'nodeid'
      "mData": "nodeid",
      "mRender": function (data, type, full) {
        var mydict = new Array();
        mydict = {{node_info}};
        console.log(mydict);
        return '<a href="/graph/' + data + '/2" title="Wykres dla ' + data + '">' + mydict[data] + '</a>'
      }
    } 
    ]
    });

  // power
  $('#ptable').dataTable({
    "aaData": power_json,  
    "bFilter": false,
    "bSearchable":false,
    "bInfo":false,
    "bPaginate": false,
    "bAutoWidth": false,
    "aaSorting": [[1, "asc"]], // sortowanie wg nodów
 
    "aoColumns":[
        {"mDataProp":"date"},
        {"mDataProp":"nodeid"},
        {"mDataProp":"vrms", "sDefaultContent":"-"},
        {"mDataProp":"power1", "sDefaultContent":"-"},
        {"mDataProp":"power2", "sDefaultContent":"-"},
        {"mDataProp":"power3", "sDefaultContent":"-"},
        {"mDataProp":"sumpower", "sDefaultContent":"-"}
    ],
    "aoColumnDefs": [
    {
      "aTargets": [1], // <- kolumna 'nodeid'
      "mData": "nodeid",
      "mRender": function (data, type, full) {
        var mydict = new Array();
        mydict = {{node_info}};
        console.log(mydict);
        return '<a href="/graph/' + data + '/2" title="Wykres dla ' + data + '">' + mydict[data] + '</a>'
      }
    }
    ]
    });
    setTimeout(requestData, 10000);    
    },
   });
}

$(document).ready(function() {
    requestData()
});
/*
      var gauges = [];

      function createGauge(name, label)
      {
        var config = 
        {
          size: 220,
          label: label,
          minorTicks: 5
        }

        config.redZones = [];
        config.redZones.push({ from: 100, to: 5000 });

        config.yellowZones = [];
        config.yellowZones.push({ from: 300, to: 1000 });

        gauges[name] = new Gauge(name + "GaugeContainer", config);
        gauges[name].render();
      }

      function createGauges()
      {
        createGauge("power", "Power");              
      }

      function updateGauges()
      {
        for (var key in gauges)
        {
          gauges[key].redraw(800);
        }
      }

      function initialize()
      {
        createGauges();
        setInterval(updateGauges, 5000);
      }
      */
</script>

{% include 'footer_template.tpl' %}
