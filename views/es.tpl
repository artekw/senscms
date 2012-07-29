{% include 'header_template.tpl' %}
<div class="page-header">
	<h2>{{title}}</h2>
</div>
<div class="well">
Strona odświeża się automatycznie. <br />
Nie działa z wszystkim przeglądarkami np. IE, Chrome.
</div>
<div id="es"></div>

<table cellpadding="0" cellspacing="0" border="0" class="table table-striped table-bordered" id="ntable">
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

{% include 'footer_template.tpl' %}
