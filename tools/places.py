import os
import requests
from typing import Dict, Any, Optional

def find_nearby_places(query: str, location: Optional[str] = None, radius: int = 5000) -> Dict[str, Any]:
    """
    Find nearby places using Google Places API.
    
    Args:
        query: The type of place to search for (e.g., "art gallery", "local secrets", "hidden gems")
        location: Optional location string (e.g., "New York, NY"). If not provided, user's current location will be used.
        radius: Search radius in meters (default 5000)
    
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
        
        # Return multiple places (top 5)
        results = []
        for place in place_data.get("results", [])[:5]:
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
            
            results.append({
                "name": name,
                "address": address,
                "lat": location_data.get("lat"),
                "lng": location_data.get("lng"),
                "place_id": place_id,
                "map_url": map_url,
                "photos": photos,
                "rating": place.get("rating"),
                "types": place.get("types", []),
            })
        
        return {"places": results, "count": len(results)}
        
    except requests.exceptions.RequestException as e:
        return {"error": f"Error fetching places data: {str(e)}"}

