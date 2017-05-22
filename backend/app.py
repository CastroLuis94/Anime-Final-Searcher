from flask import Flask, jsonify, make_response, request
from sources import (
    animes,
    animes_por_letra,
    animes_agrupados_por_letra,
    crear_usuario,
    autenticar_usuario
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

    return make_response(
        jsonify({
            'status': 200,
            'size': len(all_animes_by_letter),
            'animes': all_animes_by_letter
        }), 200
    )


@app.route('/letra/<letra>')
@crossdomain(origin='*')
def por_letra(letra):
    animes_by_letter = animes_por_letra(letra)

    return make_response(
        jsonify({
            'status': 200,
            'animes': animes_by_letter
        }), 200
    )

@app.route('/users', methods=['POST'])
@crossdomain(origin='*')
def create_user():
    user = crear_usuario(
        request.form['username'],
        request.form['password']
    )
    if user:
        return make_response(
            jsonify({
                'status': 201,
                'user': {
                    'username': user.username
                }
            }), 201
        )
    return make_response(
        jsonify({
            'status': 401,
            'message': 'Validation Error'
        }), 401
    )

@app.route('/login', methods=['POST'])
@crossdomain(origin='*')
def login():
    user = autenticar_usuario(
        request.form['username'],
        request.form['password']
    )
    if user:
        return make_response(
            jsonify({
                'status': 200,
                'user': {
                    'username': user.username
                }
            }), 200
        )
    return make_response(
        jsonify({
            'status': 404,
            'message': 'Username or Password Incorrect'
        }), 401
    )

if __name__ == '__main__':
    app.run()
