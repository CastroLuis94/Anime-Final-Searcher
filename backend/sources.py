class Anime(object):
    def __init__(self, nombre, descripcion, tags):
        self.nombre = nombre
        self.descripcion = descripcion
        self.tags = tags

    def to_json(self):
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tags': self.tags
        }

def animes():
    return [
        Anime('Naruto', 'blah', ['pelea', 'shonen']).to_json()
    ]
