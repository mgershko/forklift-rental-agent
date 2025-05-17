from typing import Dict, List, Optional, Tuple

class ConversationManager:
    """
    Manages the conversation flow for gathering forklift rental requirements
    """
    
    def __init__(self):
        """Initialize the conversation manager with the sequence of questions"""
        self.questions = [
            {
                'id': 'load_weight',
                'question': 'What is the weight of the heaviest load you need to lift?',
                'follow_up': 'Please specify the weight (e.g., 2 tons, 2000 kg)',
                'validation': self._validate_weight,
                'required': True
            },
            {
                'id': 'rental_period',
                'question': 'How long do you need to rent the forklift for?',
                'follow_up': 'Please specify the number of days',
                'validation': self._validate_days,
                'required': True
            },
            {
                'id': 'indoor_outdoor',
                'question': 'Will you be using the forklift indoors, outdoors, or both?',
                'options': ['indoor', 'outdoor', 'both'],
                'validation': lambda x: x in ['indoor', 'outdoor', 'both'],
                'required': True
            },
            {
                'id': 'lift_height',
                'question': 'What is the maximum height you need to lift to?',
                'follow_up': 'Please specify the height (e.g., 3 meters, 10 feet)',
                'validation': self._validate_height,
                'required': False
            },
            {
                'id': 'special_requirements',
                'question': 'Do you have any special requirements or attachments needed?',
                'validation': lambda x: True,  # Any answer is valid
                'required': False
            }
        ]
        
        # Track the state of the conversation
        self.current_question_index = 0
        self.answered_questions = {}
        self.conversation_complete = False
    
    def get_current_question(self) -> Dict:
        """Get the current question to ask the user"""
        if self.conversation_complete:
            return {"message": "All questions answered. Ready to recommend a forklift."}
        
        if self.current_question_index < len(self.questions):
            return self.questions[self.current_question_index]
        else:
            self.conversation_complete = True
            return {"message": "All questions answered. Ready to recommend a forklift."}
    
    def process_answer(self, answer: str) -> Tuple[bool, str]:
        """
        Process the user's answer to the current question
        
        Args:
            answer: The user's answer
            
        Returns:
            Tuple containing:
            - Boolean indicating if the answer is valid
            - String with feedback (error message or confirmation)
        """
        if self.conversation_complete:
            return True, "All questions have already been answered."
        
        current_question = self.questions[self.current_question_index]
        question_id = current_question['id']
        
        # Validate the answer
        is_valid = current_question['validation'](answer)
        
        if is_valid:
            # Store the answer
            self.answered_questions[question_id] = self._normalize_answer(question_id, answer)
            
            # Move to the next question
            self.current_question_index += 1
            
            # Check if we've completed all required questions
            if self.current_question_index >= len(self.questions):
                self.conversation_complete = True
                return True, "Thank you for providing all the information. I'll recommend a suitable forklift."
            
            # Get the next question
            next_question = self.questions[self.current_question_index]
            next_question_text = next_question['question']
            
            # Include options if available
            if 'options' in next_question:
                options_str = ', '.join(next_question['options'])
                next_question_text += f" ({options_str})"
            
            return True, f"Thank you. {next_question_text}"
        else:
            # Return an error message
            if 'follow_up' in current_question:
                return False, f"Invalid input. {current_question['follow_up']}"
            elif 'options' in current_question:
                options_str = ', '.join(current_question['options'])
                return False, f"Invalid input. Please select one of: {options_str}"
            else:
                return False, "Invalid input. Please try again."
    
    def get_requirements(self) -> Dict:
        """
        Get the gathered requirements
        
        Returns:
            Dictionary of requirements
        """
        return self.answered_questions
    
    def is_complete(self) -> bool:
        """
        Check if the conversation is complete
        
        Returns:
            Boolean indicating if all required questions have been answered
        """
        return self.conversation_complete
    
    def reset(self):
        """Reset the conversation to start over"""
        self.current_question_index = 0
        self.answered_questions = {}
        self.conversation_complete = False
    
    def _validate_weight(self, answer: str) -> bool:
        """
        Validate weight input
        
        Args:
            answer: User's weight input
            
        Returns:
            Boolean indicating if input is valid
        """
        # Check for numeric value
        import re
        if re.search(r'\d+', answer):
            # If it has units, check if they're valid
            if any(unit in answer.lower() for unit in ['ton', 'kg', 'lb']):
                return True
            # If no units, assume it's a valid number
            return True
        return False
    
    def _validate_days(self, answer: str) -> bool:
        """
        Validate rental days input
        
        Args:
            answer: User's rental period input
            
        Returns:
            Boolean indicating if input is valid
        """
        import re
        # Check for a positive integer
        if re.match(r'^\d+$', answer) and int(answer) > 0:
            return True
        # Check for period with units (days, weeks, months)
        if re.search(r'\d+\s*(day|week|month)', answer, re.IGNORECASE):
            return True
        return False
    
    def _validate_height(self, answer: str) -> bool:
        """
        Validate height input
        
        Args:
            answer: User's height input
            
        Returns:
            Boolean indicating if input is valid
        """
        import re
        # Check for numeric value
        if re.search(r'\d+', answer):
            # If it has units, check if they're valid
            if any(unit in answer.lower() for unit in ['m', 'meter', 'ft', 'feet']):
                return True
            # If no units, assume it's a valid number
            return True
        return False
    
    def _normalize_answer(self, question_id: str, answer: str):
        """
        Normalize the user's answer to a standard format
        
        Args:
            question_id: ID of the question
            answer: User's answer
            
        Returns:
            Normalized answer
        """
        if question_id == 'load_weight':
            # Extract numeric value
            import re
            match = re.search(r'(\d+\.?\d*)', answer)
            if match:
                value = float(match.group(1))
                # Convert to tons if in kg
                if 'kg' in answer.lower():
                    value = value / 1000
                return value
            return answer
        
        elif question_id == 'rental_period':
            # Extract numeric value
            import re
            match = re.search(r'(\d+)', answer)
            if match:
                days = int(match.group(1))
                # Convert to days if in weeks or months
                if 'week' in answer.lower():
                    days *= 7
                elif 'month' in answer.lower():
                    days *= 30
                return days
            return int(answer)
        
        elif question_id == 'indoor_outdoor':
            return answer.lower()
        
        elif question_id == 'lift_height':
            # Extract numeric value
            import re
            match = re.search(r'(\d+\.?\d*)', answer)
            if match:
                value = float(match.group(1))
                # Convert to meters if in feet
                if any(unit in answer.lower() for unit in ['ft', 'feet']):
                    value = value * 0.3048
                return value
            return answer
        
        else:
            return answer
