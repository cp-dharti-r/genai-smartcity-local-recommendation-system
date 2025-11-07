"""
Run the MCP Server (standalone mode)
"""

import asyncio
from mcp_server.server import SmartCityMCPServer


async def main():
    """Run the MCP server in interactive mode"""
    server = SmartCityMCPServer()
    
    print("🏙️ SmartCity MCP Server Started")
    print("=" * 50)
    
    # Initial data fetch
    city = input("Enter city name (default: London): ").strip() or "London"
    country = input("Enter country code (default: GB): ").strip() or "GB"
    
    print(f"\nFetching data for {city}, {country}...")
    data = await server.fetch_all_data(city, country)
    print("✅ Data fetched successfully!")
    
    print("\n" + "=" * 50)
    print("Ask questions about the city (type 'quit' to exit)")
    print("=" * 50)
    
    while True:
        query = input("\nYour question: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if not query:
            continue
        
        response = await server.answer_query(query, city, country)
        print(f"\n📝 Answer: {response['answer']}")
        print(f"\n📊 Relevant Data:")
        print(response.get('relevant_data', {}))


if __name__ == "__main__":
    asyncio.run(main())

