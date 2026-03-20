import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from typing import List, Dict, Any

def send_email_newsletter(papers: List[Dict[str, Any]], outputs: List[str], topic: str):
    """
    Sends an HTML email containing the summaries of the papers using SMTP.
    """
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    
    if not all([smtp_user, smtp_pass, sender_email, receiver_email]):
        print("SMTP settings incomplete. Skipping email delivery.")
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"Hugging Face Daily Papers: {topic}"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    # Create HTML body
    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
          h1 {{ color: #2c3e50; }}
          h2 {{ color: #34495e; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
          .paper {{ margin-bottom: 40px; }}
          .summary-box {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
        </style>
      </head>
      <body>
        <h1>Hugging Face Daily Papers: {topic}</h1>
        <p>Here are your top papers for the day.</p>
    """
    
    for paper, summary in zip(papers, outputs):
        html_summary = summary.replace('\n', '<br>')
        html += f"""
        <div class="paper">
          <h2><a href="{paper['link']}">{paper['title']}</a></h2>
          <p><b>Authors:</b> {', '.join(paper['authors'])}</p>
          <div class="summary-box">
             {html_summary}
          </div>
        </div>
        """
        
    html += """
      </body>
    </html>
    """
    
    part = MIMEText(html, 'html')
    msg.attach(part)
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"Successfully sent email newsletter to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
