from flask import Flask, render_template, redirect, jsonify, request
import pandas as pd
import datetime as dt
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


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


########Home Page###########

@app.route("/")
def welcome():
    return render_template('index.html')
    #return render_template('index.html', data=big_list)


########Heatmap###########

@app.route("/heatmap")
def heatmap():
    return render_template('heat.html')


@app.route('/heatmapdata')
def heatmapdata():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "latitude": result[0], "longitude": result[1]}
        big_list.append(obj)

    data=jsonify(big_list)
    
    return data


########Drug Deaths & UFO Sightings###########

@app.route("/drugs")
def drugs():
    return render_template('drugs.html')


@app.route('/drugsdata1')
def drugsdata1():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(state_stats.name, state_stats.sightings,\
    state_stats.drug_deaths).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "state_name": result[0], "state_sightings": result[1],\
            "state_drug_deaths": result[2]}
        big_list.append(obj)
    
    data=jsonify(big_list)
    
    return data

@app.route('/drugsdata2')
def drugsdata2():

    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude,\
        ufo_data.datetime, ufo_data.city, ufo_data.shape, ufo_data.comments,\
            ufo_data.duration_hours, ufo_data.year, ufo_data.month,\
                ).filter((ufo_data.year == 2014) & (ufo_data.month < 3))

    session.close()

    big_list = []

    for result in results:

        obj = {
            'latitude': result[0],
            'longitude': result[1],
            'datetime': result[2],
            'city': result[3],
            'shape': result[4],
            'comments': result[5],
            'duration_hours': result[6],
            'year': result[7],
            'month': result[8]
        }
        
        big_list.append(obj)

    data=jsonify(big_list)
    return data


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


########Circle Pack###########

@app.route("/circlepack")
def circlepack():
    return render_template('/circlepack.html')


########Bar Graph###########

@app.route("/bar")
def bar():
    return render_template('/bar.html')


@app.route("/bardata")
def bardata():
    
    session = Session(engine)

    from flask import jsonify

    results = session.query(
    shape_counts.State,
    shape_counts.Changing,
    shape_counts.Chevron,
    shape_counts.Cigar,
    shape_counts.Circle,
    shape_counts.Cone,
    shape_counts.Cross,
    shape_counts.Cylinder,
    shape_counts.Diamond,
    shape_counts.Disk,
    shape_counts.Egg,
    shape_counts.Fireball,
    shape_counts.Flash,
    shape_counts.Formation,
    shape_counts.Light,
    shape_counts.Other,
    shape_counts.Oval,
    shape_counts.Rectangle,
    shape_counts.Sphere,
    shape_counts.Teardrop,
    shape_counts.Triangle,
    shape_counts.Unknown).all()

    session.close()

    big_list = []

    for result in results:

        obj = {
        'State': result[0],
        'Changing': result[1],
        'Chevron': result[2],
        'Cigar': result[3],
        'Circle': result[4],
        'Cone': result[5],
        'Cross': result[6],
        'Cylinder': result[7], 
        'Diamond': result[8],
        'Disk': result[9],
        'Egg': result[10],
        'Fireball': result[11],
        'Flash': result[12],
        'Formation': result[13],
        'Light': result[14],
        'Other': result[15],
        'Oval': result[16],
        'Rectangle': result[17],
        'Sphere': result[18],
        'Teardrop': result[19],
        'Triangle': result[20],
        'Unknown': result[21]
        }
        
        big_list.append(obj)

    data=jsonify(big_list)
    
    return data


########Explore Data###########

@app.route("/explore")
def explore():
    return render_template('explore.html')


@app.route("/exploredata")
def exploredata():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(
        ufo_data.datetime,
        ufo_data.city,
        ufo_data.state,
        ufo_data.country,
        ufo_data.shape,
        ufo_data.duration,
        ufo_data.duration_hours,
        ufo_data.comments,
        ufo_data.date_posted,
        ufo_data.latitude,
        ufo_data.longitude,
        ufo_data.year,
        ufo_data.month)\
        .filter((ufo_data.year == 2014) & (ufo_data.month < 3)).all()

    session.close()

    data=jsonify(results)

    return data


if __name__ == '__main__':
    app.run(debug=True)