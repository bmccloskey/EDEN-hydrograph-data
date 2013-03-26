/*
$(document).ready(function() {
	var graph_div = $("div.dygraph_plot").html();
	$(window).resize(function () {
		$("div.dygraph_plot").html(graph_div);
	});
});

/*
$(window).resize(function() {
	var graph_div = $("div.dygraph_plot").html();
	$("div.dygraph_plot").html(graph_div);
});
*/

$(window).resize(function() {
	location.reload();
});
