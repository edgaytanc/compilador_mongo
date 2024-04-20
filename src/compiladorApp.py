import tkinter as tk
from tkinter import messagebox, filedialog

# Definición de la clase principal de la aplicación
class CompiladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto 2 - LFP")
        self.errores = []  # Lista para almacenar los mensajes de error
        self.root.state('zoomed')

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
        # Lógica para analizar el código
        pass

    def ver_tokens(self):
        # Lógica para ver los tokens
        pass

    def ver_errores(self):
        # Logica para mostrar los errores
        pass


