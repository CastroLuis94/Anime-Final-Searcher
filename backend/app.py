from flask import Flask, jsonify
from sources import animes, animes_por_letra
from crossdomain import crossdomain


app = Flask(__name__)

@app.route('/')
@crossdomain(origin='*')
def root():
    return jsonify({
        'status': 200,
        'animes': animes()
    })

@app.route('/letra/<letra>')
@crossdomain(origin='*')
def por_letra(letra):
    return jsonify({
        'status': 200,
        'animes': animes_por_letra(letra)
    })

if __name__ == '__main__':
    app.run()
