from flask import Flask, jsonify
from sources import animes

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({
        'status': 200,
        'animes': animes()
    })


if __name__ == '__main__':
    app.run()
