# Disaster Information & Emergency Help Website

A hackathon-level emergency response website that provides quick access to reliable information and support resources during disasters.

## Features

- 🚨 **Emergency Alerts**: Real-time disaster warnings and updates with severity levels
- 📞 **Helpline Numbers**: Quick access to emergency services and support organizations
- 🏠 **Safe Locations**: List of shelters and evacuation points with capacity information
- 👥 **Volunteer Registration**: Allow individuals to sign up and help during emergencies

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: MongoDB

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- MongoDB installed and running (or MongoDB Atlas connection string)

### Installation

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB:
   - **Local MongoDB**: Make sure MongoDB is running on `localhost:27017`
   - **MongoDB Atlas**: Set the `MONGO_URI` environment variable:
   ```bash
   export MONGO_URI="mongodb+srv://username:password@cluster.mongodb.net/"
   ```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
.
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── style.css     # Stylesheet
    └── js/
        └── app.js        # Frontend JavaScript
```

## API Endpoints

### Alerts
- `GET /api/alerts` - Get all alerts
- `POST /api/alerts` - Create a new alert

### Helplines
- `GET /api/helplines` - Get all helpline numbers
- `POST /api/helplines` - Add a new helpline

### Safe Locations
- `GET /api/safe-locations` - Get all safe locations
- `POST /api/safe-locations` - Add a new safe location

### Volunteers
- `GET /api/volunteers` - Get all registered volunteers
- `POST /api/volunteers` - Register a new volunteer

## Usage

1. **View Alerts**: Navigate to the Alerts section to see current emergency alerts
2. **Add Helplines**: Use the form to add emergency contact numbers
3. **Find Safe Locations**: Browse available shelters and safe locations
4. **Register as Volunteer**: Fill out the volunteer form to offer help

## Features in Detail

### Emergency Alerts
- Post alerts with title, message, severity level, and location
- Severity levels: Low, Medium, High, Critical
- Real-time display of recent alerts

### Helpline Numbers
- Categorized helplines (Medical, Fire, Police, Rescue, Shelter, General)
- Quick access to emergency contacts
- Add new helplines with descriptions

### Safe Locations
- Location details with address and coordinates
- Capacity and current occupancy tracking
- Facility information (food, water, medical, etc.)

### Volunteer Registration
- Register with name, contact, and location
- List skills and availability status
- Help coordinate relief efforts

## Development Notes

This is a hackathon-level project designed for rapid deployment. For production use, consider:

- Adding authentication and authorization
- Implementing data validation and sanitization
- Adding rate limiting for API endpoints
- Setting up proper error handling and logging
- Adding unit tests
- Implementing data backup and recovery
- Adding real-time updates using WebSockets
- Integrating with external emergency services APIs

## License

This project is open source and available for hackathon use.

## Contributing

Feel free to fork and improve this project for your hackathon needs!
