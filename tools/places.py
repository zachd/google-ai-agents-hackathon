import os
import requests
from typing import Dict, Any, Optional, List

def find_nearby_places(query: str, location: Optional[str] = None, radius: int = 5000, max_results: int = 10) -> Dict[str, Any]:
    """
    Find nearby places using Google Places API.
    
    Args:
        query: The type of place to search for (e.g., "art gallery", "local secrets", "hidden gems")
        location: Optional location string (e.g., "New York, NY"). If not provided, user's current location will be used.
        radius: Search radius in meters (default 5000)
        max_results: Maximum number of places to return (default 10)
    
    Returns:
        Dictionary with place details including name, address, coordinates, place_id, map_url, and photos.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"error": "GOOGLE_API_KEY not set in environment variables"}
    
    places_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    # Build the query string
    search_query = query
    if location:
        search_query = f"{query} in {location}"
    
    params = {
        "query": search_query,
        "radius": radius,
        "key": api_key,
    }
    
    try:
        response = requests.get(places_url, params=params)
        response.raise_for_status()
        place_data = response.json()
        
        if not place_data.get("results"):
            return {"error": "No places found", "places": []}
        
        # Return multiple places (up to max_results)
        results = []
        for place in place_data.get("results", [])[:max_results]:
            place_id = place.get("place_id")
            name = place.get("name")
            address = place.get("formatted_address")
            geometry = place.get("geometry", {})
            location_data = geometry.get("location", {})
            
            # Build map URL
            map_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            
            # Get photos if available
            photos = []
            for photo in place.get("photos", [])[:2]:  # First 2 photos
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo.get('photo_reference')}&key={api_key}"
                photos.append(photo_url)
            
            # Build map URL using GPS coordinates
            lat = location_data.get("lat")
            lng = location_data.get("lng")
            map_url_gps = f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
            
            results.append({
                "name": name,
                "address": address,
                "lat": lat,
                "lng": lng,
                "place_id": place_id,
                "map_url": map_url_gps,
                "photos": photos,
                "rating": place.get("rating"),
                "types": place.get("types", []),
            })
        
        return {"places": results, "count": len(results)}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching places data: {str(e)}"}

