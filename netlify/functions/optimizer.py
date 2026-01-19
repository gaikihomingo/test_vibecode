"""
Optimization engine for creating optimal travel itineraries
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ItineraryOptimizer:
    """Optimizes travel itinerary for cost and time"""
    
    def __init__(self, cost_weight: float = 0.6, time_weight: float = 0.4):
        """
        Initialize optimizer
        
        Args:
            cost_weight: Weight for cost optimization (0.0 to 1.0)
            time_weight: Weight for time optimization (0.0 to 1.0)
        """
        if abs(cost_weight + time_weight - 1.0) > 0.01:
            raise ValueError("cost_weight + time_weight must equal 1.0")
        
        self.cost_weight = cost_weight
        self.time_weight = time_weight
    
    def normalize_cost(self, costs: List[float]) -> np.ndarray:
        """Normalize costs to 0-1 scale (lower is better)"""
        if not costs:
            return np.array([])
        
        costs_array = np.array(costs)
        max_cost = np.max(costs_array)
        min_cost = np.min(costs_array)
        
        if max_cost == min_cost:
            return np.ones_like(costs_array)
        
        # Normalize: lower cost = higher score
        normalized = 1 - (costs_array - min_cost) / (max_cost - min_cost)
        return normalized
    
    def normalize_time(self, times: List[float]) -> np.ndarray:
        """Normalize times to 0-1 scale (lower is better)"""
        if not times:
            return np.array([])
        
        times_array = np.array(times)
        max_time = np.max(times_array)
        min_time = np.min(times_array)
        
        if max_time == min_time:
            return np.ones_like(times_array)
        
        # Normalize: lower time = higher score
        normalized = 1 - (times_array - min_time) / (max_time - min_time)
        return normalized
    
    def calculate_score(self, cost: float, time: float, 
                       all_costs: List[float], all_times: List[float]) -> float:
        """Calculate optimization score for a single option"""
        cost_normalized = self.normalize_cost(all_costs)
        time_normalized = self.normalize_time(all_times)
        
        cost_idx = all_costs.index(cost)
        time_idx = all_times.index(time)
        
        cost_score = cost_normalized[cost_idx]
        time_score = time_normalized[time_idx]
        
        return self.cost_weight * cost_score + self.time_weight * time_score
    
    def select_best_flight(self, flights: List[Dict]) -> Dict:
        """Select best flight based on cost and time optimization"""
        if not flights:
            return None
        
        # Extract costs and times
        costs = [f.get("total_price", float('inf')) for f in flights]
        times = [f.get("duration_hours", float('inf')) for f in flights]
        
        # Calculate scores
        scores = []
        for i, flight in enumerate(flights):
            score = self.calculate_score(costs[i], times[i], costs, times)
            scores.append(score)
        
        # Select best option
        best_idx = np.argmax(scores)
        return flights[best_idx]
    
    def select_best_hotel(self, hotels: List[Dict]) -> Dict:
        """Select best hotel based on cost and rating"""
        if not hotels:
            return None
        
        # Extract costs and ratings
        costs = [h.get("total_price", float('inf')) for h in hotels]
        ratings = [h.get("rating", 0) for h in hotels]
        
        # Normalize ratings (higher is better)
        ratings_array = np.array(ratings)
        max_rating = np.max(ratings_array)
        min_rating = np.min(ratings_array)
        
        if max_rating == min_rating:
            rating_scores = np.ones_like(ratings_array)
        else:
            rating_scores = (ratings_array - min_rating) / (max_rating - min_rating)
        
        # Normalize costs (lower is better)
        cost_scores = self.normalize_cost(costs)
        
        # Combine: cost_weight for cost, (1-cost_weight) for rating
        # But we want to balance cost and quality, so use time_weight for rating
        scores = self.cost_weight * cost_scores + self.time_weight * rating_scores
        
        best_idx = np.argmax(scores)
        return hotels[best_idx]
    
    def select_activities(self, activities: List[Dict], 
                         max_activities_per_day: int = 3,
                         max_total_hours: float = 8.0) -> List[Dict]:
        """Select optimal activities for a day using greedy algorithm"""
        if not activities:
            return []
        
        # Sort by value (rating/price ratio)
        activities_with_value = []
        for activity in activities:
            price = activity.get("price_per_person", float('inf'))
            rating = activity.get("rating", 0)
            duration = activity.get("duration_hours", 0)
            
            if price > 0 and duration > 0:
                value_score = (rating * 2) / (price / 50)  # Normalize price
                activities_with_value.append((value_score, activity))
        
        # Sort by value score (descending)
        activities_with_value.sort(key=lambda x: x[0], reverse=True)
        
        # Greedy selection: pick activities that fit in time budget
        selected = []
        total_hours = 0.0
        
        for value_score, activity in activities_with_value:
            duration = activity.get("duration_hours", 0)
            
            if (len(selected) < max_activities_per_day and 
                total_hours + duration <= max_total_hours):
                selected.append(activity)
                total_hours += duration
        
        return selected
    
    def create_itinerary(self, flights: List[Dict], hotels: List[Dict],
                        activities: List[Dict], departure_date: str,
                        return_date: str) -> Dict:
        """
        Create optimized itinerary
        
        Args:
            flights: List of flight options
            hotels: List of hotel options
            activities: List of activity options
            departure_date: Departure date (YYYY-MM-DD)
            return_date: Return date (YYYY-MM-DD)
        
        Returns:
            Dictionary containing optimized itinerary
        """
        logger.info("Creating optimized itinerary...")
        
        # Select best flight
        best_flight = self.select_best_flight(flights)
        
        # Select best hotel
        best_hotel = self.select_best_hotel(hotels)
        
        # Organize activities by date
        departure = datetime.strptime(departure_date, "%Y-%m-%d")
        return_dt = datetime.strptime(return_date, "%Y-%m-%d")
        
        itinerary_days = []
        current_date = departure + timedelta(days=1)  # Start from first full day
        
        total_cost = 0.0
        total_time = 0.0
        
        if best_flight:
            total_cost += best_flight.get("total_price", 0)
            total_time += best_flight.get("duration_hours", 0)
        
        if best_hotel:
            total_cost += best_hotel.get("total_price", 0)
        
        while current_date < return_dt:
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Get activities for this date
            day_activities = [a for a in activities if a.get("date") == date_str]
            selected_activities = self.select_activities(day_activities)
            
            day_cost = sum(a.get("total_price", 0) for a in selected_activities)
            day_time = sum(a.get("duration_hours", 0) for a in selected_activities)
            
            total_cost += day_cost
            total_time += day_time
            
            day_plan = {
                "date": date_str,
                "activities": selected_activities,
                "total_cost": day_cost,
                "total_time_hours": day_time
            }
            itinerary_days.append(day_plan)
            
            current_date += timedelta(days=1)
        
        itinerary = {
            "flight": best_flight,
            "hotel": best_hotel,
            "days": itinerary_days,
            "summary": {
                "total_cost": total_cost,
                "total_time_hours": total_time,
                "duration_days": (return_dt - departure).days,
                "departure_date": departure_date,
                "return_date": return_date
            }
        }
        
        logger.info(f"Itinerary created: Total cost ${total_cost:.2f}, Total time {total_time:.1f} hours")
        
        return itinerary
