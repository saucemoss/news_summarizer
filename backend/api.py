from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Article
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ArticleResponse(BaseModel):
    id: int
    title: str
    url: str
    source: str
    summary: str
    insights: str
    created_at: datetime
    processed_at: datetime

    class Config:
        orm_mode = True

class ArticleWithImageResponse(ArticleResponse):
    image_url: str | None

class ArticlesResponse(BaseModel):
    articles: List[ArticleResponse]
    total: int
    has_more: bool

@app.get("/api/articles", response_model=ArticlesResponse)
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    try:
        # Get total count
        total = db.query(Article).count()
        
        # Get paginated articles
        articles = db.query(Article)\
            .order_by(Article.processed_at.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()
        
        has_more = (skip + limit) < total
        
        logger.info(f"Retrieved {len(articles)} articles (skip: {skip}, limit: {limit})")
        return {
            "articles": articles,
            "total": total,
            "has_more": has_more
        }
    except Exception as e:
        logger.error(f"Error retrieving articles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/articles/{article_id}", response_model=ArticleWithImageResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    try:
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            logger.error(f"Article with ID {article_id} not found")
            raise HTTPException(status_code=404, detail="Article not found")
        logger.info(f"Retrieved article {article_id}: {article.title}")
        return article
    except Exception as e:
        logger.error(f"Error retrieving article {article_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 