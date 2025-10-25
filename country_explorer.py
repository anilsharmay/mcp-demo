#!/usr/bin/env python3
"""
Country Explorer LangGraph App

A LangGraph application that uses MCP tools to research countries
and create beautiful markdown profiles with embedded images.
"""

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

# Initialize the chat model
model = ChatOpenAI(model="gpt-4o-mini")

# Create MCP client to connect to your server
client = MultiServerMCPClient(
    {
        "unsplash-mcp-server": {
            "command": "uv",
            "args": ["--directory", ".", "run", "server.py"],
            "transport": "stdio",
        }
    }
)

async def create_country_explorer_graph():
    """Create the Country Explorer LangGraph app"""
    
    # Get tools from your MCP server
    tools = await client.get_tools()
    print(f"🔧 Discovered {len(tools)} tools from MCP server:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description}")
    
    def call_model(state: MessagesState):
        """Call the model with available tools"""
        response = model.bind_tools(tools).invoke(state["messages"])
        return {"messages": response}
    
    # Create the graph
    builder = StateGraph(MessagesState)
    
    # Add nodes
    builder.add_node("call_model", call_model)
    builder.add_node("tools", ToolNode(tools))
    
    # Add edges
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    
    return builder.compile()

async def explore_country(country_name: str):
    """Explore a country using the LangGraph app"""
    print(f"🌍 Starting exploration of {country_name}...")
    
    graph = await create_country_explorer_graph()
    
    result = await graph.ainvoke({
        "messages": f"Research {country_name} and create a beautiful markdown profile with facts and images. Use web_search to get information about {country_name}'s culture, geography, and history. Then use unsplash_search to find 10 beautiful images of {country_name}. Format as clean markdown with embedded images - do NOT wrap in code blocks or use ```markdown``` syntax."
    })
    
    return result["messages"][-1].content

def save_country_profile(country: str, markdown_content: str):
    """Save the country profile as a markdown file"""
    import os
    os.makedirs("profiles", exist_ok=True)
    filename = f"profiles/{country.lower().replace(' ', '_')}_profile.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"📄 Saved {country} profile to: {filename}")

async def main():
    """Main app function"""
    print("🌍 Country Explorer LangGraph App")
    print("=" * 50)
    print("This app will research countries and create beautiful profiles with images!")
    print("Make sure your MCP server is running with: uv run mcp dev server.py")
    print()
    
    while True:
        country = input("Enter a country name (or 'quit' to exit): ").strip()
        
        if country.lower() in ['quit', 'exit', 'q']:
            print("👋 Happy exploring!")
            break
            
        if not country:
            print("Please enter a country name.")
            continue
            
        print(f"\n🔍 Exploring {country}...")
        
        try:
            result = await explore_country(country)
            print("\n" + "="*60)
            print(result)
            print("="*60)
            
            # Ask if user wants to save
            save = input(f"\n💾 Save {country} profile as markdown file? (y/n): ").strip().lower()
            if save in ['y', 'yes']:
                save_country_profile(country, result)
                
        except Exception as e:
            print(f"❌ Error exploring {country}: {str(e)}")
            print("Make sure your MCP server is running!")

if __name__ == "__main__":
    asyncio.run(main())
