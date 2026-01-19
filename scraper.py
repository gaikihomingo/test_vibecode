"""
Web scraper for travel websites
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TravelScraper:
    """Base class for scraping travel websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.driver = None
    
    def _init_selenium(self):
        """Initialize Selenium WebDriver"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def _close_selenium(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def scrape_flights(self, origin: str, destination: str, 
                      departure_date: str, return_date: str, 
                      travelers: int = 2) -> List[Dict]:
        """Scrape flight data - to be implemented by subclasses"""
        raise NotImplementedError
    
    def scrape_hotels(self, destination: str, check_in: str, 
                     check_out: str, travelers: int = 2) -> List[Dict]:
        """Scrape hotel data - to be implemented by subclasses"""
        raise NotImplementedError
    
    def scrape_activities(self, destination: str, date: str) -> List[Dict]:
        """Scrape activity data - to be implemented by subclasses"""
        raise NotImplementedError


class MockTravelScraper(TravelScraper):
    """
    Mock scraper that generates realistic sample data
    In production, this would be replaced with actual scrapers for each website
    """
    
    def scrape_flights(self, origin: str, destination: str, 
                      departure_date: str, return_date: str, 
                      travelers: int = 2) -> List[Dict]:
        """Generate mock flight data"""
        logger.info(f"Scraping flights: {origin} -> {destination}")
        
        # Mock flight data with variations
        flights = []
        airlines = ["Delta", "United", "American", "Lufthansa", "Air France", 
                   "British Airways", "KLM", "Emirates", "Qatar", "Turkish"]
        
        base_price = 800
        for i, airline in enumerate(airlines[:10]):
            price_variation = (i * 50) + (hash(f"{origin}{destination}") % 200)
            duration_variation = 30 + (i * 15)
            
            flight = {
                "airline": airline,
                "origin": origin,
                "destination": destination,
                "departure_time": f"{8 + (i % 12)}:00",
                "arrival_time": f"{14 + (i % 10)}:00",
                "duration_hours": 7.5 + (duration_variation / 60),
                "price_per_person": base_price + price_variation,
                "total_price": (base_price + price_variation) * travelers,
                "stops": 0 if i < 5 else 1,
                "class": "Economy",
                "source": "mock_data"
            }
            flights.append(flight)
        
        return flights
    
    def scrape_hotels(self, destination: str, check_in: str, 
                     check_out: str, travelers: int = 2) -> List[Dict]:
        """Generate mock hotel data"""
        logger.info(f"Scraping hotels in {destination}")
        
        hotels = []
        hotel_names = [
            "Grand Plaza Hotel", "Oceanview Resort", "City Center Inn",
            "Luxury Suites", "Budget Stay", "Boutique Hotel", "Beachfront Villa",
            "Mountain View Lodge", "Historic Manor", "Modern Apartment"
        ]
        
        base_price = 120
        check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
        check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
        nights = (check_out_date - check_in_date).days
        
        for i, name in enumerate(hotel_names):
            price_variation = (i * 30) + (hash(destination) % 100)
            rating = 3.5 + (i * 0.3)
            
            hotel = {
                "name": name,
                "destination": destination,
                "check_in": check_in,
                "check_out": check_out,
                "nights": nights,
                "price_per_night": base_price + price_variation,
                "total_price": (base_price + price_variation) * nights,
                "rating": min(5.0, rating),
                "amenities": ["WiFi", "Breakfast", "Pool"] if i < 5 else ["WiFi"],
                "location": "City Center" if i % 2 == 0 else "Airport Area",
                "source": "mock_data"
            }
            hotels.append(hotel)
        
        return hotels
    
    def scrape_activities(self, destination: str, date: str) -> List[Dict]:
        """Generate mock activity data"""
        logger.info(f"Scraping activities in {destination}")
        
        activities = []
        activity_names = [
            "City Tour", "Museum Visit", "Cooking Class", "Wine Tasting",
            "Boat Cruise", "Hiking Tour", "Food Tour", "Photography Walk",
            "Sunset Viewing", "Local Market"
        ]
        
        base_price = 50
        for i, name in enumerate(activity_names):
            price_variation = (i * 15) + (hash(f"{destination}{name}") % 50)
            duration_variation = 2 + (i * 0.5)
            
            activity = {
                "name": name,
                "destination": destination,
                "date": date,
                "duration_hours": duration_variation,
                "price_per_person": base_price + price_variation,
                "total_price": (base_price + price_variation) * 2,  # For couple
                "category": ["Sightseeing", "Food", "Adventure", "Culture"][i % 4],
                "rating": 4.0 + (i * 0.1),
                "source": "mock_data"
            }
            activities.append(activity)
        
        return activities


class MultiSiteScraper:
    """Scraper that aggregates data from multiple travel websites"""
    
    def __init__(self, websites: List[str]):
        self.websites = websites
        self.scrapers = {}
        
        # Initialize mock scrapers for each website
        # In production, each would have its own implementation
        for site in websites:
            self.scrapers[site] = MockTravelScraper()
    
    def scrape_all_flights(self, origin: str, destination: str,
                          departure_date: str, return_date: str,
                          travelers: int = 2) -> List[Dict]:
        """Scrape flights from all configured websites"""
        all_flights = []
        
        for site_name, scraper in self.scrapers.items():
            try:
                logger.info(f"Scraping flights from {site_name}")
                flights = scraper.scrape_flights(
                    origin, destination, departure_date, return_date, travelers
                )
                # Tag each flight with its source
                for flight in flights:
                    flight["source_website"] = site_name
                all_flights.extend(flights)
                time.sleep(1)  # Be respectful with requests
            except Exception as e:
                logger.error(f"Error scraping {site_name}: {e}")
        
        return all_flights
    
    def scrape_all_hotels(self, destination: str, check_in: str,
                         check_out: str, travelers: int = 2) -> List[Dict]:
        """Scrape hotels from all configured websites"""
        all_hotels = []
        
        for site_name, scraper in self.scrapers.items():
            try:
                logger.info(f"Scraping hotels from {site_name}")
                hotels = scraper.scrape_hotels(destination, check_in, check_out, travelers)
                for hotel in hotels:
                    hotel["source_website"] = site_name
                all_hotels.extend(hotels)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error scraping {site_name}: {e}")
        
        return all_hotels
    
    def scrape_all_activities(self, destination: str, date: str) -> List[Dict]:
        """Scrape activities from all configured websites"""
        all_activities = []
        
        for site_name, scraper in self.scrapers.items():
            try:
                logger.info(f"Scraping activities from {site_name}")
                activities = scraper.scrape_activities(destination, date)
                for activity in activities:
                    activity["source_website"] = site_name
                all_activities.extend(activities)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error scraping {site_name}: {e}")
        
        return all_activities
    
    def cleanup(self):
        """Clean up resources"""
        for scraper in self.scrapers.values():
            scraper._close_selenium()
