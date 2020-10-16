// // the states data is a url link represented in the following section of the index.html file:
// {/* <script type="text/javascript" src="https://leafletjs.com/examples/choropleth/us-states.js"></script> */}
// the variable in the above url is titled 'statesData.'




var mapboxAccessToken = API_KEY;
var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    id: 'mapbox/light-v9',
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    tileSize: 512,
    zoomOffset: -1
}).addTo(map);


d3.csv('static/data/state_sightings.csv').then(function(data) {

  data.forEach(state => {
   
    statesData.features.forEach(feature => {
      
      if (state['State Names'] === feature.properties.name) {

        feature.properties['sightings'] = state['Sightings']
      }

    })
    
  })

  L.geoJson(statesData).addTo(map);

  function getColor(d) {
    return d > 5655 ? '#800026' :
           d > 4696 ? '#BD0026' :
           d > 3737 ? '#E31A1C' :
           d > 2778 ? '#FC4E2A' :
           d > 1819 ? '#FD8D3C' :
           d > 860  ? '#FEB24C' :
           d > 380  ? '#FED976' :
                      '#FFEDA0';
  };
  
  function style(feature) {
    return {
        fillColor: getColor(feature.properties.sightings),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
  }
  
  L.geoJson(statesData, {style: style}).addTo(map);


});


// Additional code for reference - ignore this

// // var mymap = L.map('map').setView([51.505, -0.09], 13);

// // L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
// //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
// //     maxZoom: 18,
// //     id: 'mapbox/satellite-v9', //mapbox/streets-v11
// //     tileSize: 512,
// //     zoomOffset: -1,
// //     accessToken: API_KEY
// // }).addTo(mymap);


// // //adding a marker

// // var marker = L.marker([51.5, -0.09]).addTo(mymap);

// // //shapes

// // var circle = L.circle([51.508, -0.11], {
// //   color: 'red',
// //   fillColor: '#f03',
// //   fillOpacity: 0.5,
// //   radius: 500
// // }).addTo(mymap);


// // var polygon = L.polygon([
// //   [51.509, -0.08],
// //   [51.503, -0.06],
// //   [51.51, -0.047]
// // ]).addTo(mymap);

// // // adding a popup

// // //bind the circle and polygon markers
// // marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();
// // circle.bindPopup("I am a circle.");
// // polygon.bindPopup("I am a polygon.");

// // //bind to shapes
// // var popup = L.popup()
// //     .setLatLng([51.5, -0.09])
// //     .setContent("I am a standalone popup.")
// //     .openOn(mymap);


// // //adding events

// // //Every time something happens in Leaflet, e.g. user clicks on a marker or map zoom changes,
// // //the corresponding object sends an event which you can subscribe to with a function. It allows you to react to user interaction:
// // //   function onMapClick(e) {
// // //     alert("Fuck off and die at " + e.latlng);
// // // }

// // // mymap.on('click', onMapClick);



// // //Each object has its own set of events — see documentation for details.
// // // The first argument of the listener function is an event object —
// // // it contains useful information about the event that happened.
// // // For example, map click event object (e in the example above) has latlng property which is a location at which the click occurred.

// // // Let’s improve our example by using a popup instead of an alert:


// // var popup = L.popup();

// // function onMapClick(e) {
// //     popup
// //         .setLatLng(e.latlng)
// //         .setContent("Fuck off and die at " + e.latlng.toString())
// //         .openOn(mymap);
// // }

// // mymap.on('click', onMapClick);