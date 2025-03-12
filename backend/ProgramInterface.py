from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import TopicLister
from pydantic import BaseModel
from typing import List
import ArticleTextExtrator
import LLMSummariser


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to restrict domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from News Summarizer!"}

@app.get("/topic_list")
def get_topic_list():
    return TopicLister.get_topic_list()

class URLList(BaseModel):
    urls: List[str]

@app.post("/summary")
async def get_summary(data: URLList):
    articles = ArticleTextExtrator.extract_articles_parallel(data.urls, max_workers=4)
    insights = LLMSummariser.get_article_summary_gemini(articles)
    insights["links"] = data.urls
    insights["full_text"] = {articles}
    return insights

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)