// API Base URL
const API_BASE = '';

// Smooth scrolling for navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });
});

// Update active nav on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 100) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

// Utility function to show messages
function showMessage(elementId, message, type = 'success') {
    const element = document.getElementById(elementId);
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    element.insertBefore(messageDiv, element.firstChild);
    setTimeout(() => messageDiv.remove(), 5000);
}

// Load all data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadAlerts();
    loadHelplines();
    loadSafeLocations();
    loadVolunteers();
});

// ========== ALERTS ==========
function loadAlerts() {
    fetch(`${API_BASE}/api/alerts`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('alertsList');
            if (data.length === 0) {
                container.innerHTML = '<p class="loading">No alerts available. Be the first to post one!</p>';
                return;
            }
            container.innerHTML = data.map(alert => `
                <div class="alert-card ${alert.severity}">
                    <h4>${alert.title}</h4>
                    <p>${alert.message}</p>
                    ${alert.location ? `<p><strong>Location:</strong> ${alert.location}</p>` : ''}
                    <div class="meta">
                        <strong>Severity:</strong> ${alert.severity.toUpperCase()} | 
                        <strong>Posted:</strong> ${formatDate(alert.timestamp)}
                    </div>
                </div>
            `).join('');
        })
        .catch(err => {
            document.getElementById('alertsList').innerHTML = 
                '<p class="error">Error loading alerts. Please try again later.</p>';
        });
}

document.getElementById('alertForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const alertData = {
        title: document.getElementById('alertTitle').value,
        message: document.getElementById('alertMessage').value,
        severity: document.getElementById('alertSeverity').value,
        location: document.getElementById('alertLocation').value
    };
    
    fetch(`${API_BASE}/api/alerts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(alertData)
    })
    .then(res => res.json())
    .then(data => {
        showMessage('alertsList', 'Alert posted successfully!', 'success');
        document.getElementById('alertForm').reset();
        loadAlerts();
    })
    .catch(err => {
        showMessage('alertsList', 'Error posting alert. Please try again.', 'error');
    });
});

// ========== HELPLINES ==========
function loadHelplines() {
    fetch(`${API_BASE}/api/helplines`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('helplinesList');
            if (data.length === 0) {
                container.innerHTML = '<p class="loading">No helplines available. Add one to help others!</p>';
                return;
            }
            container.innerHTML = data.map(helpline => `
                <div class="helpline-card">
                    <h4>${helpline.name}</h4>
                    <div class="number">${helpline.number}</div>
                    ${helpline.description ? `<p>${helpline.description}</p>` : ''}
                    <span class="category">${helpline.category}</span>
                </div>
            `).join('');
        })
        .catch(err => {
            document.getElementById('helplinesList').innerHTML = 
                '<p class="error">Error loading helplines. Please try again later.</p>';
        });
}

document.getElementById('helplineForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const helplineData = {
        name: document.getElementById('helplineName').value,
        number: document.getElementById('helplineNumber').value,
        category: document.getElementById('helplineCategory').value,
        description: document.getElementById('helplineDescription').value
    };
    
    fetch(`${API_BASE}/api/helplines`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(helplineData)
    })
    .then(res => res.json())
    .then(data => {
        showMessage('helplinesList', 'Helpline added successfully!', 'success');
        document.getElementById('helplineForm').reset();
        loadHelplines();
    })
    .catch(err => {
        showMessage('helplinesList', 'Error adding helpline. Please try again.', 'error');
    });
});

// ========== SAFE LOCATIONS ==========
function loadSafeLocations() {
    fetch(`${API_BASE}/api/safe-locations`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('locationsList');
            if (data.length === 0) {
                container.innerHTML = '<p class="loading">No safe locations available. Add one to help others find shelter!</p>';
                return;
            }
            container.innerHTML = data.map(location => `
                <div class="location-card">
                    <h4>${location.name}</h4>
                    <p class="address">📍 ${location.address}</p>
                    ${location.contact ? `<p><strong>Contact:</strong> ${location.contact}</p>` : ''}
                    <div class="info">
                        <div class="info-item">
                            <strong>Capacity</strong>
                            ${location.capacity || 'N/A'}
                        </div>
                        <div class="info-item">
                            <strong>Occupancy</strong>
                            ${location.current_occupancy || 0}
                        </div>
                        ${location.latitude && location.longitude ? `
                        <div class="info-item">
                            <strong>Coordinates</strong>
                            ${location.latitude}, ${location.longitude}
                        </div>
                        ` : ''}
                    </div>
                    ${location.facilities && location.facilities.length > 0 ? `
                    <div class="facilities">
                        ${location.facilities.map(f => `<span class="facility-tag">${f}</span>`).join('')}
                    </div>
                    ` : ''}
                </div>
            `).join('');
        })
        .catch(err => {
            document.getElementById('locationsList').innerHTML = 
                '<p class="error">Error loading safe locations. Please try again later.</p>';
        });
}

document.getElementById('locationForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const facilities = document.getElementById('locationFacilities').value
        .split(',')
        .map(f => f.trim())
        .filter(f => f);
    
    const locationData = {
        name: document.getElementById('locationName').value,
        address: document.getElementById('locationAddress').value,
        latitude: parseFloat(document.getElementById('locationLat').value) || null,
        longitude: parseFloat(document.getElementById('locationLng').value) || null,
        capacity: parseInt(document.getElementById('locationCapacity').value) || 0,
        current_occupancy: parseInt(document.getElementById('locationOccupancy').value) || 0,
        contact: document.getElementById('locationContact').value,
        facilities: facilities
    };
    
    fetch(`${API_BASE}/api/safe-locations`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(locationData)
    })
    .then(res => res.json())
    .then(data => {
        showMessage('locationsList', 'Safe location added successfully!', 'success');
        document.getElementById('locationForm').reset();
        loadSafeLocations();
    })
    .catch(err => {
        showMessage('locationsList', 'Error adding location. Please try again.', 'error');
    });
});

// ========== VOLUNTEERS ==========
function loadVolunteers() {
    fetch(`${API_BASE}/api/volunteers`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('volunteersList');
            if (data.length === 0) {
                container.innerHTML = '<p class="loading">No volunteers registered yet. Be the first to help!</p>';
                return;
            }
            container.innerHTML = data.map(volunteer => `
                <div class="volunteer-card">
                    <h4>${volunteer.name}</h4>
                    <div class="contact">
                        📧 ${volunteer.email}<br>
                        📞 ${volunteer.phone}
                    </div>
                    ${volunteer.location ? `<p><strong>Location:</strong> ${volunteer.location}</p>` : ''}
                    <span class="availability ${volunteer.availability}">${volunteer.availability}</span>
                    ${volunteer.skills && volunteer.skills.length > 0 ? `
                    <div class="skills">
                        ${volunteer.skills.map(s => `<span class="skill-tag">${s}</span>`).join('')}
                    </div>
                    ` : ''}
                </div>
            `).join('');
        })
        .catch(err => {
            document.getElementById('volunteersList').innerHTML = 
                '<p class="error">Error loading volunteers. Please try again later.</p>';
        });
}

document.getElementById('volunteerForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const skills = document.getElementById('volunteerSkills').value
        .split(',')
        .map(s => s.trim())
        .filter(s => s);
    
    const volunteerData = {
        name: document.getElementById('volunteerName').value,
        email: document.getElementById('volunteerEmail').value,
        phone: document.getElementById('volunteerPhone').value,
        location: document.getElementById('volunteerLocation').value,
        skills: skills,
        availability: document.getElementById('volunteerAvailability').value
    };
    
    fetch(`${API_BASE}/api/volunteers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(volunteerData)
    })
    .then(res => res.json())
    .then(data => {
        showMessage('volunteersList', 'Thank you for registering as a volunteer!', 'success');
        document.getElementById('volunteerForm').reset();
        loadVolunteers();
    })
    .catch(err => {
        showMessage('volunteersList', 'Error registering. Please try again.', 'error');
    });
});
