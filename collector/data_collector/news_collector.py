from config import GOOGLE_NEWS_RSS_URL, NEWS_RSS_NICKNAMES

import os
import json 
import feedparser
from datetime import datetime, UTC
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from transformers import pipeline
summarizer = pipeline("summarization", model = "sshleifer/distilbart-cnn-12-6")

import pandas as pd
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

DATA_DIRECTORY = os.environ.get("DATA_DIRECTORY")

def collectNews(rssUrl, country, nickname = None):
    now = datetime.now(UTC)
    today = now.date()
    
    save_directory = f"{DATA_DIRECTORY}/news/{country}"
    os.makedirs(save_directory, exist_ok = True)
    output_path = os.path.join(save_directory, f"{nickname}_{today}.json")
    
    news_items = []
    feed_url = f"{GOOGLE_NEWS_RSS_URL}?q={rssUrl}+when:1d&hl={country.lower()}"
    # print("feed url", feed_url)
    feed = feedparser.parse(feed_url)
    # print("feed", feed)
    for feed_item in feed.entries:
        # print("feed item", feed_item)
        news_items.append(
            {
                "title" : feed_item.get("title"),
                "link" : feed_item.get("link"),
                "published" : feed_item.get("published"),
                "summary" : feed_item.get("summary"),
                "source" : feed_url
            }
        )
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            news_items,
            f,
            ensure_ascii = False,
            indent = 2
        )
    print(f"Complete to Save {country} News RSS Feed, news count : ({len(news_items)}), to {output_path}")

def summarizeText(text, maxLength = 60):
    try:
        return summarizer(
            text,
            max_length = maxLength,
            min_length = 20,
            do_sample = False
        )[0]["summary_text"]
    except Exception as e:
        return ""
    
def summaryNews(country = "KR", date = None):
    date = date or str(datetime.now(UTC).date())
    
    data_dir = f"{DATA_DIRECTORY}/news/{country}"
    summary_dir = f"{DATA_DIRECTORY}/news_summary/{country}"
    os.makedirs(summary_dir, exist_ok = True)
    for i in range(1, 3):
        data_path = f"{data_dir}/{NEWS_RSS_NICKNAMES[f"{country}_{i}"]}_{date}.json"
        summary_path = f"{summary_dir}/{NEWS_RSS_NICKNAMES[f"{country}_{i}"]}_summary_{date}.json"
        
        news_data = None
        with open(data_path, encoding='utf-8') as f:
            news_data = json.load(f)
        if news_data != None:
            summaries = []
            for item in news_data:
                text = item.get("title", "") + " " + item.get("summary", "")
                summarized = summarizeText(text)
                summaries.append(
                    {
                        "title" : item.get("title", ""),
                        "summary" : summarized,
                        "link" : item.get("link", ""),
                        "published" : item.get("publisehd", "")
                    }
                )
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summaries, f, ensure_ascii = False, indent = 2)
    print(f"Complete to Summarize {country} News RSS Feed, count : ({len(summaries)}), to {summary_path}")

def scoreSentiment(text):
    try:
        result = sentiment_analyzer(text[:512])[0]
        label = result["label"]
        score = result["score"]
        return {
            "label" : label,
            "score" : round(score, 4),
            "sentiment_value" : {
                "positive" : 1,
                "neutral" : 0,
                "negative" : -1
            }.get(label.lower(), 0)
        }
    except Exception as e:
        return {
            "label" : "neutral",
            "score" : 0.0,
            "sentiment_value" : 0
        }

def analyzeSummarySentiment(country = "KR", date = None):
    date = date or str(datetime.now(UTC).date())
    
    summary_dir = f"{DATA_DIRECTORY}/news_summary/{country}"
    sentiment_dir = f"{DATA_DIRECTORY}/news_sentiment/{country}"
    os.makedirs(sentiment_dir, exist_ok = True)
    
    for i in range(1, 3):
        summary_path = f"{summary_dir}/{NEWS_RSS_NICKNAMES[f"{country}_{i}"]}_summary_{date}.json"
        sentiment_path = f"{sentiment_dir}/{NEWS_RSS_NICKNAMES[f"{country}_{i}"]}_{date}.parquet"

        summaries = None
        with open(summary_path, encoding="utf-8") as f:
            summaries = json.load(f)
        
        scored = []
        for item in summaries:
            text = item["summary"]
            result = scoreSentiment(text)
            scored.append(
                {
                    "date" : date,
                    "title" : item["title"],
                    "summary" : text,
                    "sentiment_level" : result["label"],
                    "sentiment_score" : result["score"],
                    "sentiment_value" : result["sentiment_value"]
                }
            )
        
        df = pd.DataFrame(scored)
        df.to_parquet(sentiment_path, index = False)
        
        print(f"Complete to calculate {country} NEWS RSS Feed Sentiment Score to {sentiment_path}")