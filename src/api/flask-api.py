from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, world</>'

app.run(debug=False, host='127.0.0.1', port=8080)


