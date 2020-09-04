import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import credantials
import pymongo
from pymongo import MongoClient
from mysql import connector
from datetime import datetime,timedelta
import multiprocessing
from textblob import TextBlob
import re
import plotly.express as px
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([

        dcc.Graph(id='graph'),
        dcc.Interval(
        id="interval_10min",
        interval=1*1000,
        n_intervals=100)
])])


@app.callback(
    Output('graph', 'figure'),
    [Input('interval_10min', 'n_intervals')])

def update_figure(data):
    try:
        mydb=connector.connect(
            host="localhost",
            user="root",
            password="",
            database="CoronaTweets",
            charset='utf8'
        )
        print("connected")
    except Exception as e:
        print("Not Connect to Database")



    query = "SELECT id_str, tweet_text, created_at,user_location,polarity,subjectivity FROM CoronaTweetData"
    df = pd.read_sql(query, con=mydb)


    Topic=''.join(df['tweet_text']).lower()
    word_tokenization=word_tokenize(Topic)
    stop_words=set(stopwords.words("english"))

    CleanText=[]
    for i in word_tokenization:
        if i not in stop_words:
            CleanText.append(i)

    FrequentTopics=FreqDist(CleanText)
    HotTopics=pd.DataFrame(FrequentTopics.most_common(10),columns=["Words","Frequency"]).drop(0)
    X=HotTopics['Words']
    Y=HotTopics ['Frequency']

    data=go.Bar(
        x=X,
        y=Y,
        name="BarChart"
    )

    return {'data':[data],}

if __name__ == '__main__':
    app.run_server(debug=True)