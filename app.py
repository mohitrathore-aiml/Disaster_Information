from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# PostgreSQL configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/disaster_info"
)

# Railway / SQLAlchemy fixes
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# FORCE psycopg v3
DATABASE_URL = DATABASE_URL.replace(
    "postgresql://",
    "postgresql+psycopg://",
    1
)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

# ==========================
# Database Models
# ==========================

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    severity = db.Column(db.String(50), default="medium")
    location = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Helpline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    number = db.Column(db.String(50))
    category = db.Column(db.String(100), default="general")
    description = db.Column(db.Text)


class SafeLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    capacity = db.Column(db.Integer, default=0)
    current_occupancy = db.Column(db.Integer, default=0)
    facilities = db.Column(db.JSON)
    contact = db.Column(db.String(100))


class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    skills = db.Column(db.JSON)
    availability = db.Column(db.String(50), default="available")
    location = db.Column(db.String(200))
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================
# Routes
# ==========================

@app.route("/")
def index():
    return render_template("index.html")


# ---- Alerts ----
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()
    return jsonify([
        {
            "id": a.id,
            "title": a.title,
            "message": a.message,
            "severity": a.severity,
            "location": a.location,
            "timestamp": a.timestamp
        } for a in alerts
    ])


@app.route("/api/alerts", methods=["POST"])
def create_alert():
    data = request.json
    alert = Alert(
        title=data.get("title"),
        message=data.get("message"),
        severity=data.get("severity", "medium"),
        location=data.get("location", "")
    )
    db.session.add(alert)
    db.session.commit()
    return jsonify({"id": alert.id}), 201


# ---- Helplines ----
@app.route("/api/helplines", methods=["GET"])
def get_helplines():
    helplines = Helpline.query.all()
    return jsonify([
        {
            "id": h.id,
            "name": h.name,
            "number": h.number,
            "category": h.category,
            "description": h.description
        } for h in helplines
    ])


@app.route("/api/helplines", methods=["POST"])
def create_helpline():
    data = request.json
    helpline = Helpline(
        name=data.get("name"),
        number=data.get("number"),
        category=data.get("category", "general"),
        description=data.get("description", "")
    )
    db.session.add(helpline)
    db.session.commit()
    return jsonify({"id": helpline.id}), 201


# ---- Safe Locations ----
@app.route("/api/safe-locations", methods=["GET"])
def get_safe_locations():
    locations = SafeLocation.query.all()
    return jsonify([
        {
            "id": l.id,
            "name": l.name,
            "address": l.address,
            "latitude": l.latitude,
            "longitude": l.longitude,
            "capacity": l.capacity,
            "current_occupancy": l.current_occupancy,
            "facilities": l.facilities,
            "contact": l.contact
        } for l in locations
    ])


@app.route("/api/safe-locations", methods=["POST"])
def create_safe_location():
    data = request.json
    location = SafeLocation(
        name=data.get("name"),
        address=data.get("address"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
        capacity=data.get("capacity", 0),
        current_occupancy=data.get("current_occupancy", 0),
        facilities=data.get("facilities", []),
        contact=data.get("contact", "")
    )
    db.session.add(location)
    db.session.commit()
    return jsonify({"id": location.id}), 201


# ---- Volunteers ----
@app.route("/api/volunteers", methods=["GET"])
def get_volunteers():
    volunteers = Volunteer.query.all()
    return jsonify([
        {
            "id": v.id,
            "name": v.name,
            "email": v.email,
            "phone": v.phone,
            "skills": v.skills,
            "availability": v.availability,
            "location": v.location,
            "registered_at": v.registered_at
        } for v in volunteers
    ])


@app.route("/api/volunteers", methods=["POST"])
def register_volunteer():
    data = request.json
    volunteer = Volunteer(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        skills=data.get("skills", []),
        availability=data.get("availability", "available"),
        location=data.get("location", "")
    )
    db.session.add(volunteer)
    db.session.commit()
    return jsonify({"id": volunteer.id}), 201


# ==========================
# Main
# ==========================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
