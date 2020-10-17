//This code produces a map of states colored by the number of drug deaths in 2018. States that are more red have more drug deaths.

//The map overlays markers of 1,000 UFO sightings. (The original file had over 80,000 sightings.)


var mapboxAccessToken = API_KEY;

function popUpMsg(feature, layer) {
  layer.bindPopup("<h3>" + feature.properties.drugdeaths + "</h3>");
};


var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 5,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
});

var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 5,
  id: "dark-v10",
  accessToken: API_KEY
});


// Define a baseMaps object to hold our base layers
var baseMaps = {
  "Street": streetmap,
  "Dark": darkmap
  };
  

// Create our map, giving it the streetmap and earthquakes layers to display on load
var myMap = L.map("map", {
    center: [ 37.09, -95.71 ],
    zoom: 5,
    layers: [streetmap]     //default selected layer
    });

streetmap.addTo(myMap);

// create layer; attach data later on
var drugDeaths = new L.LayerGroup();
var sightings = new L.LayerGroup();


// Create overlay object to hold our overlay layer
var overlayMaps = {
  "UFO Sightings": sightings
};

// Create a layer control
// Pass in baseMaps and overlayMaps
L.control.layers(baseMaps, overlayMaps, {
  collapsed: false
}).addTo(myMap);



  //Drug Deaths Color
  function getColor(d) {
    return d > 2400 ? '#BD0026' :
            d > 1200 ? '#FC4E2A'  :
            d > 600? '#FD8D3C':
            d > 300 ? '#FEB24C' :
                      '#FFEDA0';
  };
  
  
    function style(feature) {
      return {
          fillColor: getColor(feature.properties.drugdeaths),
          weight: 2,
          opacity: 1,
          color: 'white',
          dashArray: '3',
          fillOpacity: 0.7
      };
    };

    // Create a legend
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 300, 600, 1200, 2400],
        labels = [];

    div.innerHTML += '<b>Deaths from Illicit Drugs</b><br>'

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(myMap);


  
d3.csv('static/data/state_stats.csv').then(function(data) { //states_sightings.csv is csv data that contains state ufo sightings

  data.forEach(state => {
   
    statesData.features.forEach(feature => { // the statesData is in json format in a url link in the index.html file: <script type="text/javascript" src="https://leafletjs.com/examples/choropleth/us-states.js"></script>
      // click the link to view the statesData: https://leafletjs.com/examples/choropleth/us-states.js
      
      if (state['State Name'] === feature.properties.name) {

        //add state sightings to state json data
        feature.properties['sightings'] = state['State Sightings']
        
        //add state drug deaths to state json data
        feature.properties['drugdeaths'] = state['Drug Deaths']
        
        // console.log(feature.properties.drugdeaths);
        // console.log(feature.properties);


      }

    });
    
  });

  d3.csv('static/data/ufo_data1_2_2014.csv').then(function(data) { 

    data.forEach(data => {
  
  // for (var i = 0; i < data.length; i++) {
  
  // for (i=0; i<ud.length; i++) {
      var lat = parseFloat(data['latitude']);
      var long = parseFloat(data['longitude']);
      console.log(lat, long);
      var location = [lat, long];
      var marker = L.marker(location);
      marker.addTo(sightings).bindPopup(
        "<p>" + new Date(data.datetime) + "</p><hr>" +
        "<p><strong>City:</strong> " + data.city + "</p>" +
        "<p><strong>Shape:</strong> " + data.shape + "</p>" +
        "<p><strong>Event:</strong> " + data.comments + "</p>" +
        "<p><strong>Duration:</strong> " + data[`duration (hours/min)`] + "</p>"
        );

      sightings.addTo(myMap);
    
    });
    
  });



  L.geoJson(statesData.features, {
    style: style}).addTo(myMap);

});


