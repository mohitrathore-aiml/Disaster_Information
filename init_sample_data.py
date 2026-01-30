"""
Sample data initialization script for Disaster Information & Emergency Help Website
Run this script once to populate the database with sample data
"""

from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client.disaster_info

# Clear existing collections (optional - comment out if you want to keep existing data)
# db.alerts.delete_many({})
# db.helplines.delete_many({})
# db.safe_locations.delete_many({})
# db.volunteers.delete_many({})

# Sample Alerts
sample_alerts = [
    {
        'title': 'Heavy Rainfall Warning',
        'message': 'Heavy rainfall expected in the next 24 hours. Please stay indoors and avoid low-lying areas.',
        'severity': 'high',
        'location': 'Downtown Area',
        'timestamp': datetime.now()
    },
    {
        'title': 'Emergency Shelter Open',
        'message': 'Community Center at 123 Main St is now open as an emergency shelter.',
        'severity': 'medium',
        'location': '123 Main Street',
        'timestamp': datetime.now()
    }
]

# Sample Helplines
sample_helplines = [
    {
        'name': 'Emergency Services',
        'number': '911',
        'category': 'general',
        'description': 'General emergency services'
    },
    {
        'name': 'Disaster Relief Hotline',
        'number': '1-800-DISASTER',
        'category': 'rescue',
        'description': '24/7 disaster relief assistance'
    },
    {
        'name': 'Medical Emergency',
        'number': '1-800-MEDICAL',
        'category': 'medical',
        'description': 'Medical emergency hotline'
    },
    {
        'name': 'Fire Department',
        'number': '1-800-FIRE',
        'category': 'fire',
        'description': 'Fire emergency services'
    }
]

# Sample Safe Locations
sample_locations = [
    {
        'name': 'Community Center',
        'address': '123 Main Street, City, State 12345',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'capacity': 200,
        'current_occupancy': 45,
        'facilities': ['Food', 'Water', 'Medical', 'Restrooms', 'WiFi'],
        'contact': '555-0100'
    },
    {
        'name': 'High School Gymnasium',
        'address': '456 School Road, City, State 12345',
        'latitude': 40.7580,
        'longitude': -73.9855,
        'capacity': 500,
        'current_occupancy': 120,
        'facilities': ['Food', 'Water', 'Restrooms', 'Showers'],
        'contact': '555-0200'
    },
    {
        'name': 'City Hall',
        'address': '789 Government Ave, City, State 12345',
        'latitude': 40.7505,
        'longitude': -73.9934,
        'capacity': 150,
        'current_occupancy': 30,
        'facilities': ['Food', 'Water', 'WiFi', 'Charging Stations'],
        'contact': '555-0300'
    }
]

# Sample Volunteers
sample_volunteers = [
    {
        'name': 'John Doe',
        'email': 'john.doe@email.com',
        'phone': '555-1000',
        'skills': ['First Aid', 'Cooking', 'Translation'],
        'availability': 'available',
        'location': 'Downtown Area',
        'registered_at': datetime.now()
    },
    {
        'name': 'Jane Smith',
        'email': 'jane.smith@email.com',
        'phone': '555-2000',
        'skills': ['Medical', 'Counseling'],
        'availability': 'available',
        'location': 'North Side',
        'registered_at': datetime.now()
    }
]

# Insert sample data
print("Inserting sample data...")

if db.alerts.count_documents({}) == 0:
    db.alerts.insert_many(sample_alerts)
    print(f"✓ Inserted {len(sample_alerts)} alerts")
else:
    print(f"⚠ Alerts collection already has data. Skipping...")

if db.helplines.count_documents({}) == 0:
    db.helplines.insert_many(sample_helplines)
    print(f"✓ Inserted {len(sample_helplines)} helplines")
else:
    print(f"⚠ Helplines collection already has data. Skipping...")

if db.safe_locations.count_documents({}) == 0:
    db.safe_locations.insert_many(sample_locations)
    print(f"✓ Inserted {len(sample_locations)} safe locations")
else:
    print(f"⚠ Safe locations collection already has data. Skipping...")

if db.volunteers.count_documents({}) == 0:
    db.volunteers.insert_many(sample_volunteers)
    print(f"✓ Inserted {len(sample_volunteers)} volunteers")
else:
    print(f"⚠ Volunteers collection already has data. Skipping...")

print("\nSample data initialization complete!")
print("You can now run 'python app.py' to start the server.")
