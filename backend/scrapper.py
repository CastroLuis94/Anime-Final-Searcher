import requests
from bs4 import BeautifulSoup
from sources import Session, Anime


def anime_por_letra(letra):
    animes = []
    body = requests.get('http://jkanime.net/letra/{0}'.format(letra.upper())).text
    soup = BeautifulSoup(body)

    for table_search in soup.find_all('table', class_='search'):
        anime_data = {}
        anime_data['nombre'] = table_search.find('a', class_='titl').contents[0]
        anime_data['descripcion'] = table_search.find('p').contents[0]
        animes.append(anime_data)

    session = Session()
    for anime_data in animes:
        anime = Anime(nombre=anime_data['nombre'], descripcion=anime_data['descripcion'])
        session.add(anime)

    session.commit()
