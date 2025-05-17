import streamlit as st
import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from src.data_loader import ForkliftData
from src.matcher import ForkliftMatcher
from src.conversation import ConversationManager
from src.quote import QuoteGenerator
from src.ui_components import UIComponents

def main():
    """Main application entry point"""
    # Set page config
    st.set_page_config(
        page_title="Forklift Rental Inquiry Agent",
        page_icon="🚜",
        layout="wide",
    )
    
    # Load CSS
    UIComponents.load_css()
    
    # Display header
    UIComponents.display_header()
    
    # Initialize session state
    if 'conversation_manager' not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    
    if 'forklift_data' not in st.session_state:
        st.session_state.forklift_data = ForkliftData()
    
    if 'matcher' not in st.session_state:
        st.session_state.matcher = ForkliftMatcher(st.session_state.forklift_data)
    
    if 'quote_generator' not in st.session_state:
        st.session_state.quote_generator = QuoteGenerator(st.session_state.forklift_data)
    
    if 'quote_displayed' not in st.session_state:
        st.session_state.quote_displayed = False
    
    # Handle restart button
    if UIComponents.display_restart_button():
        # Reset the conversation
        st.session_state.conversation_manager.reset()
        st.session_state.quote_displayed = False
        
        # Clear messages to force reinitialization
        if 'messages' in st.session_state:
            del st.session_state.messages
            
        # Clear quote data
        if 'current_quote' in st.session_state:
            del st.session_state.current_quote
        if 'current_formatted_quote' in st.session_state:
            del st.session_state.current_formatted_quote
            
        # Rerun the app to refresh the UI
        st.rerun()
    
    # Display the conversation interface
    UIComponents.display_conversation(st.session_state.conversation_manager)
    
    # If conversation is complete, handle quote generation and display
    if st.session_state.conversation_manager.is_complete():
        # Generate the quote only once if not already generated
        if not st.session_state.quote_displayed:
            with st.spinner("Generating your forklift rental quote..."):
                # Get the gathered requirements
                requirements = st.session_state.conversation_manager.get_requirements()
                
                # Match requirements to a forklift
                forklift_match = st.session_state.matcher.match_forklift(requirements)
                
                # Generate a quote
                quote_result = st.session_state.quote_generator.generate_quote(forklift_match)
                
                # Format the quote for display
                formatted_quote = st.session_state.quote_generator.format_quote_for_display(quote_result)
                
                # Store the quote result in session state
                st.session_state.current_formatted_quote = formatted_quote
                
                # Set the quote as displayed
                st.session_state.quote_displayed = True
        
        # Display the quote - always do this if conversation is complete,
        # even after button clicks or page refreshes
        if 'current_formatted_quote' in st.session_state:
            UIComponents.display_quote(st.session_state.current_formatted_quote)

if __name__ == "__main__":
    main()
