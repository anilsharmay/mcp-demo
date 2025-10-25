#!/usr/bin/env python3
"""
Simple test script for the Unsplash search functionality.
This tests the function directly without going through the MCP protocol.
"""

import os
import sys
import json
from dotenv import load_dotenv

# Add the parent directory to the path so we can import from server.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

def test_unsplash_search():
    """Test the unsplash_search function directly."""
    try:
        # Import the function from server.py
        from server import unsplash_search
        
        print("Testing Unsplash search functionality...")
        print("=" * 50)
        
        # Test 1: Search for "nature" photos
        print("\n1. Testing search for 'nature' photos:")
        result = unsplash_search("nature", num_results=3)
        print(result)
        
        # Test 2: Search with orientation filter
        print("\n2. Testing search for 'landscape' photos with orientation filter:")
        result = unsplash_search("landscape", num_results=2, orientation="landscape")
        print(result)
        
        # Test 3: Test error handling (no API key)
        print("\n3. Testing error handling (temporarily remove API key):")
        original_key = os.environ.get("UNSPLASH_API_KEY")
        if original_key:
            del os.environ["UNSPLASH_API_KEY"]
            result = unsplash_search("test")
            print(result)
            # Restore the API key
            os.environ["UNSPLASH_API_KEY"] = original_key
        
        print("\n" + "=" * 50)
        print("Test completed!")
        
    except ImportError as e:
        print(f"Error importing from server.py: {e}")
        print("Make sure server.py is in the same directory and has no syntax errors.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_unsplash_search()
