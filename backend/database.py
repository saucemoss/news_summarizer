from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), nullable=False)
    source = Column(String(100), nullable=False)
    content = Column(Text)
    summary = Column(Text)
    insights = Column(Text)
    image_url = Column(String(1000))
    pub_date = Column(DateTime)  # Publication date from RSS feed
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, default=datetime.utcnow)

# Create database engine
engine = create_engine('sqlite:///articles.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close() 