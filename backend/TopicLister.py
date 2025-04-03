from requests_html import HTMLSession
from bs4 import BeautifulSoup
import html
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TopicLister:
    def __init__(self):
        self.session = HTMLSession()

    def extract_links(self, description):
        # Ensure the input is a string
        if not isinstance(description, str):
            description = str(description)

        decoded_description = html.unescape(description)
        soup = BeautifulSoup(decoded_description, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True)]
        logger.info(f"Extracted {len(links)} links from description")
        return links

    def parse_pub_date(self, pub_date_str):
        try:
            # Parse the RSS pubDate format
            return datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %Z')
        except Exception as e:
            logger.error(f"Error parsing publication date: {str(e)}")
            return None

    def get_topics(self):
        try:
            url = 'https://news.google.com/rss'
            logger.info(f"Fetching RSS feed from {url}")
            r = self.session.get(url)
            r.raise_for_status()  # Raise an exception for bad status codes
            
            soup = BeautifulSoup(r.text, 'xml')  # Use 'xml' parser for RSS feed
            topic_list = []
            
            items = soup.find_all('item')
            logger.info(f"Found {len(items)} items in RSS feed")
            
            for item in items:
                title = item.find('title').text
                links = self.extract_links(item.find('description'))
                pub_date = item.find('pubDate')
                pub_date_str = pub_date.text if pub_date else None
                pub_date_dt = self.parse_pub_date(pub_date_str) if pub_date_str else None
                
                logger.info(f"Extracted pubDate: {pub_date_str} -> {pub_date_dt}")
                
                topic = {
                    'title': title,
                    'links': links,
                    'pub_date': pub_date_dt
                }
                topic_list.append(topic)
                logger.info(f"Processed topic: {title} with {len(links)} links, published at {pub_date_dt}")

            logger.info(f"Successfully processed {len(topic_list)} topics")
            return topic_list
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed: {str(e)}")
            raise