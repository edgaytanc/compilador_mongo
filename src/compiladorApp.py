import tkinter as tk
from tkinter import messagebox, filedialog
from lexer import Lexer
from parser import Parser # type: ignore
from my_ast import AST, NodoCrearBD, NodoEliminarBD, NodoCrearColeccion, NodoEliminarColeccion, NodoInsertarUnico, NodoActualizarUnico, NodoEliminarUnico, NodoBuscarTodo, NodoBuscarUnico

# Definición de la clase principal de la aplicación
class CompiladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto 2 - LFP")
        self.errores = []  # Lista para almacenar los mensajes de error
        self.root.state('zoomed')
        self.code =""

        # Menú Archivo
        menu_bar = tk.Menu(root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nuevo", command=self.nuevo_archivo)
        file_menu.add_command(label="Abrir", command=self.abrir_archivo)
        file_menu.add_command(label="Guardar", command=self.guardar)
        file_menu.add_command(label="Guardar Como", command=self.guardar_como)
        file_menu.add_command(label="Salir", command=self.salir)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)

        # Menú Análisis
        analisis_menu = tk.Menu(menu_bar, tearoff=0)
        analisis_menu.add_command(label="Generar sentencias MongoDB", command=self.analizar_codigo)
        menu_bar.add_cascade(label="Análisis", menu=analisis_menu)

        # Menú Tokens
        tokens_menu = tk.Menu(menu_bar, tearoff=0)
        tokens_menu.add_command(label="Ver Tokens", command=self.ver_tokens)
        menu_bar.add_cascade(label="Tokens", menu=tokens_menu)

        # Menu Errores
        errores_menu = tk.Menu(menu_bar, tearoff=0)
        errores_menu.add_command(label="Ver Errores", command=self.ver_errores)
        menu_bar.add_cascade(label="Errores", menu=errores_menu)

        # Configurar la barra de menú
        root.config(menu=menu_bar)

        # Área de edición de código
        self.text_area = tk.Text(root)
        self.text_area.pack(expand=True, fill='both')

        # Área de errores
        self.error_area = tk.Text(root, height=10, fg='red')
        self.error_area.pack(expand=False, fill='both')
    
    def nuevo_archivo(self):
        if messagebox.askyesno("Guardar", "¿Desea guardar los cambios antes de crear un nuevo archivo?"):
            self.guardar_como()
        self.text_area.delete('1.0', tk.END)

    def abrir_archivo(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
        )
        if not filepath:
            return
        self.text_area.delete('1.0', tk.END)
        with open(filepath, 'r', encoding='utf-8') as input_file:
            text = input_file.read()
            self.text_area.insert(tk.END, text)
        self.root.title(f"Proyecto 2 - LFP - {filepath}")

    def guardar(self):
        current_text = self.text_area.get('1.0', tk.END)
        filepath = filedialog.asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(current_text)
        self.root.title(f"Proyecto 2 - LFP - {filepath}")

    def guardar_como(self):
        current_text = self.text_area.get('1.0', tk.END)
        filepath = filedialog.asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, 'w', encoding='utf-8') as output_file:
            output_file.write(current_text)
        self.root.title(f"Proyecto 2 - LFP - {filepath}")

    def salir(self):
       if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.root.destroy()

    def analizar_codigo(self):
        code = self.text_area.get('1.0', tk.END)
        print("Código a analizar:", code)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        if lexer.errors:
            error_msg = "\n".join(lexer.errors)
            self.error_area.delete('1.0', tk.END)
            self.error_area.insert('1.0', error_msg)
            return
        
        parser = Parser(tokens)
        ast = parser.parse()
        # self.error_area.insert(parser.errors)
        if parser.errors:
            error_msg = "\n".join(parser.errors)
            self.error_area.delete('1.0', tk.END)
            self.error_area.insert('1.0', error_msg)
            return
        
        self.mostrar_resultados(ast)

    def mostrar_resultados(self, ast):
        output = []
        for node in ast.nodes:
            if isinstance(node, NodoCrearBD):
                output.append(f"use('{node.nombre}');")
            elif isinstance(node, NodoEliminarBD):
                output.append("db.dropDatabase();")
            elif isinstance(node, NodoCrearColeccion):
                output.append(f"db.createCollection('{node.nombre_coleccion}');")
            elif isinstance(node, NodoEliminarColeccion):
                output.append(f"db.{node.nombre_coleccion}.drop();")
            elif isinstance(node, NodoInsertarUnico):
                output.append(f"db.{node.coleccion}.insertOne({node.documento});")
            elif isinstance(node, NodoActualizarUnico):
                output.append(f"db.{node.coleccion}.updateOne({node.nuevo_valor});")
            elif isinstance(node, NodoEliminarUnico):
                output.append(f"db.{node.coleccion}.deleteOne({node.criterio});")
            elif isinstance(node, NodoBuscarTodo):
                output.append(f"db.{node.coleccion}.find();")
            elif isinstance(node, NodoBuscarUnico):
                output.append(f"db.{node.coleccion}.findOne();")
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert('1.0', '\n'.join(output))

    def mostrar_errores(self, errors):
        messagebox.showerror("Errores de compilación", "\n".join(errors))



    def ver_tokens(self):
        code = self.text_area.get('1.0', tk.END)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        display_text = '\n'.join(str(token) for token in tokens)
        messagebox.showinfo("Tokens", display_text)

    def ver_errores(self):
        # Limpia el área de errores antes de mostrar los nuevos
        self.error_area.delete('1.0', tk.END)

        # Agrega cada error en la lista de errores al área de texto de errores
        if self.errores:
            for error in self.errores:
                self.error_area.insert(tk.END, error + "\n")
        else:
            self.error_area.insert(tk.END, "No se encontraron errores.")



if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorApp(root)
    root.mainloop()



