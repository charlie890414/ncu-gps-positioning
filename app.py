from flask import Flask, render_template
import json
app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('index.html', place_list=json.load(open('json/place.json')))

@app.route('/show/<place>')
def show(place):    
    return render_template('information.html', place=place, detail=json.load(open(f'json/{place}.json')))

@app.route('/maps/<place>')
def maps(place):
    return render_template(f'maps/{place}.html')

if __name__ == "__main__":
    app.run()