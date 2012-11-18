{% include 'header_template.tpl' %}

<div class="span12">
<div class="page-header">
  <h1>senscms <small>opensource low power sensors node</small></h1>
</div>
{# todo: tabelka generowania z konfiguracji #}
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
<h3>Aktualne odczyty:</h3>
<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="tstatus">
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
<script language="javascript">
// todo: odświeżanie po dodaniu dobazy danych
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
//      console.log(json)
  $('#tstatus').dataTable().fnDestroy();
  $('#tstatus').dataTable({
    "aaData": json,  
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
        return '<a href="/graph/' + data + '/2" title="Wykres">' + data + '</a>'
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
</script>

{% include 'footer_template.tpl' %}
