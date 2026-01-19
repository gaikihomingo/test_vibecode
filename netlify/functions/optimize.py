"""
Netlify serverless function for itinerary optimization
"""

import json
import sys
import os
from datetime import datetime, timedelta

# Add current directory to path to import modules (they're copied here)
sys.path.insert(0, os.path.dirname(__file__))

from scraper import MultiSiteScraper
from optimizer import ItineraryOptimizer
import config


def handler(event, context):
    """
    Netlify serverless function handler
    
    Args:
        event: Event object containing request data
        context: Context object (unused)
    
    Returns:
        Response dictionary with statusCode and body
    """
    # Handle CORS preflight
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': ''
        }
    
    try:
        # Parse request body
        if isinstance(event.get('body'), str):
            data = json.loads(event['body'])
        else:
            data = event.get('body', {})
        
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
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'success': True,
                    'itinerary': itinerary
                }, default=str)
            }
        
        finally:
            scraper.cleanup()
    
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': error_msg
            })
        }
