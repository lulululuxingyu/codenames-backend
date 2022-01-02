from flask import Flask, Response, request
from flask_cors import CORS
import random
import json
import pickle

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "hello world"

@app.route('/newgame', methods=['GET'])
def newgame():
    # initialize cards
    words = []
    with open('words.txt', 'r') as f:
        words = random.sample(f.read().replace('\n', ' ').split(' '), 25)
    random.shuffle(words)
    
    colors = [
        "LightCoral", "LightCoral", "LightCoral", "LightCoral", "LightCoral", "LightCoral", "LightCoral", "LightCoral", "LightCoral",
        "CornflowerBlue", "CornflowerBlue", "CornflowerBlue", "CornflowerBlue", "CornflowerBlue", "CornflowerBlue", "CornflowerBlue", "CornflowerBlue",
        "Gold", "Gold", "Gold", "Gold", "Gold", "Gold", "Gold",
        "grey"
    ]
    random.shuffle(colors)

    cards = []
    for i in range(25):
        cards.append({
            'word': words[i],
            'color': colors[i],
            'isClicked': False
        })
    
    # save cards to db
    with open('cards.pickle', 'wb') as f:
        pickle.dump(cards, f)

    rsp = Response(json.dumps(cards), status=200, content_type="application/json")
    return rsp

@app.route('/resumegame', methods=['GET'])
def resumegame():
    with open('cards.pickle', 'rb') as f:
        cards = pickle.load(f)

    rsp = Response(json.dumps(cards), status=200, content_type="application/json")
    return rsp

@app.route('/clickcard', methods=['POST'])
def clickcard():
    # process request
    card_index = request.get_json()['cardIndex']

    # update db
    with open('cards.pickle', 'rb') as f:
        cards = pickle.load(f)
    cards[card_index]['isClicked'] = True
    with open('cards.pickle', 'wb') as f:
        pickle.dump(cards, f)
    
    # make response
    rsp = Response("Successfully clicked card!", status=200)
    return rsp

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
