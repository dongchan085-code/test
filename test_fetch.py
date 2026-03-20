import sys
from src.fetcher import fetch_top_papers
import json

try:
    print("Testing fetch_top_papers...")
    papers = fetch_top_papers("LLM", 2)
    print("Successfully fetched papers:", len(papers))
    for p in papers:
        print(f"- {p['title']} ({p['link']})")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
