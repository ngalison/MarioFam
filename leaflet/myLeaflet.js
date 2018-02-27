alert('you aight!!');
var mymap = L.map('mapid').setView([47.655, -122.3035], 15);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWFyaW9mYW0iLCJhIjoiY2pkYXlkZXNhNmd1YzJxbjI3amk3YjcwMyJ9.myoE015mkCszlH0ahc7whA'
}).addTo(mymap);

var marker = L.marker([47.653739, -122.307744]).addTo(mymap)
function onMapClick(e) {
    marker.setLatLng(e.latlng);
    lat = marker.getLatLng().lat; 
	long = marker.getLatLng().lng;
	document.getElementById("latitude").innerHTML = lat;
	document.getElementById("longitude").innerHTML = long;
}
mymap.on('click', onMapClick);

var drumheller = new L.LatLng(47.653739, -122.307744);
//LatLng(47.653739, -122.307744)

//event handlers 
var lat = 0.0000;
var long = 0.0000;
var geoj = null;
(function() {
	window.onload = function() {
	//	document.getElementById("good").onclick = onButtonClick;
		document.getElementById("api").onclick = requestData;
	};

	/*function onButtonClick(){
		//alert(marker.getLatLng());
		lat = marker.getLatLng().lat; 
		long = marker.getLatLng().lng;
		document.getElementById("latitude").innerHTML = lat;
		document.getElementById("longitude").innerHTML = long;
	}*/

	function requestData(){
		var here = "https://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=vD7Q52EDZxdLcQBbn0LC&app_code=ccWrQE2jWI1y0H4ILI_ytg&waypoint0=" + lat + "%2C" + long + "&waypoint1=47.6631%2C-122.2982&mode=fastest%3Bpedestrian"
		const GoogleMaps = new Request(here);
		var url = "https://maps.googleapis.com/maps/api/directions/json?origin="+lat+","+long + "&destination=47.6631,-122.2982&mode=walking&key=AIzaSyBNxZzXxdDkyy6tBESUQ4Xc7_8_5Qv6Tt4"
		
		// url (required), options (optional)
		fetch(here, {
			method: 'get'
		}).then(function(response) {
			return response.json()
		}).then(function(returnedValue) {
			var coords = returnedValue.response.route[0].leg[0].maneuver;
			var lineStringList = [];
			for (var i = 0; i < coords.length; i++) {
				var coord = coords[i];
				lineStringList.push([coord.position.longitude, coord.position.latitude])
			}
			var geoJSON = {"type": "LineString", 
							"coordinates": lineStringList}
			if (geoj != null) {
				mymap.removeLayer(geoj)
			}
			geoj = L.geoJSON(geoJSON)
			geoj.addTo(mymap)
			//alert(JSON.stringify(geoJSON))
			//alert(JSON.stringify(coords.length))
		}).catch(function(err) {
			alert("error happened")
		});
	}

})();


