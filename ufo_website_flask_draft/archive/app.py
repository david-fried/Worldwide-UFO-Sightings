from flask import Flask, render_template, redirect, jsonify, request
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from scipy.stats import ttest_ind
import sqlite3

# Creating a SQL Alchemy ORM
engine = create_engine("sqlite:///database/database.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# table names
ufo_data = Base.classes.ufo_data
state_stats = Base.classes.state_stats

# should print table names
print(Base.classes.keys())

app = Flask(__name__)

@app.route("/")
def welcome():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "latitude": result[0], "longitude": result[1]}
        big_list.append(obj)
    
    # #debug
    # print(big_list[0:10])
    
    return render_template('index.html', data=big_list)


@app.route("/heatmap")
def heatmap():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.latitude, ufo_data.longitude).all()

    session.close()

    big_list = []
    for result in results:
        obj = { "latitude": result[0], "longitude": result[1]}
        big_list.append(obj)
    
    # #debug
    # print(big_list[0:10])

    
    return render_template('heat.html', data=big_list)


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
    
    # #debug
    # print(big_list[0:10])

    data=jsonify(big_list)
    
    return data

@app.route("/drugs")
def drugs():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    return render_template('drugs.html', data=big_list)


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
    
    # #debug
    # print(big_list[0:10])

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
    
    # #debug
    # print(big_list[0:10])
    # print(len(big_list))

    data=jsonify(big_list)
    return data


@app.route("/d3")
def d3():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    return render_template('d3.html', data=big_list)


@app.route("/explore")
def explore():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    # return jsonify(big_list)
    return render_template('explore.html', data=big_list)


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

    # big_list = []

    # for result in results:

    #     obj = {
    #         'datetime': result[0],
    #         'city': result[1],
    #         'state': result[2],
    #         'country': result[3],
    #         'shape': result[4],
    #         'duration': result[5],
    #         'duration_hours': result[6],
    #         'comments': result[7],
    #         'date_posted': result[8],
    #         'latitude': result[9],
    #         'longitude': result[10],
    #         'year': result[11],
    #         'month': result[12],
    #     }
        
    #     big_list.append(obj)
    
    # #debug
    # print(big_list[0:10])
    # print(len(big_list))
    print(results[0:10])

    data=jsonify(results)
    return data


if __name__ == '__main__':
    app.run(debug=True)



# @app.route("/api/v1.0/<start_year>")
# def start_year():

#     session = Session(engine)

#     from flask import jsonify

#     results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments, ufo_data.year).order_by(ufo_data.state.asc()).all()

#     session.close()

#     big_list = []
#     for result in results:
#         dresults = {}
#         if result[6] >= start_year:
#             dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
#             big_list.append(dresults)
    
#     return jsonify(big_list)




# @app.route("/api/v1.0/<start_year>/<end_year>")




# @app.route("/api/v1.0/<start>")
# def start_date(start):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Arg:
#         start_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
#     session = Session(engine)
#     ordered_dates = session.query(Measurement.date).order_by(Measurement.date.asc()).all()
#     first_date = dt.datetime.strptime(ordered_dates[0][0], '%Y-%m-%d').date()
#     last_date = dt.datetime.strptime(ordered_dates[-1][0], '%Y-%m-%d').date()

#     try:
#         dt.datetime.strptime(start, '%Y-%m-%d').date()
#         start = dt.datetime.strptime(start, '%Y-%m-%d').date()
#         if start >= first_date and start <= last_date:
#             results = session.query(func.min(Measurement.cities), func.avg(Measurement.cities),\
#             func.max(Measurement.cities)).filter((Measurement.date >= start) & \
#             (Measurement.date <= last_date)).all()
#             session.close()
#             results = list(results)
#             return jsonify(results[0])
#         else:
#             return f"Please enter a date between {first_date} and {last_date}."
#     except ValueError:
#         return jsonify({"error": f"Your response, {start}, was not formatted correctly"}), 404

# @app.route("/api/v1.0/<start>/<end>")
# def date_range(start, end):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
#     session = Session(engine)
#     ordered_dates = session.query(Measurement.date).order_by(Measurement.date.asc()).all()
#     first_date = dt.datetime.strptime(ordered_dates[0][0], '%Y-%m-%d').date()
#     last_date = dt.datetime.strptime(ordered_dates[-1][0], '%Y-%m-%d').date()

#     try:
#         dt.datetime.strptime(start, '%Y-%m-%d').date() and dt.datetime.strptime(end, '%Y-%m-%d').date()
#         start = dt.datetime.strptime(start, '%Y-%m-%d').date()
#         end = dt.datetime.strptime(end, '%Y-%m-%d').date()
#         if (start >= first_date and start <= last_date) and \
#             (end >= first_date and end <= last_date):
#             results = session.query(func.min(Measurement.cities), func.avg(Measurement.cities),\
#             func.max(Measurement.cities)).filter(Measurement.date >= start).filter\
#             (Measurement.date <= end).all()
#             session.close()
#             results = list(results)
#             return jsonify(results[0])
#         else:
#             return f"Please enter dates between {first_date} and {last_date}."
#     except ValueError:
#         return jsonify({"error": f"Your responses, {start} and {end}, were not formatted correctly"}), 404