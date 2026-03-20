from feedgen.feed import FeedGenerator
import datetime
from typing import List, Dict, Any
import pytz

def build_rss_feed(papers: List[Dict[str, Any]], outputs: List[str], topic: str, file_path: str = "feed.xml"):
    """
    Builds an RSS feed from the summarized papers and saves it to a file.
    """
    fg = FeedGenerator()
    fg.id(f'huggingface-papers-{topic}')
    fg.title(f'Hugging Face Daily Papers: {topic}')
    fg.author({'name': 'Paper Newsletter System'})
    fg.link(href='https://huggingface.co/papers', rel='alternate')
    fg.description(f'Daily top papers from Hugging Face for topic: {topic}')
    
    # We should set the timezone
    tz = pytz.timezone('UTC')

    for paper, summary in zip(papers, outputs):
        fe = fg.add_entry()
        fe.id(paper['link'])
        fe.title(paper['title'])
        fe.link(href=paper['link'])
        
        # Format the description as HTML
        # feedgen expects a string for the description
        html_summary = summary.replace('\n', '<br>')
        
        description = f"""
        <h3>Abstract</h3>
        <p>{paper['summary']}</p>
        <hr>
        <h3>AI Summary</h3>
        <div>{html_summary}</div>
        <p><b>Authors:</b> {', '.join(paper['authors'])}</p>
        """
        fe.description(description)
        
        # Try to parse published_at; if it fails, use current time
        pub_date = datetime.datetime.now(tz)
        if paper.get('published_at'):
            try:
                # HF returns something like '2026-03-18T17:59:56.000Z'
                dt = datetime.datetime.fromisoformat(paper['published_at'].replace('Z', '+00:00'))
                pub_date = dt
            except ValueError:
                pass
                
        fe.published(pub_date)
        
    fg.rss_file(file_path)
    print(f"Saved RSS feed to {file_path}")
