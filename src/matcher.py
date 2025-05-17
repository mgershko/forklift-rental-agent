import re
from typing import Dict, List, Optional, Tuple

class ForkliftMatcher:
    """
    Class to match customer requirements to appropriate forklift models
    """
    
    def __init__(self, forklift_data):
        """
        Initialize with forklift data
        
        Args:
            forklift_data: Instance of ForkliftData containing specifications
        """
        self.data = forklift_data
    
    def match_forklift(self, requirements: Dict) -> Dict:
        """
        Match customer requirements to the best forklift model
        
        Args:
            requirements: Dictionary containing customer requirements
                - load_weight: Weight to be lifted in kg or tons
                - rental_period: Number of days for rental
                - indoor_outdoor: Whether the forklift will be used indoors, outdoors, or both
                - height_requirement: Maximum height required in meters
                - special_requirements: Any special requirements or features needed
        
        Returns:
            Dictionary with matched forklift information and options
        """
        # Extract and normalize load weight requirement
        load_weight = self._normalize_weight(requirements.get('load_weight', 0))
        
        # Add safety margin (20% extra capacity for safety)
        required_capacity = load_weight * 1.2
        
        # Find a suitable forklift
        matched_forklift = self.data.get_forklift_by_capacity(required_capacity)
        
        # If no match found, return empty result
        if matched_forklift is None:
            return {
                'success': False,
                'message': f"No suitable forklift found for load weight of {load_weight} tons."
            }
        
        # Calculate rental rate
        rental_days = requirements.get('rental_period', 1)
        rate_info = self.data.get_rate_for_model(matched_forklift['model'], rental_days)
        
        # Get brochure information
        brochure = self.data.get_brochure_content(matched_forklift['model'])
        
        # Get indoor/outdoor recommendation
        indoor_outdoor = requirements.get('indoor_outdoor', 'both')
        usage_recommendation = self._get_usage_recommendation(matched_forklift, indoor_outdoor)
        
        # Compile the result
        result = {
            'success': True,
            'forklift': matched_forklift.to_dict(),
            'rental_details': {
                'days': rental_days,
                'rates': rate_info,
            },
            'brochure_excerpt': brochure,
            'recommendations': usage_recommendation,
            'safety_info': self._get_safety_info(matched_forklift)
        }
        
        return result
    
    def _normalize_weight(self, weight_input) -> float:
        """
        Normalize weight input to tons
        
        Args:
            weight_input: Weight as string (e.g., "2 tons", "2000 kg") or number
            
        Returns:
            Weight in tons as a float
        """
        if isinstance(weight_input, (int, float)):
            return float(weight_input)
        
        # Extract numeric value
        try:
            value = float(re.findall(r'\d+\.?\d*', str(weight_input))[0])
        except (IndexError, ValueError):
            return 0.0
        
        # Convert to tons if in kg
        if 'kg' in str(weight_input).lower():
            value = value / 1000
        
        return value
    
    def _get_usage_recommendation(self, forklift, indoor_outdoor):
        """
        Get usage recommendations based on the environment
        
        Args:
            forklift: Selected forklift information
            indoor_outdoor: Usage environment ('indoor', 'outdoor', or 'both')
            
        Returns:
            Usage recommendations
        """
        if indoor_outdoor == 'indoor':
            return (
                "For indoor use, ensure adequate ventilation when using a diesel forklift. "
                "Consider requesting LPG alternatives for better indoor air quality."
            )
        elif indoor_outdoor == 'outdoor':
            return (
                "This diesel forklift is well-suited for outdoor use. "
                "The pneumatic tires provide good traction on various surfaces."
            )
        else:  # both
            return (
                "For mixed indoor/outdoor use, this diesel forklift will work well, but ensure "
                "indoor areas are well-ventilated. For primarily indoor operations, "
                "consider an LPG model for better air quality."
            )
    
    def _get_safety_info(self, forklift):
        """
        Get safety information for the selected forklift
        
        Args:
            forklift: Selected forklift information
            
        Returns:
            Safety information
        """
        return (
            "This forklift comes with an Operator Sensing System (OSS), oil-cooled disc brakes, "
            "and excellent visibility through the mast. Remember that all operators must be "
            "certified to operate this equipment. Daily safety checks are required before operation."
        )
