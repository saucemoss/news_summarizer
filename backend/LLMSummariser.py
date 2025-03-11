import ollama
from google import genai
import APISecrets
from pydantic import BaseModel


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
    client = genai.Client(api_key=APISecrets.gemini_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="You are a news articles analyst. You are given a few articles texts on the same or very similar topic. Your job is to review the articles, evaluate the most important news information and make a summary of it. "
                 "Ignore parts of the text that are not news. For example ignore: parts of the website structure, HTML/css elements, adverts, news provider information. "
                 "IMPORTANT, output format is JSON only. You are limited to only 4 insights. You will be provided with JSON schema."
                 "Use 'status' object to indicate weather you were able to process a summary. For example: if you encounter only non-news text like: cloudflare verification, cookie wall text or something non-news related - then in status use 'access denied: + reason. "
                 "If process was successful status should say 'OK' "
                 "Pass the first line of provided text to 'topic' object. Between articles there are URLs, pass them to 'links' object as list"
                 "Here is the text to summarize: " + text,
        config={
        'response_mime_type': 'application/json',
        'response_schema': list[Summary],
        },
    )
    print(response.text)

def get_article_summary_local(text):
    r = ollama.generate(model='llama3.2', prompt=text)
    return print(r.response)