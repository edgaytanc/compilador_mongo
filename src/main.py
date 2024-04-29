from lexer import Lexer
from parser import Parser # type: ignore
from my_ast import AST, NodoCrearBD, NodoEliminarBD, NodoCrearColeccion, NodoEliminarColeccion, NodoInsertarUnico, NodoActualizarUnico, NodoEliminarUnico, NodoBuscarTodo, NodoBuscarUnico

def main():
    # Define el código que será analizado
    code = '''
    CrearBD ejemplo = nueva CrearBD(); 
    EliminarBD elimina = nueva EliminarBD(); 
    CrearColeccion colec = nueva CrearColeccion("NombreColeccion"); 
    EliminarColeccion eliminacolec = nueva EliminarColeccion("NombreColeccion"); 
    InsertarUnico insertadoc = nueva InsertarUnico("NombreColeccion", "{ 'nombre': 'Obra Literaria', 'autor': 'Jorge Luis' }"); 
    ActualizarUnico actualizadoc = nueva ActualizarUnico("NombreColeccion", "{'nombre': 'Obra Literaria'},{$set: {'autor': 'Mario Vargas'}}");   
    EliminarUnico eliminadoc = nueva EliminarUnico(“NombreColeccion”, “{'nombre': 'Obra Literaria'}”);
    BuscarTodo todo = nueva BuscarTodo("NombreColeccion"); 
    BuscarUnico todo = nueva BuscarUnico("NombreColeccion");
    '''

    # Crea una instancia del lexer y del parser
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

    # Imprime la salida basada en el AST
    for node in ast.nodes:
        if isinstance(node, NodoCrearBD):
            print(f"use('{node.nombre}');")
        elif isinstance(node, NodoEliminarBD):
            print("db.dropDatabase();")
        elif isinstance(node, NodoCrearColeccion):
            print(f"db.createCollection('{node.nombre_coleccion}');")
        elif isinstance(node, NodoEliminarColeccion):
            print(f"db.{node.nombre_coleccion}.drop();")
        elif isinstance(node, NodoInsertarUnico):
            print(f"db.{node.coleccion}.insertOne({node.documento});")
        elif isinstance(node, NodoActualizarUnico):
            print(f"db.{node.coleccion}.updateOne({node.nuevo_valor});")
        elif isinstance(node, NodoEliminarUnico):
            print(f"db.{node.coleccion}.deleteOne({node.criterio});")
        elif isinstance(node, NodoBuscarTodo):
            print(f"db.{node.coleccion}.find();")
        elif isinstance(node, NodoBuscarUnico):
            print(f"db.{node.coleccion}.findOne();")

if __name__ == "__main__":
    main()
