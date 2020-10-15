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

# tables are ufo_data and state_stats
engine = create_engine("sqlite:///../database/database.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# should print table names
print(Base.classes.keys())

# references to each table
ufo_data = Base.classes.ufo_data
state_stats = Base.classes.state_stats

app = Flask(__name__)

# When user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h3>Available Routes:<h/><br/>"
        f"/api/v1.0/sightings<br/>"
        f"/api/v1.0/states<br/>"
        # f"/api/v1.0/cities<br/>"
        # f"/api/v1.0/[start_year]<br/>"
        # f"/api/v1.0/[start_year]/[end_year]"
    )

@app.route("/api/v1.0/sightings")
def sightings():
  
    session = Session(engine)

    from flask import jsonify

    results = session.query(ufo_data.datetime, ufo_data.state, ufo_data.city, ufo_data.shape, ufo_data.duration, ufo_data.comments).order_by(ufo_data.state.asc()).all()

    session.close()

    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = { "state": result[1], "city": result[2], "sighting_shape": result[3], "sighting_duration": result[4], "comments": result[5]}
        big_list.append(dresults)
    
    return jsonify(big_list)

@app.route("/api/v1.0/states")
def states():

    session = Session(engine)

    results = session.query(state_stats.name, state_stats.drug_deaths, state_stats.sightings, state_stats.avg_sighting_duration).all()
    
    session.close()
    
    big_list = []
    for result in results:
        dresults = {}
        dresults[result[0]] = {'drug_deaths': result[1], 'ufo_sightings': result[2], 'average_sighting_duration': result[3]}
        big_list.append(dresults)
    
    return jsonify(big_list)


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