# GeoGuessAnalyzer
Analyze recent GeoGuessr rounds. Generate visualizations and playable maps of rounds played previously.

## Requirements
Mac, ZSH, Python3, Chrome (for setup)

## Setup
1. Create a file in the main directory called "cookie.txt"
2. Open Chrome developer tools (shortcut Command+Alt+I)
3. Open "Network" tab
4. Navigate to www.geoguessr.com
5. Find the request on the left-hand side of the developer tools window labelled "www.geoguessr.com" and click
6. Under the "request headers" tab, find "cookie"
7. The value should start with "devicetoken=...". Copy the entire value and paste it into cookie.txt.

## Run
1. `python3 main.py`

