from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
import requests
import json
from typing import Optional
from dice_roller import DiceRoller

load_dotenv()

mcp = FastMCP("mcp-server")
client = TavilyClient(os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for information about the given query"""
    search_results = client.get_search_context(query=query)
    return search_results

@mcp.tool()
def roll_dice(notation: str, num_rolls: int = 1) -> str:
    """Roll the dice with the given notation"""
    roller = DiceRoller(notation, num_rolls)
    return str(roller)

@mcp.tool()
def unsplash_search(query: str, num_results: int = 10, orientation: Optional[str] = None) -> str:
    """
    Search for photos on Unsplash using the given query.
    
    Args:
        query: Search term for photos
        num_results: Number of photos to return (1-30, default: 10)
        orientation: Filter by orientation - 'landscape', 'portrait', or 'squarish' (optional)
    
    Returns:
        JSON string containing search results with photo URLs and metadata
    """
    unsplash_api_key = os.getenv("UNSPLASH_API_KEY")
    if not unsplash_api_key:
        return "Error: UNSPLASH_API_KEY environment variable not set. Please add your Unsplash API key to your .env file."
    
    # Validate num_results parameter
    num_results = max(1, min(30, num_results))
    
    # Build the API URL
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {unsplash_api_key}",
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
    mcp.run(transport="stdio")