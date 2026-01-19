"""
Example usage of the Travel Itinerary Optimizer
"""

from scraper import MultiSiteScraper
from optimizer import ItineraryOptimizer
from datetime import datetime, timedelta
import config


def example_basic_usage():
    """Basic example of using the optimizer"""
    
    # Set up dates
    departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    return_date = (datetime.strptime(departure_date, "%Y-%m-%d") + 
                  timedelta(days=7)).strftime("%Y-%m-%d")
    
    origin = "New York"
    destination = "Paris"
    travelers = 2
    
    print("Example: Creating itinerary for couple")
    print(f"Origin: {origin}")
    print(f"Destination: {destination}")
    print(f"Dates: {departure_date} to {return_date}\n")
    
    # Initialize scraper
    scraper = MultiSiteScraper(config.TRAVEL_WEBSITES)
    
    try:
        # Scrape data
        print("Scraping flights...")
        flights = scraper.scrape_all_flights(
            origin, destination, departure_date, return_date, travelers
        )
        print(f"Found {len(flights)} flight options\n")
        
        print("Scraping hotels...")
        hotels = scraper.scrape_all_hotels(
            destination, departure_date, return_date, travelers
        )
        print(f"Found {len(hotels)} hotel options\n")
        
        print("Scraping activities...")
        all_activities = []
        current_date = datetime.strptime(departure_date, "%Y-%m-%d") + timedelta(days=1)
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
        
        while current_date < return_dt:
            date_str = current_date.strftime("%Y-%m-%d")
            activities = scraper.scrape_all_activities(destination, date_str)
            all_activities.extend(activities)
            current_date += timedelta(days=1)
        
        print(f"Found {len(all_activities)} activity options\n")
        
        # Optimize
        print("Optimizing itinerary...")
        optimizer = ItineraryOptimizer(
            cost_weight=config.COST_WEIGHT,
            time_weight=config.TIME_WEIGHT
        )
        
        itinerary = optimizer.create_itinerary(
            flights, hotels, all_activities, departure_date, return_date
        )
        
        # Display results
        print("\n" + "="*60)
        print("OPTIMIZED ITINERARY")
        print("="*60)
        print(f"\nTotal Cost: ${itinerary['summary']['total_cost']:,.2f}")
        print(f"Total Time: {itinerary['summary']['total_time_hours']:.1f} hours")
        
        if itinerary['flight']:
            f = itinerary['flight']
            print(f"\nFlight: {f['airline']} - ${f['total_price']:,.2f}")
        
        if itinerary['hotel']:
            h = itinerary['hotel']
            print(f"Hotel: {h['name']} - ${h['total_price']:,.2f}")
        
        print(f"\nDays with activities: {len(itinerary['days'])}")
        
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    example_basic_usage()
