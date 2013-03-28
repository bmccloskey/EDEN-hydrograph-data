//snippet of stackoverflow -- avoids the reload from being fired multiple times during window resizing
var waitForFinalEvent = (function () {
  var timers = {};
  return function (callback, ms, uniqueId) {
    if (!uniqueId) {
      uniqueId = "Don't call this twice without a uniqueId";
    }
    if (timers[uniqueId]) {
      clearTimeout (timers[uniqueId]);
    }
    timers[uniqueId] = setTimeout(callback, ms);
  };
})();

$(document).ready(function() {
	$(window).resize(function() {
		waitForFinalEvent(function() {
			location.reload();
		}, 500, "ts_dygraph_id");
	});
});