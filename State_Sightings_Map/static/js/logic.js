//This code produces a map of states colored by the number of ufo sightings. Redder states have more sightings. California has the most sightings...not surprisingly...lol
// I used the documentation here as a guide (https://leafletjs.com/examples/choropleth/). I encourage you to visit that link and check it out.
// In the documentation I made it all the way until the section titled "Adding Interaction." I attempted to incorporate the code but couldn't get it to work. I think we should
//continue to try to add this code.

// I used json state coordinates data from this link (https://leafletjs.com/examples/choropleth/us-states.js), which is stored in the link as 'statesData.'
// Please visit the link and check out the json data.

//You'll notice my code is structured a little differently than the documentation because I had to wrap the statesData (json data) in the d3.csv() callback function
//in order to add in the sightings data contained in the state_sightings.csv file (located at 'static/data/state_sightings.csv').


var mapboxAccessToken = API_KEY;
var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=' + mapboxAccessToken, {
    id: 'mapbox/light-v9',
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
    tileSize: 512,
    zoomOffset: -1
}).addTo(map);


d3.csv('static/data/state_sightings.csv').then(function(data) { //states_sightings.csv is csv data that contains state ufo sightings

  data.forEach(state => {
   
    statesData.features.forEach(feature => { // the statesData is in json format in a url link in the index.html file: <script type="text/javascript" src="https://leafletjs.com/examples/choropleth/us-states.js"></script>
      // click the link to view the statesData: https://leafletjs.com/examples/choropleth/us-states.js
      
      if (state['State Names'] === feature.properties.name) {

        feature.properties['sightings'] = state['Sightings'] //here I'm adding a new property to the statesData json data that contains the ufo sightings
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
  
  L.geoJson(statesData, {style: style}).addTo(map)

});
