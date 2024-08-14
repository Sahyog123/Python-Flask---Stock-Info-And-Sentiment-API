from flask import Flask
import implementation

app = Flask(__name__)

@app.route("/Hello")
def home():
    return "Hello World, Flask"


@app.route("/info/<ticker>", methods=["POST"])
def getInfo(ticker):
    return implementation.get_stock_data(ticker)


@app.route("/news/<ticker>", methods=["POST"])
def getHeadlines(ticker):
    return implementation.get_news_headlines(ticker)


@app.route("/sentiment/<ticker>", methods=["POST"])
def getSentiment(ticker):
    return implementation.Get_Sentiment(ticker)


