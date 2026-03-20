import requests
import urllib.parse
from typing import List, Dict, Any

def fetch_top_papers(topic: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetches the most recent 'Daily' Hugging Face papers matching the topic.
    First tries to find recent papers matching the topic, then falls back to general search.
    """
    papers = []
    topic_lower = topic.lower()
    
    # 1. Fetch latest 100 papers from HF to find fresh ones
    latest_url = "https://huggingface.co/api/papers?limit=100"
    try:
        response = requests.get(latest_url)
        response.raise_for_status()
        recent_data = response.json()
        
        # Filter for topic and sort by upvotes
        filtered = []
        for item in recent_data:
            paper_data = item.get('paper', item)
            title = paper_data.get('title', '').lower()
            summary = paper_data.get('summary', '').lower()
            
            if topic_lower in title or topic_lower in summary:
                filtered.append(paper_data)
                
        # Sort by upvotes (descending)
        filtered.sort(key=lambda x: x.get('upvotes', 0), reverse=True)
        
        # Add to our list
        for paper_data in filtered[:limit]:
            papers.append(paper_data)
            
    except Exception as e:
        print(f"Warning: Failed to fetch recent papers: {e}")

    # 2. If we didn't find enough recent papers for the topic, fallback to search (relevance)
    if len(papers) < limit:
        print(f"Only found {len(papers)} recent papers. Fetching historical top papers via search fallback...")
        query = urllib.parse.quote(topic)
        search_url = f"https://huggingface.co/api/papers/search?q={query}&limit={limit * 2}"
        
        try:
            response = requests.get(search_url)
            response.raise_for_status()
            search_data = response.json()
            
            existing_ids = {p.get('id') for p in papers}
            for item in search_data:
                if len(papers) >= limit:
                    break
                paper_data = item.get('paper', item)
                if paper_data.get('id') not in existing_ids:
                    papers.append(paper_data)
                    existing_ids.add(paper_data.get('id'))
        except Exception as e:
            print(f"Warning: Search fallback failed: {e}")

    # 3. Format the final output
    formatted_papers = []
    for paper_data in papers:
        paper_id = paper_data.get('id')
        title = paper_data.get('title')
        summary = paper_data.get('summary')
        authors = [author.get('name') for author in paper_data.get('authors', [])]
        published_at = paper_data.get('publishedAt')
        
        link = f"https://huggingface.co/papers/{paper_id}" if paper_id else ""
            
        formatted_papers.append({
            "id": paper_id,
            "title": title,
            "summary": summary,
            "authors": authors,
            "published_at": published_at,
            "link": link,
            "upvotes": paper_data.get('upvotes', 0)
        })
        
    return formatted_papers
