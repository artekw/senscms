{% include 'header_template.tpl' %}
<div class="page-header">
	<h2>{{title}}</h2>
</div>
<form class="form-horizontal" action="/tables" method="GET">
<fieldset>
<div class="control-group">
<label class="control-label" for="inputWarning">Punkt</label>
	<div class="controls">
		<select name="node" id="node">
            {% for n in nodes %}
                <option>{{n}}</option>
            {% endfor %}
              </select>
            </div>
</div>
<div class="control-group">
<label class="control-label" for="inputWarning">Czujnik</label>
	<div class="controls">
		<select name="sensor" id="sensor">
                <option>temp</option>
                <option>press</option>
                <option>humi</option>
                <option>light</option>
              </select>
            </div>
</div>
<div class="control-group">
<label class="control-label" for="inputWarning">Zakres czasowy</label>
	<div class="controls">
		<select name="timerange" id="timerange">
            {% for tr in timeranges.keys() %}
                <option>{{tr}}</option>
            {% endfor %}
        </select>
    </div>
</div>
<div class="form-actions">
	<button type="submit" class="btn btn-primary" name="send" value="send">Send query</button>
	<button class="btn">Cancel</button>
</div>
<input type='hidden' name='done' value='1'>
</fieldset>
</form>
{% if done %}
    <table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="tttable">
        <thead>
        <tr>
            <th>Data</th>
            <th>Odczyt</th>
        </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
<script language="javascript">
//    console.log({{datatables}});
    $('#tttable').dataTable({
        "aaData": {{datatables}},
        "aaSorting": [[0, "desc"]],
        "bFilter": false,
        "bSearchable":false,
        "bInfo":false,
        "bPaginate": false,
    });
</script>
{% endif %}

{% include 'footer_template.tpl' %}
