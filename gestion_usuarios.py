class Usuario:                                                    # REQUISITO TÉCNICO: Define el molde para cada socio
    def __init__(self, id_usuario, nombre, tel, direccion):       # Constructor: Inicializa los atributos del objeto
        self.id_usuario = id_usuario                              # Atributo: Identificador único (Cédula/Matrícula)
        self.nombre = nombre                                      # Atributo: Nombre completo del usuario
        self.tel = tel                                            # Atributo: Número de teléfono/celular
        self.direccion = direccion                                # Atributo: Domicilio del usuario
        self.multas = 0.0                                         # Atributo: Saldo deudor acumulado (inicia en 0)
        self.libros_prestados = []                                # Atributo: Lista de diccionarios con libros activos

    def to_dict(self):                                            # Método: Convierte el objeto a diccionario
        return self.__dict__                                      # Facilita la persistencia en el archivo JSON

def registrar_usuario(usuarios_db, id_u, nom, tel, dir_u):        # Función: Crea y guarda un nuevo usuario
    nuevo = Usuario(id_u, nom, tel, dir_u)                        # Instancia (crea) el objeto de la clase Usuario
    usuarios_db[id_u] = nuevo.to_dict()                           # Almacena el diccionario en la base de datos global
    return True                                                   # Retorna confirmación de éxito

def buscar_usuario(usuarios_db, criterio):                        # Función: Filtra usuarios por nombre o ID
    encontrados = []                                              # Lista temporal de resultados (Requisito: Listas)
    for id_u, datos in usuarios_db.items():                       # Itera sobre el diccionario (Requisito: Diccionarios)
        if criterio.lower() in datos["nombre"].lower() or criterio == id_u:
            encontrados.append((id_u, datos))                     # Agrega tupla con (ID, Datos) si hay coincidencia
    return encontrados                                            # Retorna la lista de objetos hallados

def modificar_usuario(usuarios_db, id_usuario, campo, nuevo_valor): # Función: Actualiza información específica
    if id_usuario in usuarios_db:                                 # Validación: Verifica si el usuario existe
        usuarios_db[id_usuario][campo] = nuevo_valor              # Acceso directo por llave para modificar el valor
        return True                                               # Confirmación de cambio realizado
    return False                                                  # Error: Usuario no encontrado

def eliminar_usuario(usuarios_db, id_usuario):                    # Función: Borra un registro del sistema
    if id_usuario in usuarios_db:                                 # Validación de existencia
        # REGLA DE NEGOCIO: No eliminar si debe libros o dinero
        if len(usuarios_db[id_usuario]["libros_prestados"]) == 0 and usuarios_db[id_usuario]["multas"] == 0:
            del usuarios_db[id_usuario]                           # Elimina la llave y su valor de la memoria
            return True                                           # Confirmación de borrado
        return "deuda"                                            # Error: Tiene pendientes con la biblioteca
    return False                                                  # Error: Usuario no localizado
