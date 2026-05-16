from pytrends.request import TrendReq
import time
import random

pytrends = TrendReq(
    hl='en-US',
    tz=330
)

def get_live_trends():
    keywords = [
        "Indo western outfit",
        "Korean fashion India",
        "college outfit ideas",
        "ethnic fusion wear",
        "streetwear India"
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
        # Backup values if Google blocks request
        return {
            "google": {
                "Indo western outfit": 72,
                "Korean fashion India": 61,
                "college outfit ideas": 80,
                "ethnic fusion wear": 66,
                "streetwear India": 58
            },
            "pinterest": pinterest_feeds
        }