from lexer import Lexer
from parser import Parser # type: ignore
from compiladorApp import CompiladorApp
import tkinter as tk
from tkinter import messagebox, filedialog

def main():
    input_text = """CrearBD miBaseDatos; 
    EliminarBD miBaseDatos;
    CrearColeccion miColeccion;"""
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    generated_code = parser.parse()

    # Imprime todos los comandos generados
    for command in generated_code:
        print(command)

def app():
    root = tk.Tk()
    application = CompiladorApp(root)
    root.mainloop()

    


if __name__ == "__main__":
    main()
    app()