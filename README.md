## Worldwide-UFO-Sightings

![musk](images/musk.jpg)

## Overview
This website displays information about UFO sightings occurring in North America between the years 1906 and 2014. For each sighting, information was reported on the time and date, shape, duration, and location including the state, city, and geographical coordinates (latitude and longitude).

## Website Design

### Back End
The website runs on a Python Flask application. With the exception of the circle-packing visualization and the bar chart, visualizations were supplied with data from API calls to the SQLite database. The SQLite database was created from CSV files with the Python SQLite3 library after being munged with Python Pandas. In Flask, the database tables were queried with SQL Alchemy.

Below is a code snippet from the Flask file ('app.py').

                # creating a SQL Alchemy ORM
                engine = create_engine("sqlite:///database/database.sqlite")
                Base = automap_base()
                Base.prepare(engine, reflect=True)


                # table names
                ufo_data = Base.classes.ufo_data
                state_stats = Base.classes.state_stats
                merge_again = Base.classes.merge_again
                shape_counts = Base.classes.shape_counts

                app = Flask(__name__)

                ########D3 Visualization###########

                @app.route("/d3")
                def d3():
                return render_template('d3.html')


                @app.route("/d3data")
                def d3data():

                session = Session(engine)

                from flask import jsonify

                results = session.query(\
                merge_again.death_rate,\
                merge_again.population,\
                merge_again.state_sightings,\
                merge_again.smokes,\
                merge_again.fireball,\
                merge_again.light,\
                merge_again.triangle,\
                merge_again.state_abb).all()

                session.close()

                big_list = []

                for result in results:

                    obj = {
                        'death_rate': result[0],
                        'population': result[1],
                        'state_sightings': result[2],
                        'smokes': result[3],
                        'fireball': result[4],
                        'light': result[5],
                        'triangle': result[6],
                        'state_abb': result[7]
                    }
                    
                    big_list.append(obj)

                data=jsonify(big_list)

                return data


### Front End
Data from Flask API calls to the SQL database were sent to JavaScript files, which interacted with HTML and CSS files to produce visualizations. Each visualization was created using a JavaScript Leaflet or D3 library.

Below is a code snippet from the javascript file used to produce the scatterplot ('static/js/app.js') in conjunction with the corresponding html ('d3.html') and CSS files: 'static/css/d3style', 'static/css/d3style1', and 'static/css/d3style2.'

                // Retrieve data from the SQL database and execute everything below
                d3.json("http://127.0.0.1:5000/d3data").then(function(ufoData, err) {
                if (err) throw err;

                // parse data
                ufoData.forEach(function(data) {
                    data.death_rate = +data.death_rate;
                    data.population = +data.population;
                    // divide population by 100,000
                    data.state_sightings = +data.state_sightings;
                    data.smokes = +data.smokes;
                    // grab initial value for number of fireball sightings by state
                    data.fireball_adj = +data.fireball; 
                    // divide fireball sightings by number of residents per 100,000
                    data.fireball = +data.fireball_adj * 100000 / data.population;
                    data.light_adj = +data.light;
                    data.light = +data.light_adj * 100000 / data.population;
                    data.triangle_adj = +data.light;
                    data.triangle = +data.triangle_adj * 100000 / data.population;
                });

                // xLinearScale function above csv import
                var xLinearScale = xScale(ufoData, chosenXAxis);
                var yLinearScale = yScale(ufoData, chosenYAxis);


## Visualizations

A heatmap was created using JS Leaflet to display the locations of sightings throughout North America.

### Heatmap of Sighting Locations

![heat map](images/heat_map.jpg)


### Map of UFO Sightings and Drug Deaths

It was hypothesized that areas with heavier drug users would have more sightings. The JS Leaflet map below illustrates the relationship between the number of deaths from illicit substances reported for each state and the number of reported sightings in January and February of 2014.

![drug deaths](images/drug_deaths.png)


### Visualization of Word Assocations and UFO Shapes

Using R and D3, a visualization was created from comments from individuals reporting sightings. The interactive circle-packing map below shows associations between types of UFO shapes reported and phrases in the reported commentary. For example, individuals who reported seeing UFO shapes resembling fireballs were more likely to use descriptive words associated with light and heat such as *glowing*, *pulsating*, *orange*, etc.

![circle packing](images/circle_packing.png)

### Scatterplot of UFO Shapes and Drug Use

Other visualizations included a scatterplot illustrating the relationships between UFO shapes and drug deaths, and a barchart showing sighting shape frequencies by state. Both visualizations were created using JavaScript D3.

![scatter plot](images/scatter_plot.png)

### Barchart of Sighting Shape Frequencies by State

![barchart](images/bar_chart.png)


## Team Members

- B. Daves
- Eric Donnelly
- Shelly Fischer
- David Fried
- Chioma Maduko
- Gianni Adamo


## Rock on!

![bowie](images/bowie.jpg)
