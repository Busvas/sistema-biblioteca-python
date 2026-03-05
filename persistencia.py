import json                                                    # REQUISITO TÉCNICO: Serialización de datos

def guardar_datos(biblioteca, usuarios_db):                    # Función: Graba el estado actual en disco
    try:                                                       # REQUISITO TÉCNICO: Manejo de excepciones
        datos_totales = {
            "libros": biblioteca,
            "usuarios": usuarios_db
        }
        with open("biblioteca_data.json", "w") as archivo:      # Abre el archivo en modo escritura ('w')
            json.dump(datos_totales, archivo, indent=4)        # Transforma diccionarios a texto legible
        return True
    except IOError as e:                                       # Excepción: Error de entrada/salida (disco lleno, permisos)
        print(f"❌ Error físico al guardar: {e}")
        return False

def cargar_datos():                                            # Función: Recupera datos al iniciar
    try:                                                       # REQUISITO TÉCNICO: Manejo de excepciones
        with open("biblioteca_data.json", "r") as archivo:      # Intenta abrir el archivo en modo lectura ('r')
            datos = json.load(archivo)                         # Deserializa el texto JSON a diccionarios
            return datos["libros"], datos["usuarios"]
    except FileNotFoundError:                                  # EXCEPCIÓN ESPECÍFICA: El archivo no existe aún
        print("⚠ Advertencia: Archivo no encontrado. Se iniciará una base de datos limpia.")
        return {}, {}                                          # Retorna diccionarios vacíos para no romper el programa
    except json.JSONDecodeError:                               # EXCEPCIÓN ESPECÍFICA: El archivo está corrupto
        print("❌ Error: El archivo JSON tiene un formato inválido.")
        return {}, {}
    