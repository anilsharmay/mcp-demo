#!/usr/bin/env python3
"""
Search for exactly 5 mountain images using the Unsplash MCP server.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from server.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def search_5_mountains():
    """Search for exactly 5 mountain images."""
    try:
        # Import the function from server.py
        from server import unsplash_search
        
        print("🏔️  Searching for 5 mountain images...")
        print("=" * 50)
        
        # Search for exactly 5 mountains
        result = unsplash_search("mountains", num_results=5)
        
        # Parse the JSON result
        data = json.loads(result)
        
        print(f"Found {data['total']} total mountain images available!")
        print(f"Showing {len(data['photos'])} mountain images:")
        print()
        
        for i, photo in enumerate(data['photos'], 1):
            print(f"{i}. {photo['alt_description'] or 'Mountain landscape'}")
            print(f"   📸 By: {photo['user']['name']} (@{photo['user']['username']})")
            print(f"   ❤️  {photo['likes']} likes")
            print(f"   📐 {photo['width']}x{photo['height']}")
            print(f"   🔗 View: {photo['links']['html']}")
            print(f"   🖼️  Regular size: {photo['urls']['regular']}")
            print()
        
        print("=" * 50)
        print("✅ Found 5 beautiful mountain images!")
        
    except ImportError as e:
        print(f"❌ Error importing from server.py: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON response: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    search_5_mountains()
