from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    with open('website/books.json', 'r') as f:
        books = json.load(f)
    return render_template('index.html', books=books)
if __name__ == '__main__':
    app.run(debug=True)
