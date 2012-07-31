if(typeof(Hit) == "undefined"){
	Hit = {};
}
(function(Hit){
	if(typeof(Hit.Model) == "undefined"){
		Hit.Model = {};
	}
	if(typeof(Hit.Collection) == "undefined"){
		Hit.Collection = {};
	}
	$(document)
	.bind(
			'pageinit',
			function(e, ui) {
				if (e.target.id == "page_home") {
					var map = Hit.map = L.map('map').locate({
						setView : true,
						maxZoom : 13
					});
					L
							.tileLayer(
									'http://{s}.tiles.mapbox.com/v3/mapbox.mapbox-streets/{z}/{x}/{y}.png',
									{
										attribution : '',
										maxZoom : 18
									}).addTo(map);
					function onLocationError(e) {
						alert(e.message);
					}
					map.on('locationerror', onLocationError);
				}
			})
})(Hit)
