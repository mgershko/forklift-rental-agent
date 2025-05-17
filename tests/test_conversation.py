import unittest
import sys
import os
from pathlib import Path

# Add the parent directory to the path to import the application modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.conversation import ConversationManager

class TestConversationManager(unittest.TestCase):
    """Test cases for the ConversationManager class"""
    
    def setUp(self):
        """Set up the test environment"""
        self.conversation = ConversationManager()
    
    def test_initialization(self):
        """Test that the conversation manager initializes correctly"""
        self.assertEqual(self.conversation.current_question_index, 0, "Should start with the first question")
        self.assertEqual(len(self.conversation.answered_questions), 0, "Should start with no answered questions")
        self.assertFalse(self.conversation.conversation_complete, "Conversation should not be complete initially")
    
    def test_get_current_question(self):
        """Test that the current question is returned correctly"""
        current_question = self.conversation.get_current_question()
        
        self.assertIsNotNone(current_question, "Current question should not be None")
        self.assertEqual(current_question['id'], 'load_weight', "First question should be about load weight")
        self.assertIn('question', current_question, "Question object should have a 'question' field")
        self.assertIn('validation', current_question, "Question object should have a 'validation' field")
    
    def test_process_answer_valid(self):
        """Test processing a valid answer"""
        # Answer the first question with a valid input
        is_valid, feedback = self.conversation.process_answer("3 tons")
        
        self.assertTrue(is_valid, "Answer should be valid")
        self.assertIn("Thank you", feedback, "Feedback should be positive")
        self.assertEqual(self.conversation.current_question_index, 1, "Should move to the next question")
        self.assertEqual(len(self.conversation.answered_questions), 1, "Should have one answered question")
        self.assertIn('load_weight', self.conversation.answered_questions, "Should store answer with correct ID")
    
    def test_process_answer_invalid(self):
        """Test processing an invalid answer"""
        # Answer the first question with an invalid input
        is_valid, feedback = self.conversation.process_answer("invalid")
        
        self.assertFalse(is_valid, "Answer should be invalid")
        self.assertIn("Invalid input", feedback, "Feedback should indicate the error")
        self.assertEqual(self.conversation.current_question_index, 0, "Should stay on the same question")
        self.assertEqual(len(self.conversation.answered_questions), 0, "Should not store the answer")
    
    def test_complete_conversation(self):
        """Test completing the entire conversation"""
        # Answer all questions
        answers = [
            "3 tons",            # load_weight
            "7 days",            # rental_period
            "outdoor",           # indoor_outdoor
            "3 meters",          # lift_height
            "Need side shifter"  # special_requirements
        ]
        
        for answer in answers:
            is_valid, feedback = self.conversation.process_answer(answer)
            self.assertTrue(is_valid, f"Answer '{answer}' should be valid")
        
        self.assertTrue(self.conversation.is_complete(), "Conversation should be complete")
        self.assertEqual(len(self.conversation.answered_questions), 5, "Should have 5 answered questions")
    
    def test_reset(self):
        """Test resetting the conversation"""
        # Answer a question
        self.conversation.process_answer("3 tons")
        
        # Reset the conversation
        self.conversation.reset()
        
        self.assertEqual(self.conversation.current_question_index, 0, "Should reset to the first question")
        self.assertEqual(len(self.conversation.answered_questions), 0, "Should reset answered questions")
        self.assertFalse(self.conversation.conversation_complete, "Conversation should not be complete after reset")
    
    def test_validate_weight(self):
        """Test validation of weight input"""
        # Test valid inputs
        valid_inputs = ["3 tons", "3000 kg", "3", "3.5 tons", "3.5"]
        for input_str in valid_inputs:
            self.assertTrue(
                self.conversation._validate_weight(input_str),
                f"Weight input '{input_str}' should be valid"
            )
        
        # Test invalid inputs
        invalid_inputs = ["", "abc", "tons"]
        for input_str in invalid_inputs:
            self.assertFalse(
                self.conversation._validate_weight(input_str),
                f"Weight input '{input_str}' should be invalid"
            )
    
    def test_validate_days(self):
        """Test validation of rental days input"""
        # Test valid inputs
        valid_inputs = ["7", "7 days", "1 week", "2 weeks", "1 month"]
        for input_str in valid_inputs:
            self.assertTrue(
                self.conversation._validate_days(input_str),
                f"Days input '{input_str}' should be valid"
            )
        
        # Test invalid inputs
        invalid_inputs = ["", "abc", "0", "-1", "0 days"]
        for input_str in invalid_inputs:
            self.assertFalse(
                self.conversation._validate_days(input_str),
                f"Days input '{input_str}' should be invalid"
            )
    
    def test_normalize_answer(self):
        """Test normalization of answers"""
        # Test weight normalization
        self.assertEqual(
            self.conversation._normalize_answer('load_weight', "3 tons"),
            3.0,
            "Should normalize '3 tons' to 3.0"
        )
        self.assertEqual(
            self.conversation._normalize_answer('load_weight', "3000 kg"),
            3.0,
            "Should normalize '3000 kg' to 3.0"
        )
        
        # Test days normalization
        self.assertEqual(
            self.conversation._normalize_answer('rental_period', "7 days"),
            7,
            "Should normalize '7 days' to 7"
        )
        self.assertEqual(
            self.conversation._normalize_answer('rental_period', "1 week"),
            7,
            "Should normalize '1 week' to 7"
        )
        self.assertEqual(
            self.conversation._normalize_answer('rental_period', "1 month"),
            30,
            "Should normalize '1 month' to 30"
        )
        
        # Test indoor/outdoor normalization
        self.assertEqual(
            self.conversation._normalize_answer('indoor_outdoor', "INDOOR"),
            "indoor",
            "Should normalize 'INDOOR' to 'indoor'"
        )
        
        # Test height normalization
        self.assertEqual(
            self.conversation._normalize_answer('lift_height', "3 meters"),
            3.0,
            "Should normalize '3 meters' to 3.0"
        )
        self.assertEqual(
            self.conversation._normalize_answer('lift_height', "10 feet"),
            3.048,
            "Should normalize '10 feet' to 3.048"
        )

if __name__ == '__main__':
    unittest.main()
