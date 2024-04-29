class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, Line: {self.line}, Col: {self.column})'

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.current_position = 0
        self.current_char = self.source_code[self.current_position] if self.source_code else None
        self.current_line = 1
        self.current_column = 1
        self.tokens = []
        self.errors = []

    def advance(self):
        """Advance the 'cursor' one character forward in the input text."""
        if self.current_char == '\n':
            self.current_line += 1
            self.current_column = 0

        self.current_position += 1
        self.current_char = self.source_code[self.current_position] if self.current_position < len(self.source_code) else None
        self.current_column += 1

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        if self.current_char == '-' and self.peek() == '-':
            self.advance()
            self.advance()
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
            self.advance()  # skip the newline
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()
            self.advance()
            while self.current_char is not None and not (self.current_char == '*' and self.peek() == '/'):
                self.advance()
            self.advance()  # skip the '*'
            self.advance()  # skip the '/'

    def peek(self):
        """Look at the next character without consuming it."""
        peek_pos = self.current_position + 1
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        return None

    def tokenize(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
            elif self.current_char == '-' and self.peek() == '-':
                self.skip_comment()
            elif self.current_char == '/' and self.peek() == '*':
                self.skip_comment()
            elif self.current_char.isalpha():  # could be a keyword or identifier
                self.tokens.append(self.identify_keyword_or_identifier())
            elif self.current_char.isdigit():
                self.tokens.append(self.number())
            elif self.current_char == '"' or self.current_char == '“' or self.current_char == '”':
                self.tokens.append(self.string())
            elif self.current_char in {'=', ';', '(', ')', '{', '}', ',', '$'}:
                self.tokens.append(self.symbol())
            else:
                self.error()

        return self.tokens

    def identify_keyword_or_identifier(self):
        result = ''
        start_line, start_column = self.current_line, self.current_column

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Mapeo correcto de palabras clave a sus tipos de token específicos
        keyword_to_token_type = {
            'CrearBD': 'CREARBD', 
            'EliminarBD': 'ELIMINARBD', 
            'CrearColeccion': 'CREARCOLECCION', 
            'EliminarColeccion': 'ELIMINARCOLECCION', 
            'InsertarUnico': 'INSERTARUNICO', 
            'ActualizarUnico': 'ACTUALIZARUNICO', 
            'EliminarUnico': 'ELIMINARUNICO', 
            'BuscarTodo': 'BUSCARTODO', 
            'BuscarUnico': 'BUSCARUNICO'
        }

        token_type = keyword_to_token_type.get(result, 'IDENTIFIER')
        return Token(token_type, result, start_line, start_column)



    def number(self):
        result = ''
        start_line, start_column = self.current_line, self.current_column

        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token('NUMBER', int(result), start_line, start_column)

    def string(self):
        result = ''
        self.advance()  # skip the initial quote
        start_line, start_column = self.current_line, self.current_column

        while self.current_char is not None and self.current_char not in {'"', '“', '”'}:
            result += self.current_char
            self.advance()

        self.advance()  # skip the closing quote
        return Token('STRING', result, start_line, start_column)

    def symbol(self):
        start_line, start_column = self.current_line, self.current_column
        symbol = self.current_char
        if self.current_char == '$' and self.peek() == 's':
            # consume the operator $set
            while self.current_char is not None and self.current_char not in {' ', ';', '\n'}:
                symbol += self.current_char
                self.advance()
            self.advance()  # Make sure to advance past the last character of the operator
        else:
            self.advance()  # Advance past the current symbol, which should include ';'
        return Token('SYMBOL', symbol, start_line, start_column)


    def error(self):
        message = f'Error lexico en la linea {self.current_line}, columna {self.current_column}. Caracter no reconocido: {self.current_char}'
        self.errors.append(message)
        self.advance()  # skip the problematic character

if __name__ == "__main__":
    # Example testing the lexer
    code = '''
        CrearBD ejemplo = nueva CrearBD(); 
EliminarBD elimina = nueva EliminarBD(); 
CrearColeccion colec = nueva CrearColeccion("NombreColeccion"); 
EliminarColeccion eliminacolec = nueva EliminarColeccion("NombreColeccion"); 
InsertarUnico insertadoc = nueva InsertarUnico("NombreColeccion", "{ 'nombre': 'Obra Literaria', 'autor': 'Jorge Luis' }"); 
ActualizarUnico actualizadoc = nueva ActualizarUnico(“NombreColeccion”, “{"nombre": "Obra Literaria"},{$set: {"autor": "Mario Vargas"}}”);    
EliminarUnico eliminadoc = nueva EliminarUnico("NombreColeccion", "{ }"); 
BuscarTodo todo = nueva BuscarTodo("NombreColeccion"); 
BuscarUnico todo = nueva BuscarUnico("NombreColeccion");
        '''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
    if lexer.errors:
        print("Errores encontrados:")
        for error in lexer.errors:
            print(error)
