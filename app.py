import os
from flask import Flask, blueprints, jsonify, request
from resources.twitter import twitter_api


app = Flask(__name__)
app.register_blueprint(twitter_api, url_prefix = '/api/v1/twitter/')

@app.route('/')
def hello():  
    return "Hello"

if __name__ == ('__main__'):
    app.run(debug=True, host=os.getenv('HOST'), port=os.getenv('PORT'))
