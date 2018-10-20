import os
from flask import request, Flask, blueprints
from twit import twit_api

app = Flask(__name__)
app.register_blueprint(twit_api, url_prefix = '/tweet/')

@app.route('/')
def first():
    return "Tweets Program"

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('HOST'), port=os.getenv('PORT'))