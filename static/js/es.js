if (!!window.EventSource) {
  var source = new EventSource('/event');
  var oTable;
  console.log('start');
} else {
	console.log('error');
  // Result to xhr polling :(
}

source.onmessage = function (e) {
	console.log('message');
//	document.body.innerHTML = '';
//	document.getElementById('es').innerHTML = d[0].nodeid + '<br>' + d[0].press + '<br>' + d[0].temp;
	testdata = JSON.parse(e.data)
	console.log(testdata);
	if(oTable) {
		console.log("trying to destroy"); 
		oTable.fnDestroy();
			console.log("destroyed");
	}
	oTable = $('#ntable').dataTable({
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
	
//	$('#ntable').empty();
};
