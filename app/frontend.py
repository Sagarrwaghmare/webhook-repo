from flask import Blueprint, render_template, jsonify
from pymongo import MongoClient

# Create a Blueprint named 'main_bp'
main_bp = Blueprint('main_bp', __name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['git_dashboard']
collection = db['events']

# 1. THE FRONTEND PAGE (http://localhost:5000/)
@main_bp.route('/')
def index():
    return render_template('index.html')

# 2. THE API FOR THE FRONTEND (Fetches data from Mongo)
@main_bp.route('/api/events')
def get_events():
    # Fetch last 20 events, sorted by newest first
    # We exclude '_id' because it is not JSON serializable by default
    cursor = collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(20)
    events = list(cursor)
    return jsonify(events)