@echo off
echo Starting HF Paper Newsletter Server...
start /B py app.py
echo.
echo ========================================================
echo Starting External Tunnel via Pinggy...
echo Look for the URL starting with "https://*" below!
echo Keep this window open to keep the server running.
echo ========================================================
ssh -p 443 -R0:localhost:5000 a.pinggy.io
