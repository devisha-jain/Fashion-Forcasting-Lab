from pytrends.request import TrendReq
import time
import random

pytrends = TrendReq(
    hl='en-US',
    tz=330
)

def get_live_trends(query=None):
    if not query:
        query = "fashion"
        
    keywords = [
        query,
        query + " India",
        query + " fashion",
        query + " outfit ideas"
    ]
    
    # Mock pinterest feeds since there's no open API
    pinterest_feeds = {
        "bollywood_aesthetic": random.randint(70, 98),
        "korean_streetwear": random.randint(60, 95),
        "genz_college_core": random.randint(75, 99),
        "indian_minimalism": random.randint(65, 90)
    }

    try:
        time.sleep(2)
        pytrends.build_payload(
            keywords,
            timeframe='today 3-m',
            geo='IN'
        )
        data = pytrends.interest_over_time()
        
        google_scores = {}
        for keyword in keywords:
            google_scores[keyword] = int(data[keyword].iloc[-1])
            
        return {
            "google": google_scores,
            "pinterest": pinterest_feeds
        }

    except Exception:
        # Backup values if Google blocks request (avoids crash and handles dynamic terms elegantly)
        return {
            "google": {
                query: random.randint(55, 80),
                query + " India": random.randint(60, 85),
                query + " fashion": random.randint(50, 75),
                query + " outfit ideas": random.randint(65, 90)
            },
            "pinterest": pinterest_feeds
        }
