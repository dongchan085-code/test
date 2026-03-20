from flask import Flask, send_file, render_template_string, jsonify
import os
import subprocess

app = Flask(__name__)

@app.route("/")
def index():
    if not os.path.exists("index.html"):
        return "<h3>Welcome! No newsletter generated yet. Please run <a href='/generate'>/generate</a> to fetch today's papers.</h3>", 404
    return send_file("index.html")

@app.route("/rss")
def rss():
    if not os.path.exists("feed.xml"):
        return "No RSS feed generated yet.", 404
    return send_file("feed.xml", mimetype="application/rss+xml")

@app.route("/generate")
def generate():
    """Endpoint to trigger a fresh build of the newsletter"""
    try:
        # We invoke main.py as a script to let it do the heavy lifting
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"status": "success", "message": "Successfully generated new papers", "logs": result.stdout})
        else:
            return jsonify({"status": "error", "message": "Failed to generate", "logs": result.stderr}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
