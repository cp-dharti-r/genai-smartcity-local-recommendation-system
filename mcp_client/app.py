"""
Streamlit UI for MCP Client
"""

import streamlit as st
import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.server import SmartCityMCPServer


# Initialize session state
if "mcp_server" not in st.session_state:
    st.session_state.mcp_server = SmartCityMCPServer()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_city" not in st.session_state:
    st.session_state.current_city = "London"

if "current_country" not in st.session_state:
    st.session_state.current_country = "GB"


def run_async(coro):
    """Helper to run async functions in Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


def main():
    st.set_page_config(
        page_title="SmartCity Local Recommendation System",
        page_icon="🏙️",
        layout="wide"
    )
    
    st.title("🏙️ SmartCity Local Recommendation System")
    st.markdown("Ask questions about weather, traffic, temperature, and shop offers in your city!")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        city = st.text_input("City", value=st.session_state.current_city)
        country = st.text_input("Country Code", value=st.session_state.current_country, max_chars=2)
        
        if st.button("Update City"):
            st.session_state.current_city = city
            st.session_state.current_country = country
            st.success(f"City updated to {city}, {country}")
        
        st.divider()
        
        if st.button("🔄 Refresh Data"):
            with st.spinner("Fetching latest city data..."):
                data = run_async(
                    st.session_state.mcp_server.fetch_all_data(
                        st.session_state.current_city,
                        st.session_state.current_country
                    )
                )
                st.success("Data refreshed successfully!")
        
        st.divider()
        
        # Show context summary
        st.subheader("📊 Context Summary")
        summary = st.session_state.mcp_server.get_context_summary()
        st.json(summary)
    
    # Main chat interface
    st.header("💬 Ask Questions")
    
    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
            # Show relevant data if available
            if "relevant_data" in message and message["relevant_data"]:
                with st.expander("View Details"):
                    st.json(message["relevant_data"])
    
    # Chat input
    user_query = st.chat_input("Ask about weather, traffic, temperature, or shop offers...")
    
    if user_query:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_query
        })
        
        # Get answer from MCP server
        with st.spinner("Thinking..."):
            response = run_async(
                st.session_state.mcp_server.answer_query(
                    user_query,
                    st.session_state.current_city,
                    st.session_state.current_country
                )
            )
        
        # Add assistant response to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response["answer"],
            "relevant_data": response.get("relevant_data", {})
        })
        
        # Rerun to show new messages
        st.rerun()
    
    # Quick action buttons
    st.divider()
    st.subheader("🚀 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🌤️ Weather"):
            query = "What's the weather like?"
            st.session_state.chat_history.append({"role": "user", "content": query})
            response = run_async(
                st.session_state.mcp_server.answer_query(
                    query,
                    st.session_state.current_city,
                    st.session_state.current_country
                )
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response["answer"],
                "relevant_data": response.get("relevant_data", {})
            })
            st.rerun()
    
    with col2:
        if st.button("🌡️ Temperature"):
            query = "What's the temperature?"
            st.session_state.chat_history.append({"role": "user", "content": query})
            response = run_async(
                st.session_state.mcp_server.answer_query(
                    query,
                    st.session_state.current_city,
                    st.session_state.current_country
                )
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response["answer"],
                "relevant_data": response.get("relevant_data", {})
            })
            st.rerun()
    
    with col3:
        if st.button("🚗 Traffic"):
            query = "How's the traffic?"
            st.session_state.chat_history.append({"role": "user", "content": query})
            response = run_async(
                st.session_state.mcp_server.answer_query(
                    query,
                    st.session_state.current_city,
                    st.session_state.current_country
                )
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response["answer"],
                "relevant_data": response.get("relevant_data", {})
            })
            st.rerun()
    
    with col4:
        if st.button("🛍️ Shop Offers"):
            query = "What shop offers are available?"
            st.session_state.chat_history.append({"role": "user", "content": query})
            response = run_async(
                st.session_state.mcp_server.answer_query(
                    query,
                    st.session_state.current_city,
                    st.session_state.current_country
                )
            )
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response["answer"],
                "relevant_data": response.get("relevant_data", {})
            })
            st.rerun()


if __name__ == "__main__":
    main()

