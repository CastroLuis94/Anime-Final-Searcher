from flask import Flask, jsonify
from sources import animes
from crossdomain import crossdomain


app = Flask(__name__)

@app.route('/')
@crossdomain(origin='*')
def root():
    return jsonify({
        'status': 200,
        'animes': animes()
    })


if __name__ == '__main__':
    app.run()
