from typing import Dict
import datetime

class QuoteGenerator:
    """
    Generates quotes for forklift rentals
    """
    
    def __init__(self, forklift_data):
        """
        Initialize with forklift data
        
        Args:
            forklift_data: Instance of ForkliftData containing specifications and rates
        """
        self.data = forklift_data
    
    def generate_quote(self, forklift_match: Dict) -> Dict:
        """
        Generate a quote based on the matched forklift and requirements
        
        Args:
            forklift_match: Dictionary with forklift match information
            
        Returns:
            Dictionary with quote details
        """
        if not forklift_match.get('success', False):
            return {
                'success': False,
                'message': forklift_match.get('message', 'No suitable forklift found.')
            }
        
        # Extract details from the match
        forklift = forklift_match['forklift']
        rental_details = forklift_match['rental_details']
        
        # Calculate dates
        today = datetime.date.today()
        rental_start = today + datetime.timedelta(days=1)  # Default to tomorrow
        rental_end = rental_start + datetime.timedelta(days=rental_details['days'] - 1)
        
        # Format dates
        start_date_str = rental_start.strftime('%d %B %Y')
        end_date_str = rental_end.strftime('%d %B %Y')
        
        # Calculate costs
        daily_rate = rental_details['rates']['applied_rate']
        total_cost = rental_details['rates']['total_cost']
        
        # Create the quote
        quote = {
            'quote_number': f"QT-{today.strftime('%Y%m%d')}-{forklift['model']}",
            'date_issued': today.strftime('%d %B %Y'),
            'forklift': {
                'model': forklift['model'],
                'capacity': f"{forklift['capacity_tons']} tons",
                'fuel_type': forklift['fuel_type'],
                'series': forklift['series']
            },
            'rental_period': {
                'days': rental_details['days'],
                'start_date': start_date_str,
                'end_date': end_date_str
            },
            'pricing': {
                'daily_rate': daily_rate,
                'total_rental_cost': total_cost,
                'gst_included': True,
                'deposit_required': total_cost * 0.20,  # 20% deposit
            },
            'terms_conditions': self._get_terms_conditions(),
            'recommendations': forklift_match.get('recommendations', ''),
            'safety_info': forklift_match.get('safety_info', '')
        }
        
        return {
            'success': True,
            'quote': quote,
            'brochure_excerpt': forklift_match.get('brochure_excerpt', '')
        }
    
    def format_quote_for_display(self, quote_result: Dict) -> Dict:
        """
        Format the quote for display in the UI
        
        Args:
            quote_result: The result from generate_quote
            
        Returns:
            Dictionary with formatted sections for display
        """
        if not quote_result.get('success', False):
            return {
                'success': False,
                'message': quote_result.get('message', 'Unable to generate quote.')
            }
        
        quote = quote_result['quote']
        brochure = quote_result['brochure_excerpt']
        
        # Format the quote information into sections
        quote_info = {
            'title': f"Forklift Rental Quote #{quote['quote_number']}",
            'date': f"Issued: {quote['date_issued']}",
            'model_info': {
                'title': 'Forklift Details',
                'items': [
                    {'label': 'Model', 'value': quote['forklift']['model']},
                    {'label': 'Capacity', 'value': quote['forklift']['capacity']},
                    {'label': 'Fuel Type', 'value': quote['forklift']['fuel_type']},
                    {'label': 'Series', 'value': quote['forklift']['series']}
                ]
            },
            'rental_info': {
                'title': 'Rental Period',
                'items': [
                    {'label': 'Start Date', 'value': quote['rental_period']['start_date']},
                    {'label': 'End Date', 'value': quote['rental_period']['end_date']},
                    {'label': 'Duration', 'value': f"{quote['rental_period']['days']} days"}
                ]
            },
            'pricing_info': {
                'title': 'Pricing Details',
                'items': [
                    {'label': 'Daily Rate', 'value': f"${quote['pricing']['daily_rate']:.2f}"},
                    {'label': 'Total Rental Cost', 'value': f"${quote['pricing']['total_rental_cost']:.2f}"},
                    {'label': 'GST', 'value': 'Included in price'},
                    {'label': 'Deposit Required', 'value': f"${quote['pricing']['deposit_required']:.2f}"}
                ]
            },
            'recommendations': {
                'title': 'Recommendations',
                'text': quote['recommendations']
            },
            'safety_info': {
                'title': 'Safety Information',
                'text': quote['safety_info']
            },
            'terms': {
                'title': 'Terms & Conditions',
                'text': quote['terms_conditions']
            },
            'brochure': {
                'title': 'Forklift Specifications',
                'text': brochure
            }
        }
        
        return {
            'success': True,
            'formatted_quote': quote_info
        }
    
    def _get_terms_conditions(self) -> str:
        """
        Get the terms and conditions for the rental
        
        Returns:
            String with terms and conditions
        """
        return (
            "1. RENTAL PERIOD: The rental period begins on the date specified and continues until the equipment "
            "is returned or the rental period ends, whichever is later.\n\n"
            "2. PAYMENT: A 20% deposit is required to secure the booking. The balance is due on delivery. "
            "For rentals exceeding 30 days, monthly payments may be arranged.\n\n"
            "3. OPERATOR REQUIREMENTS: All operators must be properly licensed and certified to operate the equipment. "
            "Proof of certification may be required.\n\n"
            "4. MAINTENANCE: Daily maintenance checks (oil, water, battery) are the responsibility of the renter. "
            "Any mechanical issues must be reported immediately.\n\n"
            "5. INSURANCE: The renter must provide insurance coverage for the equipment during the rental period. "
            "Proof of insurance is required prior to delivery.\n\n"
            "6. DAMAGES: The renter is responsible for any damages beyond normal wear and tear. "
            "Equipment must be returned in the same condition as when delivered.\n\n"
            "7. CANCELLATION: Cancellations made less than 48 hours before the rental start date "
            "may forfeit the deposit."
        )
