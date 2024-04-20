from lexer import Lexer
from token import Token # type: ignore

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_index = 0
        self.lookahead = tokens[self.current_index]

    def consume(self):
        # Incrementa el índice para apuntar al siguiente token
        self.current_index += 1
        if self.current_index < len(self.tokens):
            self.lookahead = self.tokens[self.current_index]
        else:
            # Asegúrate de manejar el final de la lista de tokens correctamente
            self.lookahead = Token('EOF', None)

    def parse(self):
        code_output = []
        while self.lookahead.type != 'EOF':
            if self.lookahead.type == 'CREARBD':
                code_output.append(self.createStatement())
            elif self.lookahead.type == 'ELIMINARBD':
                code_output.append(self.deleteStatement())
            # Se anaden nuevas funciones
            elif self.lookahead.type == 'CREARCOLECCION':
                code_output.append(self.createCollection())
            elif self.lookahead.type == 'ELIMINARCOLECCION':
                code_output.append(self.deleteCollection())
            elif self.lookahead.type == 'INSERTARUNICO':
                code_output.append(self.insertOne())
            elif self.lookahead.type == 'ACTUALIZARUNICO':
                code_output.append(self.updateOne())
            elif self.lookahead.type == 'ELIMINARUNICO':
                code_output.append(self.deleteOne())
            elif self.lookahead.type == 'BUSCARTODO':
                code_output.append(self.find())
            elif self.lookahead.type == 'BUSCARUNICO':
                code_output.append(self.findOne())
            elif self.lookahead.type == 'END':
                self.consume()  # Consume el `;` y continúa
                continue
            else:
                raise Exception(f"Syntax Error: Unexpected token {self.lookahead.type}")
            self.consume()  # Consume después de procesar cada declaración completa
        return code_output

    def createStatement(self):
        self.consume()  # Consume 'CREARBD'
        dbname = self.identifier()  # Asume que identifier devuelve el nombre
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"use('{dbname}');"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def deleteStatement(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.dropDatabase();"
        else:
            raise Exception("Syntax Error: Expected ';'")
        
    def createCollection(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.createCollection('{dbname}');"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def deleteCollection(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.drop();"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def insertOne(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.inserOne(ARCHIVO JSON);"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def updateOne(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.updateOne(ARCHIVO JSON);"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def deleteOne(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.deleteOne(ARCHIVO JSON);"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def find(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.find();"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def findOne(self):
        self.consume()  # Consume 'ELIMINARBD'
        dbname = self.identifier()
        if self.lookahead.type == 'END':
            # No consume aquí; deja que el método parse() lo maneje
            return f"db.{dbname}.findOne();"
        else:
            raise Exception("Syntax Error: Expected ';'")

    def identifier(self):
        if self.lookahead.type == 'ID':
            name = self.lookahead.value
            self.consume()  # consume el identificador
            return name
        else:
            raise Exception("Syntax Error: Expected identifier")
