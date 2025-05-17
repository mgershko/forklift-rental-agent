import unittest
import sys
import os
import datetime
from pathlib import Path

# Add the parent directory to the path to import the application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.quote import QuoteGenerator
from src.data_loader import ForkliftData

class TestQuoteGenerator(unittest.TestCase):
    """Test cases for the QuoteGenerator class"""
    
    def setUp(self):
        """Set up the test environment"""
        self.data = ForkliftData()
        self.quote_generator = QuoteGenerator(self.data)
        
        # Create a mock forklift match result
        self.forklift_match = {
            'success': True,
            'forklift': {
                'model': 'D40s-5',
                'capacity_tons': 4.0,
                'capacity_kg': 4000,
                'fuel_type': 'Diesel',
                'series': '5-Series'
            },
            'rental_details': {
                'days': 7,
                'rates': {
                    'daily': 30.0,
                    'weekly_short': 140.0,
                    'weekly_long': 105.0,
                    'applied_rate': 30.0,
                    'total_cost': 210.0
                }
            },
            'brochure_excerpt': 'Diesel forklifts 5-Series, Pneumatic, 3.5 to 5.5 ton capacity...',
            'recommendations': 'This diesel forklift is well-suited for outdoor use.',
            'safety_info': 'This forklift comes with an Operator Sensing System (OSS)...'
        }
        
        # Create a mock failed match result
        self.failed_match = {
            'success': False,
            'message': 'No suitable forklift found for load weight of 15.0 tons.'
        }
    
    def test_generate_quote_success(self):
        """Test generating a quote with a successful match"""
        quote_result = self.quote_generator.generate_quote(self.forklift_match)
        
        # Check that the quote was generated successfully
        self.assertTrue(quote_result['success'], "Quote generation should be successful")
        self.assertIn('quote', quote_result, "Result should include a quote object")
        self.assertIn('brochure_excerpt', quote_result, "Result should include brochure excerpt")
        
        quote = quote_result['quote']
        
        # Check quote number format
        today = datetime.date.today().strftime('%Y%m%d')
        expected_quote_number_prefix = f"QT-{today}-D40s-5"
        self.assertTrue(quote['quote_number'].startswith(expected_quote_number_prefix), "Quote number should have the correct format")
        
        # Check forklift information
        self.assertEqual(quote['forklift']['model'], 'D40s-5', "Quote should have the correct forklift model")
        self.assertEqual(quote['forklift']['capacity'], '4.0 tons', "Quote should have the correct capacity")
        
        # Check rental period
        self.assertEqual(quote['rental_period']['days'], 7, "Quote should have the correct rental period")
        
        # Check pricing
        self.assertEqual(quote['pricing']['daily_rate'], 30.0, "Quote should have the correct daily rate")
        self.assertEqual(quote['pricing']['total_rental_cost'], 210.0, "Quote should have the correct total cost")
        self.assertEqual(quote['pricing']['deposit_required'], 42.0, "Deposit should be 20% of total cost")
        
        # Check recommendations and safety info
        self.assertEqual(quote['recommendations'], self.forklift_match['recommendations'], "Quote should include recommendations")
        self.assertEqual(quote['safety_info'], self.forklift_match['safety_info'], "Quote should include safety info")
    
    def test_generate_quote_failure(self):
        """Test generating a quote with a failed match"""
        quote_result = self.quote_generator.generate_quote(self.failed_match)
        
        # Check that the quote generation failed
        self.assertFalse(quote_result['success'], "Quote generation should fail")
        self.assertIn('message', quote_result, "Result should include an error message")
        self.assertEqual(
            quote_result['message'], 
            self.failed_match['message'], 
            "Error message should be passed through"
        )
    
    def test_format_quote_for_display(self):
        """Test formatting a quote for display"""
        # Generate a quote
        quote_result = self.quote_generator.generate_quote(self.forklift_match)
        
        # Format the quote for display
        formatted_result = self.quote_generator.format_quote_for_display(quote_result)
        
        # Check that the formatting was successful
        self.assertTrue(formatted_result['success'], "Quote formatting should be successful")
        self.assertIn('formatted_quote', formatted_result, "Result should include a formatted quote object")
        
        formatted_quote = formatted_result['formatted_quote']
        
        # Check section titles
        expected_sections = ['title', 'date', 'model_info', 'rental_info', 'pricing_info', 
                             'recommendations', 'safety_info', 'terms', 'brochure']
        
        for section in expected_sections:
            self.assertIn(section, formatted_quote, f"Formatted quote should include a '{section}' section")
        
        # Check that model info has the correct structure
        self.assertIn('title', formatted_quote['model_info'], "Model info should have a title")
        self.assertIn('items', formatted_quote['model_info'], "Model info should have items")
        
        # Check that pricing info includes all required fields
        pricing_labels = [item['label'] for item in formatted_quote['pricing_info']['items']]
        expected_pricing_labels = ['Daily Rate', 'Total Rental Cost', 'GST', 'Deposit Required']
        
        for label in expected_pricing_labels:
            self.assertIn(label, pricing_labels, f"Pricing info should include '{label}'")
    
    def test_format_quote_for_display_failure(self):
        """Test formatting a failed quote for display"""
        # Format the failed quote for display
        formatted_result = self.quote_generator.format_quote_for_display(self.failed_match)
        
        # Check that the formatting indicates failure
        self.assertFalse(formatted_result['success'], "Quote formatting should indicate failure")
        self.assertIn('message', formatted_result, "Result should include an error message")
        self.assertEqual(
            formatted_result['message'], 
            self.failed_match['message'], 
            "Error message should be passed through"
        )
    
    def test_get_terms_conditions(self):
        """Test getting terms and conditions"""
        terms = self.quote_generator._get_terms_conditions()
        
        # Check that terms and conditions include key sections
        key_terms = ['RENTAL PERIOD', 'PAYMENT', 'OPERATOR REQUIREMENTS', 
                     'MAINTENANCE', 'INSURANCE', 'DAMAGES', 'CANCELLATION']
        
        for term in key_terms:
            self.assertIn(term, terms, f"Terms should include section on '{term}'")

if __name__ == '__main__':
    unittest.main()
