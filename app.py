"""
Flask web application for Travel Itinerary Optimizer
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from scraper import MultiSiteScraper
from optimizer import ItineraryOptimizer
import config

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/api/optimize', methods=['POST'])
def optimize():
    """API endpoint to create optimized itinerary"""
    try:
        data = request.json
        
        origin = data.get('origin', config.DEFAULT_DEPARTURE_CITY)
        destination = data.get('destination', config.DEFAULT_DESTINATION_CITY)
        departure_date = data.get('departure_date')
        return_date = data.get('return_date')
        travelers = data.get('travelers', config.DEFAULT_TRAVELERS)
        cost_weight = data.get('cost_weight', config.COST_WEIGHT)
        time_weight = data.get('time_weight', config.TIME_WEIGHT)
        
        # Set default dates if not provided
        if not departure_date:
            departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        if not return_date:
            return_date = (datetime.strptime(departure_date, "%Y-%m-%d") + 
                          timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Initialize scraper
        scraper = MultiSiteScraper(config.TRAVEL_WEBSITES)
        
        try:
            # Scrape data
            flights = scraper.scrape_all_flights(
                origin, destination, departure_date, return_date, travelers
            )
            
            hotels = scraper.scrape_all_hotels(
                destination, departure_date, return_date, travelers
            )
            
            # Generate activities for each day
            all_activities = []
            current_date = datetime.strptime(departure_date, "%Y-%m-%d") + timedelta(days=1)
            return_dt = datetime.strptime(return_date, "%Y-%m-%d")
            
            while current_date < return_dt:
                date_str = current_date.strftime("%Y-%m-%d")
                activities = scraper.scrape_all_activities(destination, date_str)
                all_activities.extend(activities)
                current_date += timedelta(days=1)
            
            # Optimize itinerary
            optimizer = ItineraryOptimizer(
                cost_weight=cost_weight,
                time_weight=time_weight
            )
            
            itinerary = optimizer.create_itinerary(
                flights, hotels, all_activities, departure_date, return_date
            )
            
            return jsonify({
                'success': True,
                'itinerary': itinerary
            })
        
        finally:
            scraper.cleanup()
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
