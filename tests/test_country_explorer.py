#!/usr/bin/env python3
"""
Test Country Explorer LangGraph App

A simple test version that doesn't require interactive input.
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

async def test_country_explorer():
    """Test the Country Explorer with a simple example"""
    print("🌍 Testing Country Explorer LangGraph App")
    print("=" * 50)
    
    try:
        # Get tools from your MCP server
        print("🔧 Connecting to MCP server...")
        tools = await client.get_tools()
        print(f"✅ Discovered {len(tools)} tools from MCP server:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Create the graph
        def call_model(state: MessagesState):
            """Call the model with available tools"""
            response = model.bind_tools(tools).invoke(state["messages"])
            return {"messages": response}
        
        builder = StateGraph(MessagesState)
        builder.add_node("call_model", call_model)
        builder.add_node("tools", ToolNode(tools))
        builder.add_edge(START, "call_model")
        builder.add_conditional_edges(
            "call_model",
            tools_condition,
        )
        builder.add_edge("tools", "call_model")
        
        graph = builder.compile()
        
        # Test with a simple country
        print("\n🔍 Testing with 'India'...")
        result = await graph.ainvoke({
            "messages": "Research India and create a brief markdown profile with facts and images. Use web_search to get information about India's culture and geography. Then use unsplash_search to find 2 beautiful images of India. Format as clean markdown with embedded images - do NOT wrap in code blocks or use ```markdown``` syntax."
        })
        
        print("\n" + "="*60)
        print("📄 RESULT:")
        print("="*60)
        print(result["messages"][-1].content)
        print("="*60)
        
        # Save the result to a markdown file
        filename = "profiles/india_profile.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result["messages"][-1].content)
        
        print(f"\n💾 Saved India profile to: {filename}")
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure your MCP server is running with: uv run mcp dev server.py")

if __name__ == "__main__":
    asyncio.run(test_country_explorer())
