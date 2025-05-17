import streamlit as st
import os
import base64
from pathlib import Path

class UIComponents:
    """
    Reusable UI components for the Streamlit interface
    """
    
    @staticmethod
    def load_css():
        """Load CSS styles from the css/main.css file"""
        css_file = Path(__file__).parent.parent / "css" / "main.css"
        
        if css_file.exists():
            with open(css_file) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    @staticmethod
    def display_header():
        """Display the application header"""
        st.markdown(
            """
            <div class="header">
                <h1>Forklift Rental Inquiry Agent</h1>
                <div class="header-description">
                    Welcome to our Forklift Rental Inquiry Agent. This tool will help you find the right 
                    forklift for your needs and provide you with a detailed quote.
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    @staticmethod
    def display_conversation(conversation_manager):
        """
        Display the conversation interface
        
        Args:
            conversation_manager: Instance of ConversationManager
            
        Returns:
            User's answer to the current question, or None if no answer provided
        """
        # Initialize session state for conversation
        if 'messages' not in st.session_state:
            st.session_state.messages = []
            
            # Add initial message
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Hello! I'll help you find the right forklift for your needs. Let's start with a few questions."
            })
            
            # Add first question
            current_question = conversation_manager.get_current_question()
            question_text = current_question['question']
            
            # Add options if available
            if 'options' in current_question:
                options_text = ', '.join(current_question['options'])
                question_text += f" ({options_text})"
                
            st.session_state.messages.append({
                "role": "assistant",
                "content": question_text
            })
        
        # Display conversation history
        for message in st.session_state.messages:
            message_class = "assistant-message" if message["role"] == "assistant" else "user-message"
            st.markdown(f'<div class="chat-message {message_class}">{message["content"]}</div>', unsafe_allow_html=True)
        
        # Get user input if conversation isn't complete
        if not conversation_manager.is_complete():
            user_input = st.chat_input("Your answer")
            
            if user_input:
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": user_input})
                
                # Process the answer
                is_valid, feedback = conversation_manager.process_answer(user_input)
                
                # Add assistant's response to chat history
                st.session_state.messages.append({"role": "assistant", "content": feedback})
                
                # Force a page refresh to update the display
                st.rerun()
                
            return user_input
        
        return None
    
    @staticmethod
    def create_download_link_from_html(html_content, file_name):
        """
        Create a download link for HTML content
        
        Args:
            html_content: HTML content as a string
            file_name: File name for download
            
        Returns:
            Download link markup
        """
        b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        
        # Create standard download link
        href = f'data:text/html;charset=utf-8;base64,{b64}'
        download_link = f'<a href="{href}" download="{file_name}" target="_blank"><button style="background-color: #4CAF50; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">Download Quote as HTML</button></a>'
        
        download_html = f"""
            <div style="text-align: center; margin: 20px 0;">
                {download_link}
            </div>
        """
        return download_html
    
    @staticmethod
    def display_quote(quote_info):
        """
        Display the generated quote
        
        Args:
            quote_info: Dictionary with formatted quote information
        """
        if not quote_info.get('success', False):
            st.markdown(
                f'<div class="warning-box">{quote_info.get("message", "Unable to generate quote.")}</div>',
                unsafe_allow_html=True
            )
            return
        
        formatted_quote = quote_info['formatted_quote']
        
        # Display the quote header
        st.markdown(
            f"""
            <div class="quote-container">
                <div class="quote-header">
                    <h2>{formatted_quote['title']}</h2>
                    <p>{formatted_quote['date']}</p>
                </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display model information
        st.markdown(f'<div class="quote-section"><h3>{formatted_quote["model_info"]["title"]}</h3>', unsafe_allow_html=True)
        model_data = {item['label']: item['value'] for item in formatted_quote['model_info']['items']}
        st.table(model_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display rental information
        st.markdown(f'<div class="quote-section"><h3>{formatted_quote["rental_info"]["title"]}</h3>', unsafe_allow_html=True)
        rental_data = {item['label']: item['value'] for item in formatted_quote['rental_info']['items']}
        st.table(rental_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display pricing information
        st.markdown(f'<div class="quote-section"><h3>{formatted_quote["pricing_info"]["title"]}</h3>', unsafe_allow_html=True)
        pricing_data = {item['label']: item['value'] for item in formatted_quote['pricing_info']['items']}
        st.table(pricing_data)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display recommendations
        st.markdown(
            f"""
            <div class="quote-section">
                <h3>{formatted_quote['recommendations']['title']}</h3>
                <p>{formatted_quote['recommendations']['text']}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display safety information
        st.markdown(
            f"""
            <div class="quote-section">
                <h3>{formatted_quote['safety_info']['title']}</h3>
                <p>{formatted_quote['safety_info']['text']}</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Display brochure information in an expandable section
        with st.expander("View Forklift Specifications"):
            st.markdown(formatted_quote['brochure']['text'])
        
        # Display terms and conditions in an expandable section
        with st.expander("View Terms & Conditions"):
            st.markdown(formatted_quote['terms']['text'])
        
        # Add a button to save the quote as HTML
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Store the quote info in session state for HTML generation
        if 'current_quote' not in st.session_state:
            st.session_state.current_quote = quote_info
        
        if st.button("Generate Quote Document"):
            with st.spinner("Generating document..."):
                try:
                    # Import the HTML generator
                    from src.html_pdf_generator import PDFGenerator
                    
                    # Create generator
                    generator = PDFGenerator(st.session_state.current_quote)
                    
                    # Get HTML content
                    html_content = generator.get_html_string()
                    
                    if html_content:
                        # Create a download link
                        quote_number = formatted_quote['title'].split('#')[-1].strip() if '#' in formatted_quote['title'] else 'quote'
                        file_name = f"Forklift_Rental_Quote_{quote_number}.html"
                        
                        download_html = UIComponents.create_download_link_from_html(html_content, file_name)
                        st.markdown(download_html, unsafe_allow_html=True)
                        
                        # Add a note about how to convert to PDF
                        st.info("After downloading the HTML file, you can open it in any web browser and use the browser's print function to save it as a PDF.")
                    else:
                        st.error("Failed to generate document. Please try again.")
                except Exception as e:
                    st.error(f"Error generating document: {str(e)}")
    
    @staticmethod
    def display_restart_button():
        """Display a button to restart the conversation"""
        return st.button("Start a New Inquiry")
    
    @staticmethod
    def display_loading_state(text="Processing your request..."):
        """
        Display a loading state with custom text
        
        Args:
            text: The text to display during loading
        """
        with st.spinner(text):
            st.empty()
    
    @staticmethod
    def display_error(message):
        """
        Display an error message
        
        Args:
            message: The error message to display
        """
        st.markdown(
            f'<div class="warning-box">{message}</div>',
            unsafe_allow_html=True
        )
    
    @staticmethod
    def display_info(message):
        """
        Display an informational message
        
        Args:
            message: The info message to display
        """
        st.markdown(
            f'<div class="info-box">{message}</div>',
            unsafe_allow_html=True
        )