import base64
import os
import tempfile
from datetime import datetime
import webbrowser
from pathlib import Path
import html

class PDFGenerator:
    """
    Generates PDF files for forklift rental quotes using HTML
    """
    
    def __init__(self, quote_info):
        """
        Initialize with quote information
        
        Args:
            quote_info: Dictionary with formatted quote information
        """
        self.quote_info = quote_info
        
    def get_html_string(self):
        """
        Generate HTML representation of the quote
        
        Returns:
            HTML string
        """
        if not self.quote_info.get('success', False):
            return None
            
        formatted_quote = self.quote_info['formatted_quote']
        
        # Start HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{formatted_quote['title']}</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    line-height: 1.6;
                }}
                .header {{
                    background-color: #003D73;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .section {{
                    margin-bottom: 20px;
                    border-bottom: 1px solid #E0E0E0;
                    padding-bottom: 20px;
                }}
                .section h2 {{
                    color: #003D73;
                    border-left: 5px solid #FF6B00;
                    padding-left: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                table, th, td {{
                    border: 1px solid #E0E0E0;
                }}
                th {{
                    background-color: #003D73;
                    color: white;
                    text-align: left;
                    padding: 10px;
                }}
                td {{
                    padding: 10px;
                }}
                .date {{
                    text-align: right;
                    margin-top: 10px;
                }}
                @media print {{
                    body {{ 
                        margin: 0; 
                        padding: 10px;
                    }}
                    .no-print {{ 
                        display: none; 
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Bobcat Forklift Rentals</h1>
                <h2>{formatted_quote['title']}</h2>
                <div class="date">{formatted_quote['date']}</div>
            </div>
        """
        
        # Add Forklift Model Information
        html_content += f"""
            <div class="section">
                <h2>{formatted_quote['model_info']['title']}</h2>
                <table>
                    <tr>
                        <th>Item</th>
                        <th>Value</th>
                    </tr>
        """
        
        for item in formatted_quote['model_info']['items']:
            html_content += f"""
                    <tr>
                        <td>{html.escape(item['label'])}</td>
                        <td>{html.escape(str(item['value']))}</td>
                    </tr>
            """
            
        html_content += """
                </table>
            </div>
        """
        
        # Add Rental Information
        html_content += f"""
            <div class="section">
                <h2>{formatted_quote['rental_info']['title']}</h2>
                <table>
                    <tr>
                        <th>Item</th>
                        <th>Value</th>
                    </tr>
        """
        
        for item in formatted_quote['rental_info']['items']:
            html_content += f"""
                    <tr>
                        <td>{html.escape(item['label'])}</td>
                        <td>{html.escape(str(item['value']))}</td>
                    </tr>
            """
            
        html_content += """
                </table>
            </div>
        """
        
        # Add Pricing Information
        html_content += f"""
            <div class="section">
                <h2>{formatted_quote['pricing_info']['title']}</h2>
                <table>
                    <tr>
                        <th>Item</th>
                        <th>Value</th>
                    </tr>
        """
        
        for item in formatted_quote['pricing_info']['items']:
            html_content += f"""
                    <tr>
                        <td>{html.escape(item['label'])}</td>
                        <td>{html.escape(str(item['value']))}</td>
                    </tr>
            """
            
        html_content += """
                </table>
            </div>
        """
        
        # Add Recommendations and Safety Information
        html_content += f"""
            <div class="section">
                <h2>{formatted_quote['recommendations']['title']}</h2>
                <p>{html.escape(formatted_quote['recommendations']['text'])}</p>
            </div>
            
            <div class="section">
                <h2>{formatted_quote['safety_info']['title']}</h2>
                <p>{html.escape(formatted_quote['safety_info']['text'])}</p>
            </div>
        """
        
        # Add Terms and Conditions - Fix the backslash issue by using a function
        terms_text = formatted_quote['terms']['text']
        terms_text_html = html.escape(terms_text).replace("\n", "<br>")
        
        html_content += f"""
            <div class="section">
                <h2>{formatted_quote['terms']['title']}</h2>
                <p>{terms_text_html}</p>
            </div>
        """
        
        # Add Specifications - Fix the backslash issue by using a function
        brochure_text = formatted_quote['brochure']['text']
        brochure_text_html = html.escape(brochure_text).replace("\n", "<br>")
        
        html_content += f"""
            <div class="section">
                <h2>{formatted_quote['brochure']['title']}</h2>
                <p>{brochure_text_html}</p>
            </div>
        """
        
        # Close HTML
        html_content += """
            <div class="no-print">
                <p>To print this quote, please use your browser's print functionality.</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def generate_html_file(self):
        """
        Generate an HTML file for the quote
        
        Returns:
            Path to the HTML file
        """
        html_content = self.get_html_string()
        if not html_content:
            return None
            
        try:
            formatted_quote = self.quote_info['formatted_quote']
            
            # Create a unique filename
            quote_number = formatted_quote['title'].split('#')[-1].strip() if '#' in formatted_quote['title'] else 'quote'
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            html_filename = f"Forklift_Rental_Quote_{quote_number}_{timestamp}.html"
            
            # Save to temp directory
            temp_dir = tempfile.gettempdir()
            html_path = os.path.join(temp_dir, html_filename)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return html_path
        except Exception as e:
            print(f"Error generating HTML file: {str(e)}")
            return None
    
    def get_html_as_base64(self):
        """
        Generate the HTML and return it as a base64 encoded string
        
        Returns:
            Base64 encoded HTML string
        """
        html_content = self.get_html_string()
        if not html_content:
            return None
            
        try:
            # Convert HTML to base64
            b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
            return b64
        except Exception as e:
            print(f"Error generating HTML as base64: {str(e)}")
            return None