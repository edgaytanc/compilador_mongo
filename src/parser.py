from my_ast import AST, NodoCrearBD, NodoEliminarBD, NodoCrearColeccion, NodoEliminarColeccion, NodoInsertarUnico, NodoActualizarUnico, NodoEliminarUnico, NodoBuscarTodo, NodoBuscarUnico

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.ast = AST()
        self.errors = []  # Inicializa la lista de errores

    def error(self, message):
        """Agrega un mensaje de error a la lista de errores."""
        self.errors.append(message)

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def parse(self):
        while self.current_token() is not None:
            if self.current_token().type == 'CREARBD':
                self.parse_crear_bd()
            elif self.current_token().type == 'ELIMINARBD':
                self.parse_eliminar_bd()
            elif self.current_token().type == 'CREARCOLECCION':
                self.parse_crear_coleccion()
            elif self.current_token().type == 'ELIMINARCOLECCION':
                self.parse_eliminar_coleccion()
            elif self.current_token().type == 'INSERTARUNICO':
                self.parse_insertar_unico()
            elif self.current_token().type == 'ACTUALIZARUNICO':
                self.parse_actualizar_unico()
            elif self.current_token().type == 'ELIMINARUNICO':
                self.parse_eliminar_unico()
            elif self.current_token().type == 'BUSCARTODO':
                self.parse_buscar_todo()
            elif self.current_token().type == 'BUSCARUNICO':
                self.parse_buscar_unico()
            self.advance()
        return self.ast

    def parse_crear_bd(self):
        if self.current_token().type != 'CREARBD':
            return  # Asegúrate de estar en el token correcto al comenzar el método.
        
        self.advance()  # Avanza al IDENTIFIER del nombre de la base de datos.
        if self.current_token().type == 'IDENTIFIER':
            nombre = self.current_token().value
            self.ast.nodes.append(NodoCrearBD(nombre))
            self.advance()  # Avanza al ';'
        else:
            self.error("Expected an identifier for database name.")
        
        self.advance()  # Debería moverse al siguiente comando o finalizar.


    def parse_eliminar_bd(self):
        self.advance()  # Avanza al token 'EliminarBD'
        if self.current_token().type == 'IDENTIFIER':
            # Aquí se podría capturar el identificador si fuera necesario usarlo, pero lo ignoramos
            self.advance()  # Avanza al '=', ignoramos el 'nombre' de la base de datos
            self.advance()  # Avanza a 'nueva'
            self.advance()  # Avanza a 'EliminarBD'
            self.advance()  # Avanza al '()'
            self.advance()  # Avanza al ';'
        else:
            self.error("Expected identifier after 'EliminarBD'")  # Manejo de errores si la estructura no es correcta

        # Añade el nodo al AST sin ningún nombre específico
        self.ast.nodes.append(NodoEliminarBD())


    def parse_crear_coleccion(self):
        self.advance()  # Avanza al token 'CrearColeccion'
        if self.current_token().type == 'IDENTIFIER':
            coleccion_variable = self.current_token().value
            self.advance()  # Avanza al '='
            self.advance()  # Avanza al 'nueva'
            self.advance()  # Avanza a 'CrearColeccion'
            if self.current_token().type == 'STRING':
                nombre_coleccion = self.current_token().value  # Captura el nombre de la colección
                self.advance()  # Avanza al ';'
            else:
                self.error("Expected collection name as string.")
        else:
            self.error("Expected identifier after 'CrearColeccion'")

        # Añade el nodo al AST usando el nombre de la variable como el identificador de la colección
        self.ast.nodes.append(NodoCrearColeccion(coleccion_variable))


    def parse_eliminar_coleccion(self):
        self.advance()  # Avanza al token 'EliminarColeccion'
        if self.current_token().type == 'IDENTIFIER':
            coleccion_variable = self.current_token().value
            self.advance()  # Avanza al '='
            self.advance()  # Avanza al 'nueva'
            self.advance()  # Avanza a 'EliminarColeccion'
            self.advance()  # Avanza al '('
            self.advance()  # Avanza al nombre de la colección entre comillas, aunque no se usa
            self.advance()  # Avanza al ')'
            self.advance()  # Avanza al ';'
        else:
            self.error("Expected identifier after 'EliminarColeccion'")

        # Añade el nodo al AST usando el nombre de la variable como el identificador de la colección
        self.ast.nodes.append(NodoEliminarColeccion(coleccion_variable))


    def parse_insertar_unico(self):
        self.advance()  # Avanza al token 'INSERTARUNICO'
        # print(self.current_token().type)
        if self.current_token().type != 'IDENTIFIER':
            self.error("Expected identifier after 'InsertarUnico'")
            return
        # print(self.current_token().value)
        coleccion_variable = self.current_token().value
        self.advance()  # Avanza al '='
        self.advance()  # Avanza al 'nueva'
        self.advance()  # Avanza a 'InsertarUnico'
        self.advance()  # Avanza al '('
        self.advance()
        # print(self.current_token().value)
        # El próximo token debe ser el nombre de la colección, no se utiliza, pero debemos consumirlo.
        if self.current_token().type != 'STRING':
            self.error("Expected string for collection name")
            return
        coleccion_variable = self.current_token().value
        self.advance()  # Avanza al nombre de la colección
        # print(self.current_token().value)
        
        # El próximo token debe ser una coma antes del documento JSON.
        if self.current_token().value != ',':
            self.error("Expected ',' after collection name")
            return
        self.advance()  # Avanza a la coma

        # Ahora capturamos el documento JSON.
        if self.current_token().type != 'STRING':
            self.error("Expected JSON document as string")
            return
        documento_json = self.current_token().value
        self.advance()  # Avanza al documento JSON
        self.advance()  # Avanza al ')'
        # self.advance()  # Avanza al ';'
        # print(self.current_token().value)
        # Añadir el nodo con la colección correcta y el documento JSON.
        self.ast.nodes.append(NodoInsertarUnico(coleccion_variable, documento_json))




    def parse_actualizar_unico(self):
        self.advance()  # Avanza al token 'ACTUALIZARUNICO'
        # print(self.current_token().value)
        if self.current_token().type != 'IDENTIFIER':
            self.error("Expected identifier after 'ActualizarUnico'")
            print("aqui salio")
            return
        # print(self.current_token().value)
        coleccion_variable = self.current_token().value
        self.advance()  # Avanza al '='
        self.advance()  # Avanza al 'nueva'
        self.advance()  # Avanza a 'ActualizarUnico'
        self.advance()  # Avanza al '('
        self.advance()
        # print(self.current_token().value)
        # Capturar el criterio JSON
        if self.current_token().type != 'STRING':
            self.error("Expected JSON document as string for criteria")
            return
        coleccion_variable = self.current_token().value
        criterio = self.current_token().value
        self.advance()  # Avanza al criterio JSON
        # print(self.current_token().value)
        # Avanzar al separador de criterio y nuevo valor
        if self.current_token().value != ',':
            self.error("Expected ',' after criteria JSON")
            return
        self.advance()  # Avanza a la coma
        # print(self.current_token().value)
        # Capturar el nuevo valor JSON
        if self.current_token().type != 'STRING':
            self.error("Expected JSON document as string for new value")
            return
        
        nuevo_valor = self.current_token().value
        self.advance()  # Avanza al nuevo valor JSON
        self.advance()  # Avanza al ')'
        # self.advance()  # Avanza al ';'
        # print(self.current_token().value)
        # Añadir el nodo al AST
        self.ast.nodes.append(NodoActualizarUnico(coleccion_variable, criterio, nuevo_valor))


    def parse_eliminar_unico(self):
        self.advance()  # Avanza al token 'ELIMINARUNICO'
        # print(self.current_token().value)
        if self.current_token().type != 'IDENTIFIER':
            self.error("Expected identifier after 'EliminarUnico'")
            return
        
        coleccion_variable = self.current_token().value
        self.advance()  # Avanza al '='
        self.advance()  # Avanza al 'nueva'
        self.advance()  # Avanza a 'EliminarUnico'
        self.advance()  # Avanza al '('
        self.advance()
        # print(self.current_token().value)
        # Capturar el criterio JSON
        if self.current_token().type != 'STRING':
            self.error("Expected JSON document as string for deletion criteria")
            return
        coleccion_variable = self.current_token().value
        
        self.advance()  # Avanza al documento JSON
        if self.current_token().value != ',':
            self.error("Expected ',' after collection name")
            return

        self.advance()  # Avanza al ')'
        if self.current_token().type != 'STRING':
            self.error("Expected JSON document as string")
            return
        criterio = self.current_token().value
        self.advance()  # Avanza al ';'
        self.advance()  # Avanza al ';'
        # print(self.current_token().value)
        # Añadir el nodo al AST
        self.ast.nodes.append(NodoEliminarUnico(coleccion_variable, criterio))


    def parse_buscar_todo(self):
        # print(self.current_token().type)
        self.advance()  # Avanza al token 'BUSCARTODO'
        # print(self.current_token().type)
        if self.current_token().type != 'IDENTIFIER':
            self.error("Expected identifier after 'BuscarTodo'")
            return
        # print(self.current_token().value)
        coleccion_variable = self.current_token().value
        self.advance()  # Avanza al '='
        self.advance()  # Avanza al 'nueva'
        self.advance()  # Avanza a 'BuscarTodo'
        self.advance()  # Avanza al '('
        self.advance()
        # print(self.current_token().value)
        if self.current_token().type != 'STRING':
            self.error("Expected string for collection name")
            return

        nombre_coleccion = self.current_token().value
        self.advance()  # Avanza al nombre de la colección en STRING

        self.advance()  # Avanza al ')'
        # self.advance()  # Avanza al ';'
        # print(self.current_token().value)
        # Añadir el nodo al AST
        self.ast.nodes.append(NodoBuscarTodo(nombre_coleccion))


    def parse_buscar_unico(self):
        # print(self.current_token().type)
        self.advance()  # Avanza al token 'BUSCARTODO'
        # print(self.current_token().type)
        if self.current_token().type != 'IDENTIFIER':
            self.error("Expected identifier after 'BuscarTodo'")
            return
        # print(self.current_token().value)
        coleccion_variable = self.current_token().value
        self.advance()  # Avanza al '='
        self.advance()  # Avanza al 'nueva'
        self.advance()  # Avanza a 'BuscarTodo'
        self.advance()  # Avanza al '('
        self.advance()
        # print(self.current_token().value)
        if self.current_token().type != 'STRING':
            self.error("Expected string for collection name")
            return

        nombre_coleccion = self.current_token().value
        self.advance()  # Avanza al nombre de la colección en STRING

        self.advance()  # Avanza al ')'
        # self.advance()  # Avanza al ';'
        # print(self.current_token().value)
        self.ast.nodes.append(NodoBuscarUnico(nombre_coleccion))
        # type: ignore # self.advance()  # Pasar el símbolo ';'

