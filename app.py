from flask import Flask

app = Flask(__name__)

@app.route('/<name>')

def index(name):
    return '<h1>Hola {}!<h1>'.format(name)