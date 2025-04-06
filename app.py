from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
import json
from geopy.distance import geodesic
import sqlite3
import platform

load_dotenv()

app = Flask(__name__)

# Database setup
def init_db():
    try:
        os.makedirs('user_log', exist_ok=True)
        conn = sqlite3.connect('user_log/user_data.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS user_logs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_agent TEXT,
                    latitude REAL,
                    longitude REAL,
                    address TEXT,
                    is_duplicate INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database initialization error: {str(e)}")

init_db()

def get_db_connection():
    return sqlite3.connect('user_log/user_data.db')

def is_duplicate_visit(user_agent, lat, lng, time_window_minutes=5):
    conn = sqlite3.connect('user_log/user_data.db')
    c = conn.cursor()
    
    # Calculate time threshold
    time_threshold = (datetime.now() - timedelta(minutes=time_window_minutes)).isoformat()
    
    # Check for similar visits within time window
    c.execute('''SELECT COUNT(*) FROM user_logs 
                 WHERE user_agent = ? 
                 AND timestamp > ? 
                 AND ABS(latitude - ?) < 0.0001 
                 AND ABS(longitude - ?) < 0.0001''',
              (user_agent, time_threshold, lat, lng))
    
    count = c.fetchone()[0]
    conn.close()
    
    return count > 0

def log_user_data(user_agent, latitude, longitude, address):
    try:
        conn = sqlite3.connect('user_log/user_data.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO user_logs (timestamp, user_agent, latitude, longitude, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), user_agent, latitude, longitude, address))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error logging user data: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/get_user_logs')
def get_user_logs():
    try:
        conn = sqlite3.connect('user_log/user_data.db')
        cursor = conn.cursor()
        
        # Get all logs
        cursor.execute('''
            SELECT id, timestamp, user_agent, latitude, longitude, address 
            FROM user_logs 
            ORDER BY timestamp DESC
        ''')
        logs = cursor.fetchall()
        
        # Get unique browsers
        cursor.execute('SELECT COUNT(DISTINCT user_agent) FROM user_logs')
        unique_browsers = cursor.fetchone()[0]
        
        # Format logs
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                'id': log[0],
                'timestamp': log[1],
                'user_agent': log[2],
                'latitude': log[3],
                'longitude': log[4],
                'address': log[5]
            })
        
        conn.close()
        
        return jsonify({
            'logs': formatted_logs,
            'total_visits': len(logs),
            'unique_browsers': unique_browsers,
            'last_visit': logs[0][1] if logs else None
        })
        
    except Exception as e:
        print(f"Error getting user logs: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_restaurants', methods=['POST'])
def get_restaurants():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')
    user_agent = request.headers.get('User-Agent')
    
    # Get address from coordinates
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={os.getenv('GOOGLE_API_KEY')}"
    geocode_response = requests.get(geocode_url).json()
    address = geocode_response.get('results', [{}])[0].get('formatted_address', '')
    
    # Log user data
    log_user_data(user_agent, lat, lng, address)
    
    # Get nearby restaurants
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1500&type=restaurant&key={os.getenv('GOOGLE_API_KEY')}"
    places_response = requests.get(places_url).json()
    
    restaurants = []
    for place in places_response.get('results', []):
        restaurant = {
            'name': place.get('name'),
            'rating': place.get('rating', 0),
            'vicinity': place.get('vicinity'),
            'place_id': place.get('place_id'),
            'photos': place.get('photos', [{}])[0].get('photo_reference', '') if place.get('photos') else '',
            'lat': place.get('geometry', {}).get('location', {}).get('lat'),
            'lng': place.get('geometry', {}).get('location', {}).get('lng')
        }
        restaurants.append(restaurant)
    
    # Sort by rating
    restaurants.sort(key=lambda x: x['rating'], reverse=True)
    
    return jsonify({
        'restaurants': restaurants,
        'user_location': {'lat': lat, 'lng': lng, 'address': address}
    })

@app.route('/get_computer_name')
def get_computer_name():
    return jsonify({
        'computer_name': platform.node()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 