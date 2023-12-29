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
       f"Welcome to the Hawaii Climate app API<br/>"
        f"Here are all the Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>(enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end>(enter as YYYY-MM-DD/YYYY-MM-DD)<br/>")
        
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
        
if __name__ == "__main__":
    app.run(debug=True)






