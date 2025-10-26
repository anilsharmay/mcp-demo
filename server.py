from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from typing import Optional
from dice_roller import DiceRoller
from unsplash_searcher import UnsplashSearcher

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
    """Search for photos on Unsplash using the given query."""
    searcher = UnsplashSearcher()
    return searcher.search_photos(query, num_results, orientation)

if __name__ == "__main__":
    mcp.run(transport="stdio")