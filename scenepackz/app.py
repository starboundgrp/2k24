from flask import Flask, render_template, request
from serpapi import GoogleSearch

app = Flask(__name__)

def google_search(query):
    params = {
        "q": f"site:youtube.com {query}",
        "api_key": "0498f7b260b93fd8e5e2642baa799d016aae7b651538ae2d75168d009449a84c",
        "num": 10
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    links = []
    for result in results.get("organic_results", []):
        link = result.get("link")
        if "youtube.com/watch" in link:
            links.append(link)
    return list(set(links))

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form["query"]
        yt_links = google_search(query)
        formatted_links = [(link, {
            "cobalt": "https://cobalt.tools",
            "y2mate": "https://www.y2mate.ltd",
            "snapinsta": "https://snapinsta.app/youtube-downloader"
        }) for link in yt_links[:5]]
        insta_tag = query.replace(" ", "").lower()
        results = {
            "youtube": formatted_links,
            "instagram": f"https://www.instagram.com/explore/tags/{insta_tag}/"
        }
    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
