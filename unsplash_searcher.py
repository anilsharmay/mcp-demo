import os
import requests
import json
from typing import Optional, Dict, Any


class UnsplashSearcher:
    """A class for searching photos on Unsplash using their API."""
    
    def __init__(self, api_key: str = None):
        """Initialize the Unsplash searcher with an API key."""
        self.api_key = api_key or os.getenv("UNSPLASH_API_KEY")
        self.base_url = "https://api.unsplash.com"
    
    def search_photos(self, query: str, num_results: int = 10, orientation: Optional[str] = None) -> str:
        """
        Search for photos on Unsplash using the given query.
        
        Args:
            query: Search term for photos
            num_results: Number of photos to return (1-30, default: 10)
            orientation: Filter by orientation - 'landscape', 'portrait', or 'squarish' (optional)
        
        Returns:
            JSON string containing search results with photo URLs and metadata
        """
        if not self.api_key:
            return "Error: UNSPLASH_API_KEY environment variable not set. Please add your Unsplash API key to your .env file."
        
        # Validate num_results parameter
        num_results = max(1, min(30, num_results))
        
        # Build the API URL
        url = f"{self.base_url}/search/photos"
        headers = {
            "Authorization": f"Client-ID {self.api_key}",
            "Accept-Version": "v1"
        }
        
        params = {
            "query": query,
            "per_page": num_results
        }
        
        # Add orientation filter if specified
        if orientation and orientation.strip() and orientation.lower() in ['landscape', 'portrait', 'squarish']:
            params["orientation"] = orientation.lower()
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the results for better readability
            results = {
                "total": data.get("total", 0),
                "total_pages": data.get("total_pages", 0),
                "photos": []
            }
            
            for photo in data.get("results", []):
                photo_info = {
                    "id": photo.get("id"),
                    "description": photo.get("description", "No description"),
                    "alt_description": photo.get("alt_description", "No alt description"),
                    "width": photo.get("width"),
                    "height": photo.get("height"),
                    "color": photo.get("color"),
                    "likes": photo.get("likes"),
                    "urls": {
                        "raw": photo.get("urls", {}).get("raw"),
                        "full": photo.get("urls", {}).get("full"),
                        "regular": photo.get("urls", {}).get("regular"),
                        "small": photo.get("urls", {}).get("small"),
                        "thumb": photo.get("urls", {}).get("thumb")
                    },
                    "user": {
                        "name": photo.get("user", {}).get("name"),
                        "username": photo.get("user", {}).get("username"),
                        "portfolio_url": photo.get("user", {}).get("portfolio_url")
                    },
                    "links": {
                        "html": photo.get("links", {}).get("html"),
                        "download": photo.get("links", {}).get("download")
                    }
                }
                results["photos"].append(photo_info)
            
            return json.dumps(results, indent=2)
            
        except requests.exceptions.RequestException as e:
            return f"Error making request to Unsplash API: {str(e)}"
        except json.JSONDecodeError as e:
            return f"Error parsing response from Unsplash API: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


if __name__ == "__main__":
    # Test the UnsplashSearcher
    searcher = UnsplashSearcher()
    result = searcher.search_photos("mountains", 5)
    print(result)
