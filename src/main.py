from lexer import Lexer
from parser import Parser # type: ignore

def main():
    input_text = "CrearBD miBaseDatos; EliminarBD miBaseDatos;"
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    generated_code = parser.parse()

    # Imprime todos los comandos generados
    for command in generated_code:
        print(command)


if __name__ == "__main__":
    main()