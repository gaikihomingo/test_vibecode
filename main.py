"""
Main application for Travel Itinerary Optimizer
"""

import argparse
import json
from datetime import datetime, timedelta
from scraper import MultiSiteScraper
from optimizer import ItineraryOptimizer
import config


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"


def print_itinerary(itinerary: dict):
    """Print formatted itinerary"""
    print("\n" + "="*80)
    print("OPTIMIZED TRAVEL ITINERARY FOR COUPLE")
    print("="*80)
    
    summary = itinerary.get("summary", {})
    print(f"\nTrip Duration: {summary.get('duration_days', 0)} days")
    print(f"Departure: {summary.get('departure_date', 'N/A')}")
    print(f"Return: {summary.get('return_date', 'N/A')}")
    print(f"\nTotal Cost: {format_currency(summary.get('total_cost', 0))}")
    print(f"Total Travel Time: {summary.get('total_time_hours', 0):.1f} hours")
    
    # Flight information
    flight = itinerary.get("flight")
    if flight:
        print("\n" + "-"*80)
        print("FLIGHT DETAILS")
        print("-"*80)
        print(f"Airline: {flight.get('airline', 'N/A')}")
        print(f"Route: {flight.get('origin', 'N/A')} → {flight.get('destination', 'N/A')}")
        print(f"Departure: {flight.get('departure_time', 'N/A')}")
        print(f"Arrival: {flight.get('arrival_time', 'N/A')}")
        print(f"Duration: {flight.get('duration_hours', 0):.1f} hours")
        print(f"Stops: {flight.get('stops', 0)}")
        print(f"Price: {format_currency(flight.get('total_price', 0))}")
        print(f"Source: {flight.get('source_website', 'N/A')}")
    
    # Hotel information
    hotel = itinerary.get("hotel")
    if hotel:
        print("\n" + "-"*80)
        print("HOTEL DETAILS")
        print("-"*80)
        print(f"Name: {hotel.get('name', 'N/A')}")
        print(f"Location: {hotel.get('location', 'N/A')}")
        print(f"Check-in: {hotel.get('check_in', 'N/A')}")
        print(f"Check-out: {hotel.get('check_out', 'N/A')}")
        print(f"Nights: {hotel.get('nights', 0)}")
        print(f"Rating: {hotel.get('rating', 0):.1f}/5.0")
        print(f"Price: {format_currency(hotel.get('total_price', 0))}")
        print(f"Amenities: {', '.join(hotel.get('amenities', []))}")
        print(f"Source: {hotel.get('source_website', 'N/A')}")
    
    # Daily activities
    days = itinerary.get("days", [])
    if days:
        print("\n" + "-"*80)
        print("DAILY ITINERARY")
        print("-"*80)
        
        for day in days:
            date = day.get("date", "N/A")
            activities = day.get("activities", [])
            
            print(f"\n📅 {date}")
            print(f"   Activities: {len(activities)}")
            print(f"   Daily Cost: {format_currency(day.get('total_cost', 0))}")
            print(f"   Total Time: {day.get('total_time_hours', 0):.1f} hours")
            
            for i, activity in enumerate(activities, 1):
                print(f"\n   {i}. {activity.get('name', 'N/A')}")
                print(f"      Category: {activity.get('category', 'N/A')}")
                print(f"      Duration: {activity.get('duration_hours', 0):.1f} hours")
                print(f"      Price: {format_currency(activity.get('total_price', 0))}")
                print(f"      Rating: {activity.get('rating', 0):.1f}/5.0")
    
    print("\n" + "="*80)
    print("End of Itinerary")
    print("="*80 + "\n")


def save_itinerary_json(itinerary: dict, filename: str = "itinerary.json"):
    """Save itinerary to JSON file"""
    with open(filename, 'w') as f:
        json.dump(itinerary, f, indent=2, default=str)
    print(f"Itinerary saved to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Travel Itinerary Optimizer")
    parser.add_argument("--origin", type=str, default=config.DEFAULT_DEPARTURE_CITY,
                       help="Departure city")
    parser.add_argument("--destination", type=str, default=config.DEFAULT_DESTINATION_CITY,
                       help="Destination city")
    parser.add_argument("--departure-date", type=str, default=None,
                       help="Departure date (YYYY-MM-DD)")
    parser.add_argument("--return-date", type=str, default=None,
                       help="Return date (YYYY-MM-DD)")
    parser.add_argument("--travelers", type=int, default=config.DEFAULT_TRAVELERS,
                       help="Number of travelers")
    parser.add_argument("--cost-weight", type=float, default=config.COST_WEIGHT,
                       help="Weight for cost optimization (0.0-1.0)")
    parser.add_argument("--time-weight", type=float, default=config.TIME_WEIGHT,
                       help="Weight for time optimization (0.0-1.0)")
    parser.add_argument("--output", type=str, default="itinerary.json",
                       help="Output JSON file")
    parser.add_argument("--no-print", action="store_true",
                       help="Don't print itinerary to console")
    
    args = parser.parse_args()
    
    # Set default dates if not provided
    if args.departure_date is None:
        departure_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        departure_date = args.departure_date
    
    if args.return_date is None:
        return_date = (datetime.strptime(departure_date, "%Y-%m-%d") + 
                      timedelta(days=7)).strftime("%Y-%m-%d")
    else:
        return_date = args.return_date
    
    print("="*80)
    print("TRAVEL ITINERARY OPTIMIZER")
    print("="*80)
    print(f"\nSearching for optimal itinerary:")
    print(f"  Origin: {args.origin}")
    print(f"  Destination: {args.destination}")
    print(f"  Departure: {departure_date}")
    print(f"  Return: {return_date}")
    print(f"  Travelers: {args.travelers}")
    print(f"  Cost Weight: {args.cost_weight}")
    print(f"  Time Weight: {args.time_weight}")
    print(f"\nScraping {len(config.TRAVEL_WEBSITES)} travel websites...")
    
    # Initialize scraper
    scraper = MultiSiteScraper(config.TRAVEL_WEBSITES)
    
    try:
        # Scrape data
        print("\n[1/3] Scraping flights...")
        flights = scraper.scrape_all_flights(
            args.origin, args.destination, departure_date, return_date, args.travelers
        )
        print(f"Found {len(flights)} flight options")
        
        print("\n[2/3] Scraping hotels...")
        hotels = scraper.scrape_all_hotels(
            args.destination, departure_date, return_date, args.travelers
        )
        print(f"Found {len(hotels)} hotel options")
        
        print("\n[3/3] Scraping activities...")
        # Generate activities for each day
        all_activities = []
        current_date = datetime.strptime(departure_date, "%Y-%m-%d") + timedelta(days=1)
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
        
        while current_date < return_dt:
            date_str = current_date.strftime("%Y-%m-%d")
            activities = scraper.scrape_all_activities(args.destination, date_str)
            all_activities.extend(activities)
            current_date += timedelta(days=1)
        
        print(f"Found {len(all_activities)} activity options")
        
        # Optimize itinerary
        print("\nOptimizing itinerary...")
        optimizer = ItineraryOptimizer(
            cost_weight=args.cost_weight,
            time_weight=args.time_weight
        )
        
        itinerary = optimizer.create_itinerary(
            flights, hotels, all_activities, departure_date, return_date
        )
        
        # Output results
        if not args.no_print:
            print_itinerary(itinerary)
        
        save_itinerary_json(itinerary, args.output)
        
        print("\n✅ Itinerary optimization complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    main()
