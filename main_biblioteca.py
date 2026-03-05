import gestion_libros as gl                                       # Capa de Negocio: Maneja la lógica de objetos Libro
import gestion_usuarios as gu                                     # Capa de Negocio: Maneja la lógica de objetos Usuario
import gestion_prestamos as gp                                    # Capa de Transacciones: Cruza libros con usuarios
import persistencia as per                                        # Capa de Datos: Serialización y escritura en JSON
import reportes as rep                                            # Capa de Análisis: Filtros y ordenamiento de datos

# Inicialización del sistema mediante Deserialización
# per.cargar_datos() intenta leer el JSON; si no existe, devuelve dicts vacíos {}
biblioteca, usuarios = per.cargar_datos()                         # Recupera el estado previo de la memoria

def agregar_libro():                                              # Interfaz de entrada para nuevos registros
    try:                                                          # Manejo de excepciones para entradas de usuario
        isbn = input("Ingrese ISBN: ")                            # Captura la llave primaria del libro
        titulo = input("Título: ")                                # Captura atributo descriptivo
        autor = input("Autor: ")                                  # Captura atributo de autoría
        cat = input("Categoría: ")                                # Captura atributo de clasificación
        cant = int(input("Cantidad total: "))                     # Casting a entero para cálculos aritméticos
        
        # Invocamos la clase Libro del módulo gl y guardamos el dict resultante
        biblioteca[isbn] = gl.crear_libro(isbn, titulo, autor, cat, cant) 
        per.guardar_datos(biblioteca, usuarios)                   # Sincronización inmediata con el archivo físico
        print("✔ Libro registrado con éxito.")
    except ValueError:                                            # Captura error si el usuario no ingresa números
        print("❌ Error: La cantidad debe ser un número entero.")

def gestionar_usuarios():                                         # Controlador del submenú de socios
    print("\na. Registrar\nb. Buscar\nc. Eliminar")
    op_u = input("Seleccione: ")
    if op_u == "a":
        id_u = input("ID/Cédula: ")                               # Llave primaria del usuario
        nom = input("Nombre: ")                                   # Atributo nominal
        tel = input("Teléfono: "); dir_u = input("Dirección: ")   # Atributos de contacto
        gu.registrar_usuario(usuarios, id_u, nom, tel, dir_u)     # Llama a la lógica de instanciación en gu
        per.guardar_datos(biblioteca, usuarios)                   # Actualiza persistencia tras el registro
    elif op_u == "b":
        crit = input("Nombre o ID: ")                             # Criterio de búsqueda flexible
        # Imprime la lista de tuplas devuelta por el motor de búsqueda
        print(gu.buscar_usuario(usuarios, crit)) 
    elif op_u == "c":
        id_u = input("ID a eliminar: ")                           # Llave para borrado lógico
        # gu.eliminar_usuario valida que no existan deudas antes de borrar
        res = gu.eliminar_usuario(usuarios, id_u)
        if res == True: 
            per.guardar_datos(biblioteca, usuarios)               # Refleja el borrado en el JSON
            print("✔ Usuario eliminado.")
        else: print(f"❌ No se pudo eliminar: {res}")

def realizar_prestamo():                                          # Controlador de salida de mercancía
    entrada = input("Ingrese ISBN o nombre del libro: ")          # Búsqueda por múltiples atributos
    coincidencias = gl.buscar_libro(biblioteca, entrada)          # Llama al filtro del módulo libros
    
    if coincidencias:                                             # Validación de existencia del recurso
        isbn_real = coincidencias[0][0]                           # Normalización: toma el ISBN real del primer hallazgo
        id_usu = input("ID del estudiante: ")                     # Validador de identidad del socio
        
        # Llama a la lógica de negocio que resta stock y verifica multas/límites
        ticket = gp.registrar_prestamo(biblioteca, usuarios, isbn_real, id_usu)
        
        if isinstance(ticket, dict):                              # Verifica si la operación fue exitosa (devolvió dict)
            per.guardar_datos(biblioteca, usuarios)               # Persiste la reducción de stock y el nuevo préstamo
            print(f"✔ Préstamo de '{ticket['titulo']}' registrado.")
            print(f"Entregar el: {ticket['fecha_limite']}")       # Muestra fecha calculada por timedelta
        else:
            print(f"{ticket}")                                    # Imprime el mensaje de error personalizado de gp
    else:
        print("❌ Error: Libro no encontrado en la base de datos.")

def devolver_libro():                                             # Controlador de retorno y cálculo de mora
    id_u = input("ID del estudiante: ")                           # Identifica al deudor
    isbn = input("ISBN del libro a devolver: ")                   # Identifica el recurso a liberar
    # registrar_devolucion calcula días de retraso y aplica multas de $1
    exito = gp.registrar_devolucion(biblioteca, usuarios, id_u, isbn)
    if exito:
        per.guardar_datos(biblioteca, usuarios)                   # Persiste el aumento de stock y el saldo de multas
        print("✔ Devolución procesada correctamente.")
    else:
        print("❌ Error: El registro de préstamo no existe.")

def menu():                                                       # Bucle principal de ejecución (CLI)
    while True:                                                   # Mantiene el programa activo hasta que el usuario decida salir
        print("\n--- SISTEMA BIBLIOTECARIO INTEGRADOR ---")       # Encabezado del sistema
        print("1. Libros (Agregar/Listar)\n2. Usuarios (Gestión)")
        print("3. Préstamos\n4. Devoluciones")
        print("5. Reportes (Populares/Multas)\n6. Salir")
        op = input("Seleccione: ")                                # Captura la decisión del usuario
        
        if op == "1": agregar_libro()                             # Rama para inventario
        elif op == "2": gestionar_usuarios()                      # Rama para socios
        elif op == "3": realizar_prestamo()                      # Rama para transacciones de salida
        elif op == "4": devolver_libro()                         # Rama para transacciones de entrada
        elif op == "5":                                           # Rama para análisis de datos
            rep.libros_mas_populares(biblioteca)                  # Muestra Top 5 usando sorted() y lambda
            rep.usuarios_con_multas(usuarios)                     # Filtra usuarios con atributo multa > 0
        elif op == "6":                                           # Cierre preventivo
            per.guardar_datos(biblioteca, usuarios)               # Último resguardo de información antes de cerrar
            print("Saliendo del sistema...")
            break                                                 # Rompe el bucle While y termina la ejecución
        