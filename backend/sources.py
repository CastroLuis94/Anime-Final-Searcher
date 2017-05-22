from sqlalchemy import create_engine, Column, Integer, String, Index, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from unidecode import unidecode
from utils import hash_


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
            'tags': [ tag.nombre for tag in self.tags ]
        }

    def __repr__(self):
        return "<Anime[{0}] nombre='{1}' descipcion='{2}' tags=[{3}]>".format(
            self.id,
            self.nombre,
            "{0}...".format(self.descripcion[:20]) if self.descripcion is not None else '',
            ', '.join("'{0}'".format(tag.nombre) for tag in self.tags)
        )

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    animes = relationship("Anime", secondary='animes_tags', viewonly=True)

    def __repr__(self):
        return "<Tag[{0}] nombre='{1}'>".format(
            self.id,
            self.nombre
        )


class AnimeTag(Base):
    __tablename__ = 'animes_tags'

    id = Column(Integer, primary_key=True)
    anime_id = Column(Integer, ForeignKey('animes.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    anime = relationship("Anime")
    tag = relationship("Tag")

    idx_anime_tag = Index('idx_anime_tag', anime_id, tag_id, unique=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    _password = Column(String)
    animes = relationship("Anime", secondary='users_animes', viewonly=True)

    def __init__(self, *args, **kwargs):
        for p in ['password', '_password']:
            if p in kwargs:
                self._password = hash_(kwargs[p])
                del(kwargs[p])
        super(User, self).__init__(*args, **kwargs)

    def authenticate(self, pass_):
        return self.password == hash_(pass_)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pass_):
        self._password = hash_(pass_)


class UserAnime(Base):
    __tablename__ = 'users_animes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    anime_id = Column(Integer, ForeignKey('animes.id'))
    users = relationship("User")
    anime = relationship("Anime")

    idx_anime_user = Index('idx_anime_user', anime_id, user_id, unique=True)


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

def crear_usuario(username, password):
    session = Session()

    try:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()
        return user
    except:
        return False

def autenticar_usuario(username, password):
    session = Session()

    user = session.query(User).filter_by(username=username).first()
    if user and user.authenticate(password):
        return user
    return False
