# 1. import Flask
from flask import Flask, jsonify
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
#Base.classes.keys()

measurements = Base.classes.measurement
stations = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return (
        f"<b>Home Page for climate analysis</b>"
        "<br />"
        "Select a route by clicking the link<br />"
        "<br />"
        "<a href='/api/v1.0/precipitation' >Precipitation (/api/v1.0/precipitation)</a><br />"
        "<a href='/api/v1.0/stations' >Stations (/api/v1.0/stations)</a><br />"
        "<a href='/api/v1.0/tobs' >Tempertures (/api/v1.0/tobs)</a><br />"
        "<a href='/api/v1.0/start' >Enter start date in URL (/api/v1.0/start)</a><br />"
        "<a href='/api/v1.0/startAndEnd' >Enter start and end date in URL (/api/v1.0/startAndEnd)</a><br />"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date one year from the last date in data set.
    lastYearDate = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurements.date, measurements.prcp).filter(measurements.date >= lastYearDate).all()

    session.close()

    # create dictionary object
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)
 
# Stations route
@app.route("/api/v1.0/stations")
def station():
    # Perform a query to retrieve the data and precipitation scores
    results2 = session.query(stations.station).all() 
    session.close()

    stationsList = list(np.ravel(results2))

    # Return JSON
    return jsonify(stationsList)

# Get all temps route
@app.route("/api/v1.0/tobs")
def tobs():
    # Calculate the date one year from the last date in data set.
    lastYearDate = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Perform a query to retrieve all tempertuate for most active stations for past year
    temps = session.query(measurements.date, measurements.tobs).\
        filter(measurements.station == 'USC00519281', measurements.date >= lastYearDate).all() 
    session.close()

    tempList = list(np.ravel(temps))

    # Return JSON
    return jsonify(tempList)


# Get temperture for given range
@app.route("/api/v1.0/<start>")
def dateStatStart(start:None):
    # Convert date that user entererd
    startDate = dt.datetime.strptime(start, '%m%d%y')

    # Perform a query to retrieve all tempertuate for given date
    temps =session.query(func.max(measurements.tobs), func.avg(measurements.tobs), func.min(measurements.tobs)).\
        filter(measurements.date > startDate).all() 
    session.close()

    tempList = list(np.ravel(temps))

    # Return JSON
    return jsonify(tempList)

# Get temperture for given range
@app.route("/api/v1.0/<start>/<end>")
def dateStatStartEnd(start:None, end:None):
    # Convert date that user entererd
    startDate = dt.datetime.strptime(start, '%m%d%y')
    endDate = dt.datetime.strptime(end, '%m%d%y')


    # Perform a query to retrieve all tempertuate for given date
    temps =session.query(func.max(measurements.tobs), func.avg(measurements.tobs), func.min(measurements.tobs)).\
        filter(measurements.date > startDate, measurements.date < endDate).all() 
    session.close()

    tempList = list(np.ravel(temps))

    # Return JSON
    return jsonify(tempList)


if __name__ == "__main__":
    app.run(debug=True)
