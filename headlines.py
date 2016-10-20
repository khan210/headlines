import feedparser
import json
import urllib2
import urllib
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
api_url= 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&\
appid=368707a5e2b142653612d1a7ed80477d'

currency_url= 'http://openexchangerates.org//api/latest.json?\
app_id=1191ca17ac684d079a7912b8a1582cda'


DEFAULTS =  {'publication' : 'bbc' ,
             'city' : 'Islamabad,Pakistan',
             'currency_from' : "GBP" ,
             'currency_to' : "USD"}



@app.route("/")

def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from , currency_to)          
    return render_template("home.html", articles= articles, \
weather = weather , currency_from = currency_from , \
currency_to = currency_to , rate = rate , \
currencies= sorted(currencies))

def get_news(query):
    if not query or query.lower() not in rss_feeds:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()

    feed = feedparser.parse(rss_feeds[publication])
    return feed['entries']

    

def get_weather(query): 
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description" : parsed ["weather"][0]["description"],
                   "temperature" : parsed ["main"]["temp"],
                   "city" : parsed ["name"],
                   "country" : parsed["sys"]["country"]
                   }
    return weather

def get_rate(frm, to):
    all_currency = urllib2.urlopen(currency_url).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate , parsed.keys())
                
    return render_template('home.html' , articles = feed['entries'] , weather=weather)





if __name__ == "__main__":
    app.run(port=5000 , debug=True)
