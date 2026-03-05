class Libro:                                                      # REQUISITO TÉCNICO: Definición de Clase
    def __init__(self, isbn, titulo, autor, categoria, cantidad): # Constructor para inicializar el objeto
        self.isbn = isbn                                          # Identificador único
        self.titulo = titulo                                      # Nombre de la obra
        self.autor = autor                                        # Escritor responsable
        self.categoria = categoria                                # Género o área (Requisito funcional)
        self.cantidad = cantidad                                  # Stock total ingresado
        self.disponibles = cantidad                               # Unidades libres para préstamo
        self.prestamos_totales = 0                                # Contador para reporte de popularidad

    def to_dict(self):                                            # Convierte el objeto a diccionario para JSON
        return self.__dict__                                      # Facilita el guardado en archivos

def crear_libro(isbn, titulo, autor, categoria, cantidad):        # Mantiene la interfaz que ya usas en el main
    nuevo_libro = Libro(isbn, titulo, autor, categoria, cantidad) # Instancia un nuevo objeto de la clase Libro
    return nuevo_libro.to_dict()                                  # Retorna el diccionario listo para la base de datos

def buscar_libro(biblioteca, criterio):                          # Busca libros por ISBN o por Título
    encontrados = []                                              # Lista temporal para guardar coincidencias
    for isbn, datos in biblioteca.items():                        # Recorre toda la base de datos (diccionario)
        # Compara el criterio con el título o el ISBN directamente
        if criterio.lower() in datos["titulo"].lower() or criterio == isbn: 
            encontrados.append((isbn, datos))                     # Agrega el libro hallado a la lista
    return encontrados                                            # Devuelve todos los resultados hallados

def eliminar_libro(biblioteca, isbn):                             # Elimina un libro del sistema definitivamente
    if isbn in biblioteca:                                        # Verifica si el ISBN existe en el diccionario
        # Requisito lógico: Solo borra si no hay préstamos activos
        if biblioteca[isbn]["disponibles"] == biblioteca[isbn]["cantidad"]: 
            del biblioteca[isbn]                                  # Elimina la entrada del diccionario global
            return True                                           # Confirma que el borrado fue exitoso
        else:
            return "prestado"                                     # Error: Hay libros en manos de usuarios
    return False                                                  # Error: El ISBN no existe

def listar_libros(biblioteca):                                    # Genera la lista completa del inventario
    print("\n" + "="*70)                                          # Estética de reporte
    print(f"{'ISBN':<10} | {'TITULO':<25} | {'CATEGORIA':<15} | {'STOCK'}")
    print("-" * 70)
    for isbn, d in biblioteca.items():                            # Recorre el diccionario para mostrar los datos
        print(f"{isbn:<10} | {d['titulo'][:25]:<25} | {d['categoria']:<15} | {d['disponibles']}/{d['cantidad']}")
    print("="*70 + "\n")
    