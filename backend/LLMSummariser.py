import ollama
from google import genai
import APISecrets
from pydantic import BaseModel
import json

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
    return json_dict[0]
