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
}
mymap.on('click', onMapClick);

var drumheller = new L.LatLng(47.653739, -122.307744);
//LatLng(47.653739, -122.307744)

//event handlers 
var lat = 0.0000;
var long = 0.0000;
(function() {
	window.onload = function() {
		document.getElementById("good").onclick = onButtonClick;
	};

	function onButtonClick(){
		alert(marker.getLatLng());
		lat = marker.getLatLng().lat; 
		long = marker.getLatLng().lng;
		alert(lat);
		alert(long);
	}
})();

const GoogleMaps = new Request(https://maps.googleapis.com/maps/api/directions/json?origin=47.6553,-122.3035&destination=47.6631, -122.2982&mode=walking&key=AIzaSyBNxZzXxdDkyy6tBESUQ4Xc7_8_5Qv6Tt4);
