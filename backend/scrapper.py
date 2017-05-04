import requests
from bs4 import BeautifulSoup
from sources import Session, Anime


letras = [chr(x) for x in range(ord('a'), ord('z') + 1)]
letras.append('0-9')

def anime_por_letra(letra):
    animes = []

    page_no = 1
    while True:
        body = requests.get('http://jkanime.net/letra/{0}/{1}'.format(
            letra.upper(),
            page_no
        )).text
        soup = BeautifulSoup(body, 'lxml')

        if soup.body.find_all(text='No se encontraron resultados'):
            break

        for table_search in soup.find_all('table', class_='search'):
            anime_data = {}
            anime_data['nombre'] = table_search.find('a', class_='titl').contents[0]
            anime_data['descripcion'] = str(table_search.find('p').contents[0])
            animes.append(anime_data)

        page_no += 1

    session = Session()
    for anime_data in animes:
        anime_or_none = session.query(Anime).filter_by(**anime_data).first()
        if anime_or_none is not None:
            continue

        session.add(Anime(**anime_data))

    session.commit()

def todos_los_animes(lista_letras):
    for letra in lista_letras:
        anime_por_letra(letra)

if __name__ == '__main__':
    todos_los_animes(letras)