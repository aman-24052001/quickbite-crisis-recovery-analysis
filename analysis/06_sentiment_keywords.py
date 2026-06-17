"""
06_sentiment_keywords.py
Review text frequency analysis — top keywords by phase and sentiment
"""
import pandas as pd
import re
from collections import Counter
import warnings; warnings.filterwarnings('ignore')

BASE = "data/"

STOPWORDS = {
    'the','a','an','is','it','was','and','or','but','of','to','in','for',
    'my','i','so','on','at','with','very','this','that','not','had','have',
    'has','me','we','our','their','from','be','been','as','are','by','do',
    'did','no','just','got','get','will','would','they','them','he','she',
    'its','were','too','all','more','than','food','order','delivery'
}

def top_words(series, n=15):
    words = []
    for text in series.dropna():
        for w in re.findall(r"[a-z']+", str(text).lower()):
            if len(w) > 3 and w not in STOPWORDS:
                words.append(w)
    return Counter(words).most_common(n)

def load():
    ratings = pd.read_csv(f"{BASE}fact_ratings.csv")
    ratings['review_timestamp'] = pd.to_datetime(
        ratings['review_timestamp'], dayfirst=True, errors='coerce'
    )
    ratings['month_num'] = ratings['review_timestamp'].dt.month
    ratings['phase'] = ratings['month_num'].map(
        lambda m: 'Pre-Crisis' if m <= 5 else ('Crisis' if m == 6 else 'Recovery')
    )
    return ratings

if __name__ == '__main__':
    ratings = load()

    print("=== RATINGS BY PHASE ===")
    print(ratings.groupby('phase').agg(
        avg_rating    = ('rating', 'mean'),
        avg_sentiment = ('sentiment_score', 'mean'),
        count         = ('rating', 'count'),
    ).round(3).to_string())

    print("\n=== TOP NEGATIVE KEYWORDS (rating < 3) ===")
    neg = ratings[ratings['rating'] < 3]
    for phase in ['Crisis', 'Recovery']:
        sub = neg[neg['phase'] == phase]
        print(f"\n{phase}:")
        for word, count in top_words(sub['review_text'], 10):
            print(f"  {word:<20} {count:>5}")

    print("\n=== TOP POSITIVE KEYWORDS (Pre-Crisis, rating >= 4) ===")
    pos = ratings[(ratings['phase']=='Pre-Crisis') & (ratings['rating'] >= 4)]
    for word, count in top_words(pos['review_text'], 10):
        print(f"  {word:<20} {count:>5}")
