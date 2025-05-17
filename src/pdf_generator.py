from fpdf import FPDF
import tempfile
import os
from datetime import datetime

class PDFGenerator:
    """
    Generates PDF files for forklift rental quotes
    """
    
    def __init__(self, quote_info):
        """
        Initialize with quote information
        
        Args:
            quote_info: Dictionary with formatted quote information
        """
        self.quote_info = quote_info
        # Use A4 format
        self.pdf = FPDF(orientation='P', unit='mm', format='A4')
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
        # Use built-in fonts for reliability across environments
        self.pdf.set_font('Helvetica', '', 10)
        
    def generate_pdf(self):
        """
        Generate the PDF document
        
        Returns:
            Path to the generated PDF file
        """
        if not self.quote_info.get('success', False):
            return None
            
        formatted_quote = self.quote_info['formatted_quote']
        
        # Add the first page
        self.pdf.add_page()
        
        # Set colors for elements
        primary_color = (255, 107, 0)  # Orange
        secondary_color = (0, 61, 115)  # Navy blue
        
        # Company info and logo
        self._add_header(formatted_quote['title'], formatted_quote['date'])
        
        # Add quote sections
        self._add_section(formatted_quote['model_info'])
        self._add_section(formatted_quote['rental_info'])
        self._add_section(formatted_quote['pricing_info'])
        self._add_text_section(formatted_quote['recommendations'])
        self._add_text_section(formatted_quote['safety_info'])
        
        # Add terms in a separate page
        self.pdf.add_page()
        self._add_text_section(formatted_quote['terms'], include_full_text=True)
        
        # Add brochure excerpt in a separate page
        self.pdf.add_page()
        self._add_text_section(formatted_quote['brochure'], include_full_text=True)
        
        try:
            # Save the PDF to a temporary file
            temp_dir = tempfile.gettempdir()
            quote_number = formatted_quote['title'].split('#')[-1].strip() if '#' in formatted_quote['title'] else 'quote'
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_path = os.path.join(temp_dir, f"Forklift_Rental_Quote_{quote_number}_{timestamp}.pdf")
            
            self.pdf.output(pdf_path)
            
            # Verify the file was created
            if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                return pdf_path
            else:
                print(f"Error: PDF file was not created properly at {pdf_path}")
                return None
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            return None
    
    def _add_header(self, title, date):
        """Add the header section to the PDF"""
        # Set color for the header
        self.pdf.set_fill_color(0, 61, 115)  # Navy blue
        self.pdf.rect(0, 0, 210, 35, 'F')
        
        # Add company name
        self.pdf.set_font('Helvetica', 'B', 20)
        self.pdf.set_text_color(255, 255, 255)  # White
        self.pdf.cell(0, 15, "Bobcat Forklift Rentals", 0, 1, 'C')
        
        # Add quote title
        self.pdf.set_font('Helvetica', 'B', 16)
        self.pdf.cell(0, 10, title, 0, 1, 'C')
        
        # Add date
        self.pdf.set_font('Helvetica', '', 10)
        self.pdf.set_text_color(0, 0, 0)  # Black
        self.pdf.cell(0, 15, date, 0, 1, 'R')
        
        # Add some space
        self.pdf.ln(5)
    
    def _add_section(self, section_info):
        """Add a table section to the PDF"""
        # Add section title
        self.pdf.set_font('Helvetica', 'B', 14)
        self.pdf.set_fill_color(255, 107, 0)  # Orange
        self.pdf.set_text_color(0, 0, 0)  # Black
        self.pdf.cell(0, 10, section_info['title'], 0, 1, 'L', ln=1)
        
        # Add items as a table
        items = section_info['items']
        self.pdf.set_font('Helvetica', 'B', 10)
        self.pdf.set_fill_color(230, 230, 230)  # Light gray
        
        # Table header
        self.pdf.cell(60, 8, "Item", 1, 0, 'L', 1)
        self.pdf.cell(0, 8, "Value", 1, 1, 'L', 1)
        
        # Table data
        self.pdf.set_font('Helvetica', '', 10)
        for item in items:
            self.pdf.cell(60, 8, item['label'], 1, 0, 'L')
            self.pdf.cell(0, 8, str(item['value']), 1, 1, 'L')
        
        # Add some space
        self.pdf.ln(5)
    
    def _add_text_section(self, section_info, include_full_text=False):
        """Add a text section to the PDF"""
        # Add section title
        self.pdf.set_font('Helvetica', 'B', 14)
        self.pdf.set_fill_color(255, 107, 0)  # Orange
        self.pdf.set_text_color(0, 0, 0)  # Black
        self.pdf.cell(0, 10, section_info['title'], 0, 1, 'L', ln=1)
        
        # Add text content
        self.pdf.set_font('Helvetica', '', 10)
        
        text = section_info['text']
        if not include_full_text and len(text) > 500:
            # Truncate long text for main sections
            text = text[:500] + "..."
            
        # Split text into lines to avoid overflow
        self.pdf.multi_cell(0, 5, text)
        
        # Add some space
        self.pdf.ln(5)
