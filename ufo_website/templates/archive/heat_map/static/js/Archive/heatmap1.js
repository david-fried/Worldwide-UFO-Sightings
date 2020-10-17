//This code produces a map of states colored by the number of drug deaths. Redder states have more drug deaths.

//I would like to overlay markers of ufo sightings. Am having a hard time getting this to work.


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
  "Dark": darkmap,
  };
  

// Create our map, giving it the streetmap and earthquakes layers to display on load
var myMap = L.map("map", {
    center: [ 37.09, -95.71 ],
    zoom: 4,
    layers: [streetmap]     //default selected layer
    });

streetmap.addTo(myMap);

// create layer; attach data later on
var drugDeaths = new L.LayerGroup();
var sightings = new L.LayerGroup();


// Create overlay object to hold our overlay layer
var overlayMaps = {
  "Ufo Sightings": sightings
};

// Create a layer control
// Pass in baseMaps and overlayMaps
L.control.layers(baseMaps, overlayMaps, {
  collapsed: false
}).addTo(myMap);

  // //sightingsColor
  // function getColor(d) {
  //   return d > 5655 ? '#800026' :
  //           d > 4696 ? '#BD0026' :
  //           d > 3737 ? '#E31A1C' :
  //           d > 2778 ? '#FC4E2A' :
  //           d > 1819 ? '#FD8D3C' :
  //           d > 860  ? '#FEB24C' :
  //           d > 380  ? '#FED976' :
  //                     '#FFEDA0';
  // };
  

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

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(myMap);



var ImportedData = "static/data/ufo_data.csv";

d3.csv(ImportedData, function(data) {

  var heatArray = [];

  for (var i = 0; i < data.length; i++) {

    var latitude = parseFloat(data[i].latitude);
    var longitude = parseFloat(data[i].longitude);

      heatArray.push([latitude, longitude]);
    }

  var heat = L.heatLayer(heatArray, {
    radius: 75,
    blur: 35
  }).addTo(myMap);

});




  
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





  L.geoJson(statesData.features, {
    style: style}).addTo(myMap);

});
