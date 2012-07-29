{% include 'header_template.tpl' %}
<div class="page-header">
	<h2>{{title}}</h2>
</div>
<div class="well">
<strong>Work in progress</strong>
</div>
<form class="form-horizontal">
<fieldset>
<div class="control-group">
<label class="control-label" for="inputWarning">Node</label>
	<div class="controls">
		<select id="select01">
                <option>node2</option>
                <option>node5</option>
                <option>node9</option>
              </select>
            </div>
</div>
<div class="control-group">
<label class="control-label" for="inputWarning">Sensor</label>
	<div class="controls">
		<select id="select02">
                <option>press</option>
                <option>humi</option>
                <option>light</option>
              </select>
            </div>
</div>
<div class="control-group">
<label class="control-label" for="inputWarning">Time range</label>
	<div class="controls">
		<select id="select02">
                <option>24h</option>
                <option>48h</option>
                <option>week</option>
				<option>month</option>
				<option>3 months</option>
				<option>6 months</option>
				<option>year</option>
				<option>custom</option>
              </select>
            </div>
</div>
<div class="form-actions">
	<button type="submit" class="btn btn-primary">Send query</button>
	<button class="btn">Cancel</button>
</div>
</fieldset>
</form>

{% include 'footer_template.tpl' %}
