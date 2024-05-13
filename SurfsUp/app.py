# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas
import os
import datetime as dt



# Create engine
os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


print(Base.classes.keys())
#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    return ("""
    <h1>Climate Analysis API</h1>
    <h2>Available Routes:</h2>
    <ul>
        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
        <li><a href="/api/v1.0/tstats">/api/v1.0/&lt;start&gt;</a></li>
        <li><a href="/api/v1.0/tstats/">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a></li>
    </ul>
    """)

@app.route('/api/v1.0/precipitation')
def precipitation():
    date = session.query(func.max(measurement.date)).scalar()
    oneyear = dt.datetime.strptime(date, "%Y-%m-%d") - dt.timedelta(days=365)
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= oneyear).all()

    precpdict = {}
    for date, prcp in precipitation:
        precpdict[date]=prcp
    return jsonify(precpdict)


@app.route('/api/v1.0/stations')
def stations():
    date = session.query(func.max(measurement.date)).scalar()
    oneyear = dt.datetime.strptime(date, "%Y-%m-%d") - dt.timedelta(days=365)
    stations = session.query(func.count(station.station)).scalar()
    activestations = session.query(measurement.station, func.count(measurement.id)).group_by(measurement.station).order_by(func.count(measurement.id).desc()).all()
    mostactive = activestations[0][0]
    lowtemp = session.query(func.min(measurement.tobs)).filter(measurement.station == mostactive).scalar()
    hightemp = session.query(func.max(measurement.tobs)).filter(measurement.station == mostactive).scalar()
    avgtemp = session.query(func.avg(measurement.tobs)).filter(measurement.station == mostactive).scalar()
    totaltemperatures = session.query(measurement.tobs).filter(measurement.station == mostactive).filter(measurement.date >= oneyear).all()
    temperatures = [temp[0] for temp in totaltemperatures]  
    return jsonify(temperatures)

@app.route('/api/v1.0/tobs')
def tobs():
    date = session.query(func.max(measurement.date)).scalar()
    oneyear = dt.datetime.strptime(date, "%Y-%m-%d") - dt.timedelta(days=365)
    mostactive = session.query(measurement.station, func.count(measurement.station))\
                        .group_by(measurement.station)\
                        .order_by(func.count(measurement.station).desc())\
                        .first()[0]
    totaltemperatures = session.query(measurement.date, measurement.tobs)\
                               .filter(measurement.date >= oneyear)\
                               .filter(measurement.station == mostactive)\
                               .all()
    temperaturedict = {date: tobs for date, tobs in totaltemperatures}

    return jsonify(temperaturedict)


@app.route('/api/v1.0/<start>')
def start(start):
    date = session.query(func.max(measurement.date)).scalar()
    oneyear = dt.datetime.strptime(date, "%Y-%m-%d") - dt.timedelta(days=365)
    temperaturestats = session.query(func.min(measurement.tobs), 
                                      func.max(measurement.tobs), 
                                      func.avg(measurement.tobs))\
                               .all()
    mintemp, maxtemp, avgtemp = temperaturestats[0]

    stats = {
        "Start Date": start,
        "Minimum Temperature": mintemp,
        "Maximum Temperature": maxtemp,
        "Average Temperature": avgtemp
    }

    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)

