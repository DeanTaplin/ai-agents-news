import os
import re
import json
import requests
from datetime import datetime, timedelta
from newspaper import Article

def search_brave(query, count=10):
    api_key = os.getenv('BRAVE_API_KEY')
    if not api_key:
        raise ValueError('BRAVE_API_KEY environment variable not set')
    
    headers = {'X-Subscription-Token': api_key}
    url = 'https://api.search.brave.com/res/v1/web/search'
    params = {
        'q': query,
        'count': count,
        'freshness': 'pw',  # Past week
    }
    
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            'title': article.title,
            'text': article.text,
            'publish_date': article.publish_date,
            'url': url
        }
    except:
        return None

def categorize_news(article):
    # Define keywords for each category
    release_keywords = ['launch', 'release', 'announce', 'introduce', 'unveil', 'update', 'new version']
    innovation_keywords = ['breakthrough', 'research', 'discover', 'improve', 'develop', 'innovation', 'novel']
    market_keywords = ['market', 'industry',
