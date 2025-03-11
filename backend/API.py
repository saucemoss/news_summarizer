from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

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
    return {"message": "Hello from FastAPI!"}

@app.get("/test")
def test():
    return {"message": "Test successful."}

@app.get("/news")
def get_news():
    time.sleep(2)
    return [
        {
            "name": "Tech Innovations",
            "summary": "AI is transforming the industry...",
            "insights": ["Insight 1", "Insight 2", "Insight 3", "Insight 4"],
            "articles": [{"url": "https://example.com", "text": "Full article text"}]
        },
        {
            "name": "What? No!",
            "summary": "Testing The Waters",
            "insights": ["Insight 5", "Insight 6", "Insight 7", "Insight 8"],
            "articles": [{"url": "https://example.com", "text": "Full article text"}]
        },
        {
            "name": "QWEASDZXC",
            "summary": "Lorem Ipsum",
            "insights": ["Insight 9", "Insight 1", "Insight 2", "Insight 3"],
            "articles": [{"url": "https://example.com", "text": "Full article text"}]
        },
        {
            "name": "Major ship collision in UK waters sparks fears of toxic chemical leak - New Scientist",
            "summary": "Major ship collision in UK waters sparks fears of toxic chemical leak - New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak - "
                       "New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak - New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak -"
                       " New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak - New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak -"
                       " New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak - New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak -"
                       " New ScientistMajor ship collision in UK waters sparks fears of toxic chemical leak - New Scientist",
            "insights": ["Insight 9", "Insight 1", "Insight 2", "Insight 3"],
            "articles": [{"url": "https://example.com", "text": "Full article text"}]
        }
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)