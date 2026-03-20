import os
import datetime
from typing import List, Dict, Any

def build_web_page(papers: List[Dict[str, Any]], outputs: List[str], topic: str, file_path: str = "index.html"):
    """
    Builds a stunning, responsive static HTML page with modern CSS to view the papers.
    Uses glassmorphism, nice gradients, and Google Fonts.
    """
    
    # generate the paper cards
    cards_html = ""
    for paper, summary in zip(papers, outputs):
        html_summary = summary.replace('\n', '<br>')
        
        # safely get authors and summary
        authors_str = ', '.join(paper.get('authors', []))
        paper_abstract = paper.get('summary', '')
        # limit abstract length for UI compactness
        if len(paper_abstract) > 300:
            paper_abstract = paper_abstract[:300] + "..."
            
        cards_html += f"""
        <div class="card">
            <h2><a href="{paper['link']}" target="_blank">{paper['title']}</a></h2>
            <p class="authors"><strong>Authors:</strong> {authors_str}</p>
            <div class="abstract">
                <p>{paper_abstract}</p>
            </div>
            <div class="summary-box">
                {html_summary}
            </div>
            <a href="{paper['link']}" target="_blank" class="read-more">Read Paper &rarr;</a>
        </div>
        """

    current_date = datetime.datetime.now().strftime("%B %d, %Y")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hugging Face Daily Papers: {topic}</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-gradient-start: #0f172a;
            --bg-gradient-end: #1e1b4b;
            --primary-accent: #6ee7b7;
            --secondary-accent: #3b82f6;
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--bg-gradient-start), var(--bg-gradient-end));
            background-attachment: fixed;
            color: var(--text-primary);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }}

        header {{
            text-align: center;
            padding: 4rem 2rem 2rem;
            width: 100%;
            max-width: 900px;
        }}

        h1 {{
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0;
            background: -webkit-linear-gradient(45deg, var(--primary-accent), var(--secondary-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }}

        .subtitle {{
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-top: 10px;
            font-weight: 300;
        }}

        .container {{
            width: 100%;
            max-width: 900px;
            padding: 0 2rem 4rem;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        }}

        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            border-color: rgba(255, 255, 255, 0.2);
        }}

        .card h2 {{
            margin-top: 0;
            font-size: 1.8rem;
            line-height: 1.3;
        }}

        .card h2 a {{
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        .card h2 a:hover {{
            color: var(--primary-accent);
        }}

        .authors {{
            color: var(--secondary-accent);
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }}

        .abstract {{
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
            padding-left: 1rem;
            border-left: 3px solid var(--card-border);
        }}

        .summary-box {{
            background: rgba(0, 0, 0, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            font-size: 0.95rem;
            line-height: 1.7;
        }}

        .summary-box h3 {{
            color: var(--primary-accent);
            margin-top: 0;
            font-size: 1.1rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }}
        
        .summary-box h3:not(:first-child) {{
            margin-top: 1.5rem;
        }}

        .read-more {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(45deg, var(--secondary-accent), var(--primary-accent));
            color: #fff;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: opacity 0.2s ease, transform 0.2s ease;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
        }}

        .read-more:hover {{
            opacity: 0.9;
            transform: scale(1.05);
        }}

        @media (max-width: 768px) {{
            h1 {{
                font-size: 2.5rem;
            }}
            .card {{
                padding: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <h1>Daily AI Papers</h1>
        <div class="subtitle">Focus: <strong>{topic}</strong> &mdash; {current_date}</div>
    </header>
    <div class="container">
        {cards_html}
    </div>
</body>
</html>"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated gorgeous webpage at {file_path}")
