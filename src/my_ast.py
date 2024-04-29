class AST:
    """Clase para representar el Árbol Sintáctico Abstracto."""
    def __init__(self):
        self.nodes = []

    def __repr__(self):
        return f'AST({self.nodes})'

class Nodo:
    """Clase base para todos los nodos del AST."""
    pass

class NodoCrearBD(Nodo):
    """Nodo para representar la creación de una base de datos."""
    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f'NodoCrearBD(nombre={self.nombre})'

class NodoEliminarBD(Nodo):
    """ Nodo para representar la eliminación de una base de datos. """
    def __init__(self, nombre=None):  # Haz opcional el nombre si es necesario
        self.nombre = nombre

    def __repr__(self):
        return f'NodoEliminarBD(nombre={self.nombre})'


class NodoCrearColeccion(Nodo):
    """Nodo para representar la creación de una colección."""
    def __init__(self, nombre_coleccion):
        self.nombre_coleccion = nombre_coleccion

    def __repr__(self):
        return f'NodoCrearColeccion(nombre_coleccion={self.nombre_coleccion})'

class NodoEliminarColeccion(Nodo):
    """Nodo para representar la eliminación de una colección."""
    def __init__(self, nombre_coleccion):
        self.nombre_coleccion = nombre_coleccion

    def __repr__(self):
        return f'NodoEliminarColeccion(nombre_coleccion={self.nombre_coleccion})'

class NodoInsertarUnico(Nodo):
    """Nodo para representar la inserción de un documento único en una colección."""
    def __init__(self, coleccion, documento):
        self.coleccion = coleccion
        self.documento = documento

    def __repr__(self):
        return f'NodoInsertarUnico(coleccion={self.coleccion}, documento={self.documento})'

class NodoActualizarUnico(Nodo):
    """Nodo para representar la actualización de un documento único."""
    def __init__(self, coleccion, criterio, nuevo_valor):
        self.coleccion = coleccion
        self.criterio = criterio
        self.nuevo_valor = nuevo_valor

    def __repr__(self):
        return f'NodoActualizarUnico(coleccion={self.coleccion}, criterio={self.criterio}, nuevo_valor={self.nuevo_valor})'

class NodoEliminarUnico(Nodo):
    """Nodo para representar la eliminación de un documento único."""
    def __init__(self, coleccion, criterio):
        self.coleccion = coleccion
        self.criterio = criterio

    def __repr__(self):
        return f'NodoEliminarUnico(coleccion={self.coleccion}, criterio={self.criterio})'

class NodoBuscarTodo(Nodo):
    """Nodo para representar la búsqueda de todos los documentos en una colección."""
    def __init__(self, coleccion):
        self.coleccion = coleccion

    def __repr__(self):
        return f'NodoBuscarTodo(coleccion={self.coleccion})'

class NodoBuscarUnico(Nodo):
    """Nodo para representar la búsqueda de un único documento en una colección."""
    def __init__(self, coleccion, criterio=None):
        self.coleccion = coleccion
        self.criterio = criterio

    def __repr__(self):
        return f'NodoBuscarUnico(coleccion={self.coleccion})'
