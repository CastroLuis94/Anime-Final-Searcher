from flask import Flask, jsonify
from sources import (
    animes,
    animes_por_letra,
    animes_agrupados_por_letra
)
from crossdomain import crossdomain


app = Flask(__name__)

@app.route('/')
@crossdomain(origin='*')
def all():
    all_animes = animes()

    return jsonify({
        'status': 200,
        'size': len(all_animes),
        'animes': all_animes
    })


@app.route('/letra')
@crossdomain(origin='*')
def all_by_letter():
    all_animes_by_letter = animes_agrupados_por_letra()

    return jsonify({
        'status': 200,
        'size': len(all_animes_by_letter),
        'animes': all_animes_by_letter
    })


@app.route('/letra/<letra>')
@crossdomain(origin='*')
def por_letra(letra):
    animes_by_letter = animes_por_letra(letra)

    return jsonify({
        'status': 200,
        'animes': animes_by_letter
    })

if __name__ == '__main__':
    app.run()
