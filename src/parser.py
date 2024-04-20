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
            return f"use {dbname};"
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

    def identifier(self):
        if self.lookahead.type == 'ID':
            name = self.lookahead.value
            self.consume()  # consume el identificador
            return name
        else:
            raise Exception("Syntax Error: Expected identifier")
