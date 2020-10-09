## Important: 

1. To get the map to work you need to first update the config.js file located at static/js/config.js with your API Key. This is the same key you used for all of the class leaflet exercises.

2. You then need to run python -m http.server in this directory and vist you localhost:800 in your webbrowser.


## Note: 

I did not used the us_states.json files. For whatever reason, this file is difficult to run for me. It might not have been created correctly by the author.

Instead I used json data containing states coordinates at https://leafletjs.com/examples/choropleth/us-states.js.

I retrieved the sightings from the state_sightings.csv located in static/data/state_sightings.csv.

I found this leaflet documentation helpful for creating the map (https://leafletjs.com/examples/choropleth/).