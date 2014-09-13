
import os
import sys
import logging
from pymongo import Connection
import json
import random

from flask import Flask, render_template
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
f = open('/Users/robrant/eclipseWorkspace/geo_app/data/borough.geojson', 'r')
county_gj = json.loads(f.read)

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
    
    
    


@app.route('/')
def index():
    """ normal http request to a serve up the page """  
    
    print 'hello'
    leaderboard_flds = ["name", "score"]
    
    aggregation = [{"$group" :
                                {"_id" : {"county" : "$BOROUGH"},
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
        item = {'name':item['_id']['county'], 'r':item['num_r'], 'a':item['num_a'], 'g':item['num_g'], 'score':score}
        geojson_data['features'].append(get_geojson(county_name=item['_id']['county'], score=score))
        
        leaderboard_items.append(item)
        
    
    geojson = open('/Users/robrant/eclipseCode/compare-baskets/geo_app/data/borough.geojson', 'r')
    geojson_data = json.loads(geojson.read())
    geojson_data = json.dumps(geojson_data, indent=2)
    
    
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

if __name__ == '__main__':

    app.run()
    
    #socketio.run(app)
    """
    """
    





