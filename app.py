#################################################
# import dependencies 
#################################################

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Flask (Server)
from flask import Flask, jsonify, render_template, request, flash, redirect

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Database Setup:sqlite
#################################################
#from flask_sqlalchemy import SQLAlchemy
# The database URI
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/belly_button_biodiversity.sqlite"

#db = SQLAlchemy(app)




engine = create_engine("sqlite:///db/la_colission.sqlite")
    
    
Base = automap_base()               # reflect an existing database into a new model    
Base.prepare(engine, reflect=True)  # reflect the tables
Base.classes.keys()                 # Save reference to the table
conn = engine.connect()
LA_collisions= Base.classes.collision


session = Session(engine)# Create our session (link) from Python to the DB





#################################################
# Flask Routes
#################################################

@app.route("/")
def default():

    return render_template("index.html")


@app.route("/names")
def names():
   # """Return a list of sample names."""

    stmt = session.query(LA_collisions).statement
    df = pd.read_sql_query(stmt, session.bind)
    df.set_index('id', inplace=True)

    # Returning list of the column names (sample names)
    return jsonify(list(df.columns))
    


@app.route('/area')
def area():
#"""List of Neighborhoods."""

    hood_N_req = session.query(LA_collisions.area).all()
    hood_names = list(np.ravel(hood_N_req))
    return jsonify(hood_names)

@app.route('/data')
def data():
    sel = [LA_collisions.id, LA_collisions.age,
           LA_collisions.sex, LA_collisions.area,
           LA_collisions.descent, LA_collisions.date,
           LA_collisions.day_of_week, LA_collisions.time,
           LA_collisions.location, LA_collisions.geojson
           ]
    results = session.query(*sel).all()
    

    # Create a dictionary entry for each row of metadata information
    collisions = []
    for result in results:
        collisions.append({
            "ID": result[0],
            "Age": result[1],
            "Gender" : result[2],
            "Area" : result[3],
            "Ethnicity" : result[4],
            "Date of Incident" : result[5],
            "Day of Incident" : result[6],
            "Time of Incident" : result[7],
            "Lat:Lon": result[9]
        })

    return jsonify(collisions)

@app.route('/time')
def time():
    sel = [LA_collisions.id, LA_collisions.age,
           LA_collisions.sex, LA_collisions.area,
           LA_collisions.descent, LA_collisions.date,
           LA_collisions.day_of_week, LA_collisions.time,
           LA_collisions.location, LA_collisions.geojson
           ]
    results = session.query(*sel).all()
    

    # Create a dictionary entry for each row of metadata information
    collisions = []
    for result in results:
        collisions.append({
            "ID": result[0],
            #"Age": result[1],
            #"Gender" : result[2],
            "Area" : result[3],
            #"Ethnicity" : result[4],
            "Date of Incident" : result[5],
            "Day of Incident" : result[6],
            "Time of Incident" : result[7],
           # "Lat:Lon": result[9]
        })

    return jsonify(collisions)



    # # Create a dictionary entry for each row of data information
    # all_collisions = []
    # for collision in results:
    #     collision_dict = {}       
    #     collision_dict["ID"]: LA_collisions.id
    #     collision_dict["Age"]: LA_collisions.age
    #     collision_dict["Gender"] : LA_collisions.sex
    #     collision_dict["Area"] : LA_collisions.area
    #     collision_dict["Ethnicity"] : LA_collisions.descent
    #     collision_dict["Date of Incident"] : LA_collisions.date
    #     collision_dict["Day of Incident"] : LA_collisions.day_of_week
    #     collision_dict["Time of Incident"] :LA_collisions.time
    #     collision_dict["Location"] : LA_collisions.location
    #     collision_dict["Lat:Lon"] :LA_collisions.geojson
    #     collision_dict["crossstreet"] :LA_collisions.reporting_district
    #     all_collisions.append(collision_dict)
 
    # return jsonify(all_collisions)






if __name__ == '__main__':
    app.run(debug=True)
