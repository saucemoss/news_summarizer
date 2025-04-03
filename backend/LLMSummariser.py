import ollama
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import APISecrets
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)

#Gemini JSON Schema
class Insights(BaseModel):
    insight1: str
    insight2: str
    insight3: str
    insight4: str

class Summary(BaseModel):
    status: str
    topic: str
    links: list[str]
    insights: list[Insights]

def get_article_summary_gemini(text):
    prompt = """You are a news article analyst. Your task is to analyze multiple articles on the same or similar topic, 
                extract the most important news information, and generate a concise summary.
                
                Guidelines:
                - Ignore non-news content, such as website structure, HTML/CSS elements, advertisements, and news provider details.
                - Output strictly in JSON format based on the provided schema.
                - Extract exactly 4 key insights—no more, no less.
                - Create concise and clear title base on your insights and put it in "topic".
                - Collect all URLs found in the text and store them in the "links" list.
                
                Status Handling:
                - If the articles contain only non-news content (e.g., Cloudflare verification, cookie wall text, access restrictions), 
                  set "status": "access denied: [reason]".
                - If summarization is successful, set "status": "OK".
                
                Input:
                Below is the text to summarize: 
                """

    client = genai.Client(api_key=APISecrets.gemini_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents= prompt + text,
        config={
        'response_mime_type': 'application/json',
        'response_schema': list[Summary],
        },
    )

    json_dict = json.loads(response.text)
    logger.info(f"Raw Gemini response: {json.dumps(json_dict, indent=2)}")
    
    # Ensure the response has the correct structure
    if not isinstance(json_dict, list):
        logger.error("Response is not a list")
        return [{"status": "error", "topic": "Error processing article", "links": [], "insights": []}]
    
    if len(json_dict) == 0:
        logger.error("Response is empty")
        return [{"status": "error", "topic": "No content found", "links": [], "insights": []}]
    
    # Ensure each item has the required fields
    for item in json_dict:
        if "insights" not in item:
            item["insights"] = []
        if "links" not in item:
            item["links"] = []
        if "status" not in item:
            item["status"] = "OK"
        if "topic" not in item:
            item["topic"] = "Untitled"
    
    return json_dict
