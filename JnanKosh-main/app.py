from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# API Keys (Replace with your actual API keys)
GOOGLE_API_KEY = "AIzaSyDKBxIo9luZJaixPwGZ4MOIrfGV9rlWae8"
GOOGLE_CX = "e75f47581696d4d0a"
YOUTUBE_API_KEY = "AIzaSyBON0ShwhTdMD-6-RFk3222M0iwHaBWTCY"

@app.route('/')
def index():
    return render_template('new.html')  # Serve new.html

@app.route('/nextpage')
def next_page():
    return render_template('nextpage.html')

@app.route('/search', methods=['POST'])
def search():
    topic = request.form.get('topic')

    google_results = fetch_from_google(topic)
    youtube_results = fetch_from_youtube(topic)

    google_data = [normalize_google_result(item) for item in google_results]
    youtube_data = [normalize_youtube_result(item) for item in youtube_results]

    combined_results = google_data + youtube_data
    ranked_results = rank_content(combined_results)

    return render_template('results.html', results=ranked_results)

def fetch_from_google(topic):
    url = f"https://www.googleapis.com/customsearch/v1?q={topic}&key={GOOGLE_API_KEY}&cx={GOOGLE_CX}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def fetch_from_youtube(topic):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={topic}&type=video&key={YOUTUBE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('items', [])
    return []

def normalize_google_result(item):
    return {
        'title': item.get('title'),
        'link': item.get('link'),
        'snippet': item.get('snippet'),
        'source': 'Google'
    }

def normalize_youtube_result(item):
    return {
        'title': item['snippet']['title'],
        'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        'snippet': item['snippet']['description'],
        'source': 'YouTube'
    }

def rank_content(items):
    source_priority = {'Google': 1, 'YouTube': 2}
    return sorted(items, key=lambda x: source_priority.get(x['source'], 99))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
