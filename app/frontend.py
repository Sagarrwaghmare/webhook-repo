from flask import Blueprint, render_template, jsonify
from pymongo import MongoClient

main_bp = Blueprint('main_bp', __name__)

# connecting to local instance; using 'git_dashboard' as defined in setup
client = MongoClient('mongodb://localhost:27017/')
db = client['git_dashboard']
collection = db['events']

@main_bp.route('/')
def index():
    # render the main dashboard for polling
    return render_template('index.html')

@main_bp.route('/api/events')
def get_events():
    # internal api for ui polling (15s interval)
    # sort descending to show latest events first
    cursor = collection.find({}, {'_id': 0}).sort("timestamp", -1) 
    events = list(cursor)
    
    return jsonify(events)