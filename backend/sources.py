from sqlalchemy import create_engine, Column, Integer, String, Index, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from unidecode import unidecode


engine = create_engine('sqlite:///animes.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Anime(Base):
    __tablename__ = 'animes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    descripcion = Column(String)
    url = Column(String)
    tags = relationship("Tag", secondary='animes_tags', viewonly=True)

    idx_nombre_descripcion = Index('idx_nombre_descripcion', nombre, descripcion, unique=True)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tags': self.tags
        }

    def __repr__(self):
        return "<Anime[{0}] nombre='{1}' descipcion='{2}...'>".format(
            self.id,
            self.nombre,
            self.descripcion[:20]
        )

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    animes = relationship("Anime", secondary='animes_tags', viewonly=True)
    

class AnimeTag(Base):
    __tablename__ = 'animes_tags'

    id = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey('animes.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))

    idx_anime_tag = Index('idx_anime_tag', anime_id, tag_id, unique=True)


def animes():
    session = Session()
    return [anime.to_json()
            for anime in session.query(Anime).all()]


def animes_por_letra(letra):
    session = Session()
    return [anime.to_json()
            for anime in session.query(Anime).filter(
                Anime.nombre.like('{0}%'.format(letra))
            ).all()]


def animes_agrupados_por_letra():
    animes = {}

    session = Session()
    for letra, anime in session.query(func.substr(Anime.nombre, 1, 1), Anime).all():
        letra = unidecode(letra.lower())

        if letra in [str(i) for i in range(0, 10)]:
            if '0-9' not in animes:
                animes['0-9'] = []
            animes['0-9'].append(anime.to_json())
            continue

        if letra not in animes:
            animes[letra] = []
        animes[letra].append(anime.to_json())

    return animes
