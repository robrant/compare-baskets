
import os
import sys
import logging
from pymongo import Connection
import json
import random

from flask import Flask, render_template, jsonify
#from flask.ext.socketio import SocketIO, emit

# Ensure the tracking-level directory is on the path. Then use . package notation and __init__ files.
this_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if this_dir not in sys.path:
    sys.path.append(this_dir)

# Basic lagging configuration
logging.basicConfig(format='%(levelname)s:\t%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask App configuration
app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'secret!'
#socketio = SocketIO(app)

import mdb

c, dbh = mdb.getHandle(host = 'localhost',
                       port     = 27017,
                       db       = 'mydb')

collHandle = dbh['tescodata']

# Load the county geojson
#f = open('/Users/robrant/eclipseCode/compare-baskets/geo_app/data/counties_districts_boroughs.geojson', 'r')
f = open('/Users/dusted-ipro/Documents/LiClipse Workspace/compare-baskets/geo_app/data/counties_districts_boroughs.geojson', 'r')
county_gj = json.loads(f.read())

# ----------------------------------------------------------------------------------------

def update_progress(socketio, progress, event_type='progress_update', namespace='/test'):
    """ Reports progress via a log and emit via socketio """



    if not socketio:
        logger.info('%s :\t %s'%(progress['data']['key'], progress['data']['value']))
    else:
        # Pass a list of progress info through
        if isinstance(progress['data'], list):
            socketio.emit(event_type, progress, namespace=namespace)
        else:
            logger.info('%s :\t %s'%(progress['data']['key'], progress['data']['value']))
            socketio.emit(event_type, progress, namespace=namespace)


# -----------------------------------------------------------------------------

def get_geojson(county_name, score):
    """ Merge geojson with the scores """

    county_out = {'geometry':{},
                  'type':'',
                  'properties':{}}

    for county in county_gj['features']:
        if county['properties']['NAME_2'].lower() == county_name.lower():

            county_out['properties']['name'] = county['properties']['NAME_2']
            county_out['properties']['score'] = score
            county_out['geometry'] = county['geometry']
            county_out['type'] = county['type']
            return county_out
        else:
            return None



# -----------------------------------------------------------------------------


@app.route('/')
def index():
    """ normal http request to a serve up the page """

    print 'hello'
    leaderboard_flds = ["name", "score"]

    aggregation = [{"$group" :
                                {"_id" : {"borough" : "$BOROUGH"},
                                "num_a" : {"$sum" : {"$cond" : { "if" : { "$eq": ["$HEALTHY", "a"] }, "then": 1, "else": 0 }  }},
                                "num_r" : {"$sum" : {"$cond" : { "if" : { "$eq": ["$HEALTHY", "r"] }, "then": 1, "else": 0 }  }},
                                "num_g" : {"$sum" : {"$cond" : { "if" : { "$eq": ["$HEALTHY", "g"] }, "then": 1, "else": 0 }  }},
                                }
                }]

    print aggregation
    res = collHandle.aggregate(aggregation)['result']

    leaderboard_items = []
    geojson_data = {'features':[]}

    for item in res:
        score = random.randint(0,5)
        region = item['_id']['borough']
        print region,
        item = {'name':item['_id']['borough'], 'r':item['num_r'], 'a':item['num_a'], 'g':item['num_g'], 'score':score}
        region_geojson = get_geojson(county_name=region, score=score)
        print region_geojson

        # Add in the geojson output if we managed to retrieve it
        if region_geojson != None:
            geojson_data['features'].append(region_geojson)

        leaderboard_items.append(item)

    # Convert to string before dumping out
    geojson_data = json.dumps(geojson_data)

    return render_template('index.html',
                           geojson_data=geojson_data,
                           leaderboard_flds=leaderboard_flds,
                           leaderboard_items=leaderboard_items)

# -----------------------------------------------------------------------------

@app.route('/')
def email_content():
    """ normal http request to a serve up the page """




    return render_template('index.html')


'''
# -----------------------------------------------------------------------------

@socketio.on('start_processor_event', namespace='/test')
def start_processor_event(data):
    """ Event receiver that starts the processor """

    # Log and emit the progress
    progress = {'data': {"key":"Command to start processor from client received by server.", "value":""}}
    update_progress(socketio, progress, event_type='progress_update', namespace='/test')

    # Call the matching algorithm
    matching.main(socketio)
    '''
'''
# -----------------------------------------------------------------------------

@socketio.on('connect', namespace='/test')
def test_connect():

    progress ={'data': {'key':'Connection','value':'New client websocket connection made.'}}
    update_progress(socketio, progress, event_type='progress_update', namespace='/test')

# -----------------------------------------------------------------------------

@socketio.on('disconnect', namespace='/test')
def test_disconnect():

    progress ={'data': {'key':'Connection','value':'Client disconnected.'}}
    update_progress(socketio, progress, event_type='progress_update', namespace='/test')

# -----------------------------------------------------------------------------
'''
@app.route('/data')
def graphData():

    gD = [
            {'date':'1-May-12', 'close':582.13},
            {'date':'30-Apr-12', 'close':    583.98},
            {'date':'27-Apr-12', 'close':     603.00},
            {'date':'26-Apr-12', 'close':   607.70}]


    return jsonify(graphData=gD)

@app.route('/lines')
def line():
    graphData = [
            {'date':'1-May-12', 'close':582.13},
            {'date':'30-Apr-12', 'close':    583.98},
            {'date':'27-Apr-12', 'close':     603.00},
            {'date':'26-Apr-12', 'close':   607.70}]

    allOutput = [ {'demZ':10, 'flightZ':5, 'rnge':1},
                 {'demZ':20, 'flightZ':5, 'rnge':2},
                 {'demZ':30, 'flightZ':5, 'rnge':3},
                 {'demZ':40, 'flightZ':5, 'rnge':4}]



    return render_template('lines.html', allOutput=allOutput)

@app.route('/profile')
def personal_profile():
    """ normal http request to a serve up the page """

    print 'hello'
    leaderboard_flds = ["health", "score"]

    item1 = {'health':'red', 'score':10, 'colour':'red'}
    item2 = {'health':'amber', 'score':15, 'colour':'orange'}
    item3 = {'health':'green', 'score':55, 'colour':'green'}
    allTimeItems =[item1, item2, item3]

    item1 = {'health':'red', 'score':5, 'colour':'red'}
    item2 = {'health':'amber', 'score':20, 'colour':'orange'}
    item3 = {'health':'green', 'score':2, 'colour':'green'}
    lastMonth =[item1, item2, item3]

    item1 = {'health':'red', 'score':1, 'colour':'red'}
    item2 = {'health':'amber', 'score':10, 'colour':'orange'}
    item3 = {'health':'green', 'score':5, 'colour':'green'}
    mostRecentShop =[item1, item2, item3]

    graphData = [
            {'date':'1-May-12', 'close':582.13},
            {'date':'30-Apr-12', 'close':    583.98},
            {'date':'27-Apr-12', 'close':     603.00},
            {'date':'26-Apr-12', 'close':   607.70}]


    allOutput = [ {'demZ':10, 'flightZ':5, 'rnge':1},
                 {'demZ':25, 'flightZ':15, 'rnge':2},
                 {'demZ':40, 'flightZ':35, 'rnge':3},
                 {'demZ':5, 'flightZ':7, 'rnge':4}]


    return render_template('personal_profile.html',
                           leaderboard_flds=leaderboard_flds,
                           allTimeItems=allTimeItems,
                           lastMonth = lastMonth,
                           mostRecentShop = mostRecentShop,
                           allOutput=allOutput)

if __name__ == '__main__':

    app.run()

    #socketio.run(app)
    """
    """






