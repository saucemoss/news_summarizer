import unittest
from unittest.mock import patch, MagicMock
from LLMSummariser import generate_image
from google import genai
from PIL import Image
import io

class TestImageGenerator(unittest.TestCase):
    def setUp(self):
        # Mock the Google API key
        self.api_key = "test_api_key"
        genai.configure(api_key=self.api_key)
        
        # Create a mock model
        self.mock_model = MagicMock()
        
        # Create a mock response
        self.mock_response = MagicMock()
        self.mock_response.image = Image.new('RGB', (100, 100), color='red')
        
        # Create a mock generation
        self.mock_generation = MagicMock()
        self.mock_generation.images = [self.mock_response]

    @patch('google.generativeai.GenerativeModel')
    def test_generate_image_success(self, mock_generative_model):
        # Setup mock
        mock_model = MagicMock()
        mock_model.generate_content.return_value = self.mock_generation
        mock_generative_model.return_value = mock_model
        
        # Test data
        prompt = "A beautiful sunset over mountains"
        
        # Call the function
        image = generate_image(prompt)
        
        # Assertions
        self.assertIsNotNone(image)
        self.assertIsInstance(image, Image.Image)
        mock_model.generate_content.assert_called_once()
        
        # Verify the prompt was passed correctly
        call_args = mock_model.generate_content.call_args[0][0]
        self.assertIn(prompt, str(call_args))

    @patch('google.generativeai.GenerativeModel')
    def test_generate_image_empty_prompt(self, mock_generative_model):
        # Test with empty prompt
        with self.assertRaises(ValueError):
            generate_image("")

    @patch('google.generativeai.GenerativeModel')
    def test_generate_image_api_error(self, mock_generative_model):
        # Setup mock to raise an exception
        mock_model = MagicMock()
        mock_model.generate_content.side_effect = Exception("API Error")
        mock_generative_model.return_value = mock_model
        
        # Test error handling
        with self.assertRaises(Exception) as context:
            generate_image("Test prompt")
        
        self.assertIn("API Error", str(context.exception))

    @patch('google.generativeai.GenerativeModel')
    def test_generate_image_invalid_response(self, mock_generative_model):
        # Setup mock with invalid response
        mock_model = MagicMock()
        mock_generation = MagicMock()
        mock_generation.images = []  # Empty images list
        mock_model.generate_content.return_value = mock_generation
        mock_generative_model.return_value = mock_model
        
        # Test error handling
        with self.assertRaises(Exception) as context:
            generate_image("Test prompt")
        
        self.assertIn("No image generated", str(context.exception))

    def test_generate_image_safety_settings(self):
        # Test that safety settings are properly configured
        with patch('google.generativeai.GenerativeModel') as mock_generative_model:
            mock_model = MagicMock()
            mock_model.generate_content.return_value = self.mock_generation
            mock_generative_model.return_value = mock_model
            
            generate_image("Test prompt")
            
            # Verify safety settings were configured
            mock_generative_model.assert_called_once()
            call_args = mock_generative_model.call_args[1]
            self.assertIn('safety_settings', call_args)
            safety_settings = call_args['safety_settings']
            
            # Check that all required safety categories are present
            categories = ['HARASSMENT', 'HATE_SPEECH', 'SEXUALLY_EXPLICIT', 'DANGEROUS_CONTENT']
            for category in categories:
                found = False
                for setting in safety_settings:
                    if setting['category'] == category:
                        found = True
                        self.assertEqual(setting['threshold'], 'BLOCK_MEDIUM_AND_ABOVE')
                        break
                self.assertTrue(found, f"Safety setting for {category} not found")

if __name__ == '__main__':
    unittest.main() 