import re
from token import Token # type: ignore

class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []
        self.current_position = 0  # Asegúrate de que esta variable esté bien escrita

    def tokenize(self):
        token_specs = [
            ('NUM', r'\d+'),
            ('ASSIGN', r'='),
            ('END', r';'),
            ('CREARBD', r'\bCrearBD\b'),
            ('ELIMINARBD', r'\bEliminarBD\b'),
            ('CREARCOLECCION', r'\bCrearColeccion\b'),
            ('ELIMINARCOLECCION', r'\bEliminarColeccion\b'),
            ('INSERTARUNICO', r'\bInsertarUnico\b'),
            ('ACTUALIZARUNICO', r'\bActualizarUnico\b'),
            ('ELIMINARUNICO', r'\bEliminarUnico\b'),
            ('BUSCARTODO', r'\bBuscarTodo\b'),
            ('BUSCARUNICO', r'\bBuscarUnico\b'),
            ('ID', r'[A-Za-z]+'),
            ('OP', r'[+\-*/]'),
            ('SKIP', r'[ \t\n]+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
        get_token = re.compile(tok_regex).match

        pos = self.current_position
        match = get_token(self.input_text, pos)
        while match is not None:
            type = match.lastgroup
            value = match.group(type)
            if type == 'NUM':
                value = int(value)
            if type != 'SKIP' and type != 'MISMATCH':
                # # Imprimir información de cada token reconocido
                # print(f"Token: {type} Value: {value} Pos: {pos}")
                self.tokens.append(Token(type, value))
            pos = match.end()
            match = get_token(self.input_text, pos)
        self.tokens.append(Token('EOF', None))  # Agrega el token EOF
        return self.tokens
