from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
import json
from geopy.distance import geodesic
import sqlite3

load_dotenv()

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('user_log/user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  user_agent TEXT,
                  latitude REAL,
                  longitude REAL,
                  address TEXT)''')
    conn.commit()
    conn.close()

init_db()

def log_user_data(user_agent, lat, lng, address):
    conn = sqlite3.connect('user_log/user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO user_logs (timestamp, user_agent, latitude, longitude, address) VALUES (?, ?, ?, ?, ?)',
              (datetime.now().isoformat(), user_agent, lat, lng, address))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True) 