from lexer import Lexer
from parser import Parser # type: ignore
from my_ast import AST, NodoCrearBD, NodoEliminarBD, NodoCrearColeccion, NodoEliminarColeccion, NodoInsertarUnico, NodoActualizarUnico, NodoEliminarUnico, NodoBuscarTodo, NodoBuscarUnico

def main():
    # Define el código que será analizado
    code = '''
CrearBD DBEjemplo = new CrearBD();
EliminarBD DBEjemplo = new EliminarBD();
CrearBD Futbol = new CrearBD();
CrearColeccion nuevaColeccion = new CrearColeccion("Calificacion");
EliminarColeccion eliminarColeccion = new EliminarColeccion("Calificacion");
CrearColeccion nuevaColeccion = new CrearColeccion("Futbolistas");
--- Messi el único GOAT
InsertarUnico insertarFutbolista = new InsertarUnico("Futbolistas", 
{ 
    "nombre": "Lionel Messi",
    "club": "Paris Saint-Germain"
}

/* 
	Es que Haaland es muy bueno también, pero bueno, centrémonos en LFP :D
*/
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
InsertarUnico insertarFutbolista = new InsertarUnico("Futbolistas", 
{ 
    "nombre": "Erling Haaland",
    "club": "Manchester City"
}
);
ActualizarUnico actualizarFutbolista = new ActualizarUnico("Futbolistas", 
{
    "nombre": "Lionel Messi" 
}, 
{ 
     $set: { "club": "Inter Miami" } 
}
);
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
EliminarUnico eliminarFutbolista = new EliminarUnico("Futbolistas", 
{ 
     "nombre": "Lionel Messi" 
}
);
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");
/* 
	Eliminamos a Haaland para verificar el flujo de información
*/
EliminarUnico eliminarFutbolista2 = new EliminarUnico("Futbolistas",
{
      "nombre": "Erling Haaland"
}
);
/* 
	No debería de haber nada en la colección
*/
BuscarTodo todosFutbolistas = new BuscarTodo("Futbolistas");
BuscarUnico unFutbolista = new BuscarUnico("Futbolistas");

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
