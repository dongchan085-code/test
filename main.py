import os
from dotenv import load_dotenv
from src.fetcher import fetch_top_papers
from src.summarizer import summarize_paper
from src.rss_builder import build_rss_feed
from src.email_sender import send_email_newsletter
from src.web_builder import build_web_page

def main():
    # Load environment variables
    load_dotenv()
    
    topic = os.getenv("HF_TOPIC", "LLM")
    
    print(f"Fetching top 5 papers from Hugging Face for topic: {topic}")
    try:
        papers = fetch_top_papers(topic, limit=5)
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return
        
    if not papers:
        print("No papers found for this topic today.")
        return
        
    print(f"Found {len(papers)} papers. Summarizing...")
    
    summaries = []
    for i, paper in enumerate(papers):
        print(f"[{i+1}/{len(papers)}] Summarizing: {paper.get('title')}")
        try:
            summary = summarize_paper(paper)
            summaries.append(summary)
        except Exception as e:
            print(f"Error summarizing paper {paper.get('title')}: {e}")
            summaries.append(f"Failed to summarize: {e}")
            
    # Delivery
    print("Generating RSS feed...")
    build_rss_feed(papers, summaries, topic, file_path="feed.xml")
    
    print("Generating Webpage...")
    build_web_page(papers, summaries, topic, file_path="index.html")
    
    print("Sending email (if configured)...")
    send_email_newsletter(papers, summaries, topic)
    
    print("Done!")

if __name__ == "__main__":
    main()
