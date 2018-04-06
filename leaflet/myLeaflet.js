alert('you aight!!');
var mymap = L.map('mapid').setView([47.655, -122.3035], 15);
L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1IjoibWFyaW9mYW0iLCJhIjoiY2pkYXlkZXNhNmd1YzJxbjI3amk3YjcwMyJ9.myoE015mkCszlH0ahc7whA'
}).addTo(mymap);

var marker = L.marker([47.653739, -122.307744]).addTo(mymap)
//event handlers 
var lat = 47.653739;
var long = -122.307744;
var geoj = null;
var polyline = null;

function onMapClick(e) {
    marker.setLatLng(e.latlng);
    lat = marker.getLatLng().lat; 
	long = marker.getLatLng().lng;
	//document.getElementById("latitude").innerHTML = lat;
	//document.getElementById("longitude").innerHTML = long;
}
mymap.on('click', onMapClick);

var drumheller = new L.LatLng(47.653739, -122.307744);
//LatLng(47.653739, -122.307744)

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

	function dist(coord1, coord2) {
		return Math.sqrt(Math.pow(coord1[0] - coord2[0], 2) + Math.pow(coord1[1] - coord2[1], 2))
	}

	function requestData(){
		walkDist = document.getElementById("input").value;
		if (isNaN(parseFloat(walkDist))) {
			alert("Invalid walking distance. Please enter a number.")
			return;
		}
		var localserver = "https://35.192.10.218/Project/selectpaths/" + long + "/" + lat + "/" + walkDist
		console.log(localserver)
		//const GoogleMaps = new Request(here);		
		// url (required), options (optional)

		// Request from our own local server for a walking path
		fetch(localserver, {
			method: 'get'
		}).then(function(response) {
			return response.json();
		}).then(function(returnedValue) {
			var walkcoords = returnedValue.features[0].geometry.coordinates;
			if (polyline != null) {
				mymap.removeLayer(polyline);
			}
			polyline = L.polyline(walkcoords, {color: 'red'}).addTo(mymap);

			// Request to here api AFTER we know where we're going
			var srcCoord = [lat, long];
			var destCoord1 = walkcoords[0];
			var destCoord2 = walkcoords[walkcoords.length - 1];

			var destCoord;
			if (dist(srcCoord, destCoord1) < dist(srcCoord, destCoord2)) {
				destCoord = destCoord1;
			} else {
				destCoord = destCoord2;
			}
			alert(destCoord)
			
			var here = "https://route.cit.api.here.com/routing/7.2/calculateroute.json?app_id=vD7Q52EDZxdLcQBbn0LC&app_code=ccWrQE2jWI1y0H4ILI_ytg&waypoint0=" 
						+ lat + "%2C" + long + "&waypoint1=" + destCoord[0] + "%2C" + destCoord[1] + "&mode=fastest%3Bpedestrian"

			// NESTED FETCH CHAOS
			// Request from the here api to get a path to that location
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

		}).catch(function(err) {
			alert(err);
		});
	}

})();


