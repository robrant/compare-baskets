
import os
import sys
import logging
from pymongo import Connection

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

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
socketio = SocketIO(app)

import mdb

c, dbh = mdb.getHandle(host = 'localhost',
                       port     = 27017,
                       db       = 'transactions')

collHandle = dbh['idea']

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

@app.route('/')
def index():
    """ normal http request to a serve up the page """  
    
    collHandle
    
    
    
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

if __name__ == '__main__':

    socketio.run(app)
    """
    """
    





