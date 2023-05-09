# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine)

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
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query database to return date and prcp within the date range
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    
    # Create an empty list to hold the results
    all_precip = []

    # Loop through the results
    for date, prcp in results:
        # Convert the data to a dictionary
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['prcp'] = prcp

        # Append the dictionary to the list
        all_precip.append(precip_dict)

    # Return the list of dictionary results in JSON format
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Query the database for all station data
    stations = session.query(Station)

    # Create an empty list to hold the results
    all_stations = []

    # Loop through the results
    for station in stations:
        # Convert the data to a dictionary
        station_dict = {}
        station_dict['station'] = station.station
        station_dict['name'] = station.name
        station_dict['latitude'] = station.latitude
        station_dict['longitude'] = station.longitude
        station_dict['elevation'] = station.elevation

        # Append the dictionary to the list
        all_stations.append(station_dict)

    # Return the list of dictionary results in JSON format
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query the database for date and tobs data from the 'USC00519281' station within the date range
    station_temps = session.query(Measurement.date, Measurement.tobs).\
                            filter(Measurement.date >= '2016-08-23').\
                            filter(Measurement.station == 'USC00519281').\
                            all()
    
    # Create an empty list to hold the results
    all_tobs = []

    # Loop through the results
    for date, temp in station_temps:
        # Convert the data to a dictionary
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = temp

        # Append the dictionary to the list
        all_tobs.append(tobs_dict)

    # Return the list of dictionary results in JSON format
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
# @app.route("/api/v1.0/<start>/<end>")
def date_range(start):
    # Convert date string to date object
    date_list = start.split("-")
    start_date = dt.date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
    # Query the database for min, max, and avg temps starting at the provided start date
    results = session.query(func.min(Measurement.tobs),
                            func.max(Measurement.tobs),
                            func.avg(Measurement.tobs)
                            ).\
                            filter(Measurement.date >= start_date).\
                            all()[0]

    temp_dict = {
        "min": results[0],
        "max": results[1],
        "avg": results[2]
    }

    return jsonify(temp_dict)
    

if __name__ == '__main__':
    app.run(debug=True)