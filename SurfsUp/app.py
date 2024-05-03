# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas
import os


# Create engine
os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)


print(Base.classes.keys())
# #################################################
# # Database Setup
# #################################################
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# # Save references to each table
# Measurement = Base.classes.measurement
# Station = Base.classes.station

# # Create our session (link) from Python to the DB
# session = Session(engine)

# #################################################
# # Flask Setup
# #################################################
# app = Flask(__name__)



# #################################################
# # Flask Routes
# #################################################
# @app.route("/")
# def home():
#     return ("""
#     <h1>Climate Analysis API</h1>
#     <h2>Available Routes:</h2>
#     <ul>
#         <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
#         <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
#         <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
#         <li><a href="/api/v1.0/tstats">/api/v1.0/&lt;start&gt;</a></li>
#         <li><a href="/api/v1.0/tstats/">/api/v1.0/&lt;start&gt;/&lt;end&gt;</a></li>
#     </ul>
#     """)

# if __name__ == '__main__':
#     app.run(debug=True)