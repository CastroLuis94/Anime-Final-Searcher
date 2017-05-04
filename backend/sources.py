from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///animes.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Anime(Base):
    __tablename__ = 'animes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    descripcion = Column(String)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }


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
