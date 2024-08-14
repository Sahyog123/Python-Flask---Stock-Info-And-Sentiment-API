from flask import Flask, redirect, url_for, jsonify
from bs4 import BeautifulSoup
import requests
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_stock_data(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    regularMarketPreviousClose = soup.find('fin-streamer', {'data-field': 'regularMarketPreviousClose'}).text

    regularMarketOpen = soup.find('fin-streamer', {'data-field': 'regularMarketOpen'}).text

    regularMarketDayRange = soup.find('fin-streamer',{'data-field': 'regularMarketDayRange'}).text

    fiftyTwoWeekRange = soup.find('fin-streamer',{'data-field': 'fiftyTwoWeekRange'}).text

    # Extract stock volume
    volume = soup.find('fin-streamer', {'data-field': 'regularMarketVolume'}).text

    averageVolume = soup.find('fin-streamer',{'data-field': 'averageVolume'}).text

    market_cap = soup.find('fin-streamer', {'data-field': 'marketCap'}).text

    trailingPE = soup.find('fin-streamer',{'data-field': 'trailingPE'}).text

    targetMeanPrice = soup.find('fin-streamer',{'data-field': 'targetMeanPrice'}).text

    # Extract stock price
    price = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'}).text

    return jsonify({
        "Share": ticker,
        "Regular Market Previous Close": regularMarketPreviousClose,
        "Regular Market Open": regularMarketOpen,
        "Regular Market Day Range": regularMarketDayRange,
        "Fifty Two Week Range": fiftyTwoWeekRange,
        "Volume": volume,
        "Average Volume": averageVolume,
        "Market Cap": market_cap,
        "Trailing PE": trailingPE,
        "Target Mean Price": targetMeanPrice,
        "Price": price
    })


def get_news_headlines(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/news'
    # url2 = f''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.find_all('h3', class_='clamp yf-1044anq'))

    headlines = []
    for item in soup.find_all('h3', class_='clamp yf-1044anq'):
        headlines.append(item.get_text(strip=True))

    return headlines


sia = SentimentIntensityAnalyzer()


def analyze_headlines(headlines):
    sentiment_scores = [sia.polarity_scores(headline) for headline in headlines]
    return sentiment_scores



def Get_Sentiment(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}/news'
    # url2 = f''

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup.find_all('h3', class_='clamp yf-1044anq'))

    headlines = []
    for item in soup.find_all('h3', class_='clamp yf-1044anq'):
        headlines.append(item.get_text(strip=True))

    sentiment_scores = analyze_headlines(headlines)

    total_compound = sum(score['compound'] for score in sentiment_scores)
    average_compound = total_compound / len(sentiment_scores)


    if average_compound >= 0.75:
        sentiment = "Very Positive"
    elif 0.05 <= average_compound < 0.75:
        sentiment = "Positive"
    elif -0.05 < average_compound < 0.05:
        sentiment = "Neutral"
    elif -0.75 <= average_compound <= -0.05:
        sentiment = "Negative"
    else:  # average_compound < -0.75
        sentiment = "Very Negative"


    return jsonify({
        "Ticker": ticker,
        "Total Compound Sentiment Score": total_compound,
        "Average Compound Sentiment Score": average_compound,
        "Overall Sentiment": sentiment
        })