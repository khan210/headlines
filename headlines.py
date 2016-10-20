import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

rss_feeds = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn' : 'http://rss.cnn.com/rss/edition.rss',
             'fox' : 'http://feeds.foxnews.com/foxnews/latest',
             'iol' : 'http://classic.iol.co.za/cmlink/1.640',
             'guardian' : 'https://www.theguardian.com/world/rss',
             'express' : 'http://feeds.feedburner.com/daily-express-nature'}

@app.route("/")
@app.route("/<publication>")
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in rss_feeds:
        publication = "bbc"
    else:
        publication = query.lower()

    feed = feedparser.parse(rss_feeds[publication])
    return render_template('home.html' , articles = feed['entries'])
if __name__ == "__main__":
    app.run(port=5000 , debug=True)
