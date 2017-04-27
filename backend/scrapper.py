import requests
from bs4 import BeautifulSoup
from sources import Session, Anime


def anime_por_letra(letra):
    animes = []
    body = requests.get('http://jkanime.net/letra/{0}'.format(letra.upper())).text
    soup = BeautifulSoup(body)

    for a_titl in soup.find_all('a', class_='titl'):
        animes.append({'nombre': a_titl.contents[0], 'descripcion': ''})

    session = Session()
    for anime_data in animes:
        anime = Anime(nombre=anime_data['nombre'], descripcion=anime_data['descripcion'])
        session.add(anime)

    session.commit()
