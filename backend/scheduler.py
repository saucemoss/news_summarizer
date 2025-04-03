import schedule
import time
from datetime import datetime
from sqlalchemy.orm import Session
from database import Article, get_db
from ArticleTextExtrator import extract_articles_parallel
from LLMSummariser import get_article_summary_gemini
from TopicLister import TopicLister
import logging
import json
from ImageGenerator import generate_article_image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_topic(topic):
    """Process a single topic: extract content, generate summary, and create image"""
    try:
        # Debug logging
        logger.info(f"Processing topic: {topic}")
        logger.info(f"Topic type: {type(topic)}")
        if isinstance(topic, dict):
            logger.info(f"Topic keys: {topic.keys()}")
            logger.info(f"Topic links: {topic.get('links', [])}")
            logger.info(f"Topic pub_date: {topic.get('pub_date')}")
        
        # Extract articles from links
        if not isinstance(topic, dict) or 'links' not in topic:
            logger.error(f"Invalid topic structure: {topic}")
            return
            
        logger.info(f"Extracting articles from {len(topic['links'])} links")
        articles = extract_articles_parallel(topic['links'], max_workers=8)
        logger.info(f"Extracted {len(articles)} articles")
        
        if not articles:
            logger.error("No articles extracted from links")
            return
            
        # Merge all article contents
        merged_content = "\n\n".join(article['content'] for article in articles)
        merged_title = topic['title']  # Use topic title as the main title
        
        # Check if article already exists
        db = next(get_db())
        try:
            existing_article = db.query(Article).filter(Article.title == merged_title).first()
            if existing_article:
                logger.info(f"Article already exists: {merged_title}")
                db.close()
                return
        except Exception as e:
            logger.error(f"Error checking for existing article: {str(e)}")
            db.close()
            return
            
        try:
            # Generate summary using Gemini
            summary_data_list = get_article_summary_gemini(merged_content)
            if not summary_data_list:
                logger.error("No summary data generated")
                return
                
            # Generate image for the article
            image_url = generate_article_image(merged_title, json.dumps(summary_data_list[0].get('insights', [])))
            logger.info(f"Generated image URL: {image_url}")
            
            # Create article in database
            article = Article(
                title=merged_title,
                url=topic['links'][0],  # Use first link as primary URL
                source=articles[0].get('source', 'Unknown'),
                content=merged_content,
                summary=summary_data_list[0].get('summary', ''),
                insights=json.dumps(summary_data_list[0].get('insights', [])),
                image_url=image_url,
                pub_date=topic.get('pub_date')  # Add publication date from RSS feed
            )
            
            db.add(article)
            db.commit()
            logger.info(f"Successfully created article: {merged_title}")
            
        except Exception as e:
            logger.error(f"Error creating article in database: {str(e)}")
            db.rollback()
        finally:
            db.close()
                
    except Exception as e:
        logger.error(f"Error processing topic: {str(e)}")
        logger.error(f"Topic data: {topic}")
        raise  # Re-raise the exception to see the full traceback

def run_scheduler():
    """Main scheduler function"""
    logger.info("Starting scheduler...")
    
    try:
        # Get topics
        topic_lister = TopicLister()
        topics = topic_lister.get_topics()
        logger.info(f"Retrieved {len(topics)} topics from RSS feed")
        
        if not topics:
            logger.error("No topics retrieved from RSS feed")
            return
            
        # Get database session
        db = next(get_db())
        try:
            # Get list of existing article titles
            existing_titles = {article.title for article in db.query(Article.title).all()}
            logger.info(f"Found {len(existing_titles)} existing articles in database")
            
            # Filter out topics that already exist in the database
            new_topics = [
                topic for topic in topics 
                if topic['title'] not in existing_titles
            ]
            logger.info(f"Found {len(new_topics)} new topics to process")
            
            if not new_topics:
                logger.info("No new topics to process")
                return
                
            # Process each new topic
            for topic in new_topics:
                logger.info(f"Processing new topic: {topic.get('title', 'No title')}")
                process_topic(topic)
            
            logger.info("Scheduler completed successfully")
        except Exception as e:
            logger.error(f"Error in database operations: {str(e)}")
            raise
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error in run_scheduler: {str(e)}")
        raise

def main():
    # Run immediately on startup
    run_scheduler()
    
    # Schedule to run every hour
    schedule.every(1).hours.do(run_scheduler)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main() 