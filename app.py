from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import os

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client.disaster_info

# Collections
alerts_collection = db.alerts
helplines_collection = db.helplines
safe_locations_collection = db.safe_locations
volunteers_collection = db.volunteers

@app.route('/')
def index():
    return render_template('index.html')

# Alerts endpoints
@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    alerts = list(alerts_collection.find().sort('timestamp', -1).limit(10))
    for alert in alerts:
        alert['_id'] = str(alert['_id'])
    return jsonify(alerts)

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    data = request.json
    alert = {
        'title': data.get('title'),
        'message': data.get('message'),
        'severity': data.get('severity', 'medium'),
        'location': data.get('location', ''),
        'timestamp': datetime.now()
    }
    result = alerts_collection.insert_one(alert)
    alert['_id'] = str(result.inserted_id)
    return jsonify(alert), 201

# Helpline endpoints
@app.route('/api/helplines', methods=['GET'])
def get_helplines():
    helplines = list(helplines_collection.find())
    for helpline in helplines:
        helpline['_id'] = str(helpline['_id'])
    return jsonify(helplines)

@app.route('/api/helplines', methods=['POST'])
def create_helpline():
    data = request.json
    helpline = {
        'name': data.get('name'),
        'number': data.get('number'),
        'category': data.get('category', 'general'),
        'description': data.get('description', '')
    }
    result = helplines_collection.insert_one(helpline)
    helpline['_id'] = str(result.inserted_id)
    return jsonify(helpline), 201

# Safe locations endpoints
@app.route('/api/safe-locations', methods=['GET'])
def get_safe_locations():
    locations = list(safe_locations_collection.find())
    for location in locations:
        location['_id'] = str(location['_id'])
    return jsonify(locations)

@app.route('/api/safe-locations', methods=['POST'])
def create_safe_location():
    data = request.json
    location = {
        'name': data.get('name'),
        'address': data.get('address'),
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'capacity': data.get('capacity', 0),
        'current_occupancy': data.get('current_occupancy', 0),
        'facilities': data.get('facilities', []),
        'contact': data.get('contact', '')
    }
    result = safe_locations_collection.insert_one(location)
    location['_id'] = str(result.inserted_id)
    return jsonify(location), 201

# Volunteer registration endpoints
@app.route('/api/volunteers', methods=['GET'])
def get_volunteers():
    volunteers = list(volunteers_collection.find())
    for volunteer in volunteers:
        volunteer['_id'] = str(volunteer['_id'])
    return jsonify(volunteers)

@app.route('/api/volunteers', methods=['POST'])
def register_volunteer():
    data = request.json
    volunteer = {
        'name': data.get('name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'skills': data.get('skills', []),
        'availability': data.get('availability', 'available'),
        'location': data.get('location', ''),
        'registered_at': datetime.now()
    }
    result = volunteers_collection.insert_one(volunteer)
    volunteer['_id'] = str(result.inserted_id)
    return jsonify(volunteer), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
