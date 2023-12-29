# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################
# Create the connection engine
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#1 Start at the homepage.
# List all the available routes.


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate App API <br/>"
        
        f"Here are all the available routes:<br/>"
        
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>(enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end>(enter as YYYY-MM-DD/YYYY-MM-DD)<br/>"
               )

#2 Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary 
# using date as the key and prcp as the value.

# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")

def precipitation():
        # create session link from python to the DB
        session = Session(engine)
        
        # most recent date
        most_recent_date =(session.query(Measurement.date)
             .order_by(Measurement.date.desc())
                .first())
        # one year date
        one_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

        # query results
        results = session.query(Measurement.date, Measurement.prcp).filter\
        (Measurement.date >= one_year_date).order_by(Measurement.date).all()
        
        # convert to dictionary
        prcp_dict = dict(results)
        
        return jsonify(prcp_dict)
        
# if __name__ == "__main__":
#     app.run(debug=True)


#3 Return a JSON list of stations from the dataset
#  elements of station table - station	name	latitude	longitude	elevation

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations data"""
    # Query all station data
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    query = session.query(*sel).all()

    session.close()

    # Create a dictionary from the row data and append 
    stations = []
    for station, name, latitude, longitude, elevation in query:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["lat"] = latitude
        station_dict["lon"] = longitude
        station_dict["elev"] = elevation
        
        stations.append(station_dict)

    return jsonify(stations)

#4 Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    query = session.query( Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281')\
    .filter(Measurement.date >= '2016-08-23').all()

    session.close()
    temp_obs = []
    for date, tobs in query:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        temp_obs.append(tobs_dict)

    return jsonify(temp_obs)


#5 Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or   start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

def start_temp(start):
     # Create our session (link) from Python to the DB
        
    session = Session(engine)
    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in query:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)









