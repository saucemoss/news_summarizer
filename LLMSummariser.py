import ollama
from google import genai
import APISecrets

def get_article_summary_gemini(text):
    client = genai.Client(api_key=APISecrets.gemini_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="You are a news articles analyst. Your job is to review given text, find in it the most important news information and make a summary of it. "
                 "Ignore parts of the text that are not news. For example ignore: parts of the website structure, HTML/css elements, adverts, news provider information. "
                 "IMPORTANT, output format is JSON only. Use this JSON schema: Summary = {'status': str,'insights': {'insight1': str,'insight2': str,'insight3': str}}. Return: list[Summary]. You are limited to only 3 insights. "
                 "Use 'status' object in schema to indicate weather you were able to process a summary. For example: if you encounter only non-news text like: cloudflare verification, cookie wall text or something non-news related - then in status use 'access denied: + reason. "
                 "If process was successful status should say 'OK' "
                 "Here is the text to summarize: " + text
    )
    print(response.text)

def get_article_summary_local(text):
    r = ollama.generate(model='llama3.2', prompt=text)
    return print(r.response)