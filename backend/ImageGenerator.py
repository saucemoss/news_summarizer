from google import genai
from google.genai import types
import APISecrets
import base64
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def generate_article_image(title, insights):

    try:
        # Create a prompt that combines title, summary, and insights
        prompt = f"""

        Create a high-quality, visually appealing image with no text or words. Negative prompt: text or words.
        The image should contain an abstract representation of the topic and insights presented in the below input.

        Topic: {title}
        Insights: {insights}

        """


        # Initialize Gemini client
        client = genai.Client(api_key=APISecrets.gemini_key)
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=['Text', 'Image']
                )
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO((part.inline_data.data)))
                buffered = BytesIO()
                image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue()).decode()

                
        return f"data:image/jpeg;base64,{img_str}"   
  
        
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return None 