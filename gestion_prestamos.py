import datetime                                                # REQUISITO TÉCNICO: Manejo de tiempos y fechas

class Prestamo:                                                # REQUISITO TÉCNICO: Define la transacción
    def __init__(self, isbn, titulo, fecha_prestamo):          # Constructor de la transacción
        self.isbn = isbn                                       # Atributo: Identificador del libro
        self.titulo = titulo                                   # Atributo: Nombre de la obra para el ticket
        self.fecha_prestamo = str(fecha_prestamo)              # Atributo: Día que salió de la biblioteca
        # Calcula automáticamente la fecha de entrega (7 días después)
        self.fecha_limite = str(fecha_prestamo + datetime.timedelta(days=7)) 

    def to_dict(self):                                         # Método: Convierte el ticket a diccionario
        return self.__dict__                                   # Estructura lista para guardar en el perfil del usuario

def registrar_prestamo(biblioteca, usuarios_db, isbn, id_u):   # Función: Conecta Libro con Usuario
    # VALIDACIONES DE SEGURIDAD (Reglas de Negocio)
    if isbn not in biblioteca or id_u not in usuarios_db:
        return "❌ Error: Datos de libro o usuario no registrados."
    
    libro = biblioteca[isbn]                                   # Acceso al diccionario del libro
    usuario = usuarios_db[id_u]                                # Acceso al diccionario del usuario
    
    if libro["disponibles"] <= 0: return "❌ Sin stock físico."
    if len(usuario["libros_prestados"]) >= 3: return "❌ Límite de 3 libros alcanzado."
    if usuario["multas"] > 0: return "❌ Usuario con multas pendientes ($)."

    # EJECUCIÓN DEL PRÉSTAMO
    libro["disponibles"] -= 1                                  # Actualiza stock en tiempo real
    libro["prestamos_totales"] += 1                            # Suma al reporte de popularidad
    
    # Crea el objeto Prestamo (POO)
    nuevo_ticket = Prestamo(isbn, libro["titulo"], datetime.date.today())
    usuario["libros_prestados"].append(nuevo_ticket.to_dict()) # Guarda el préstamo en la lista del usuario
    
    return nuevo_ticket.to_dict()                              # Retorna los datos para el ticket impreso

def registrar_devolucion(biblioteca, usuarios_db, id_u, isbn): # Función: Retorno y cálculo de multas
    usuario = usuarios_db[id_u]                                # Localiza al socio
    
    for p in usuario["libros_prestados"]:                      # Busca el libro en la lista de pendientes
        if p["isbn"] == isbn:
            # LÓGICA DE MULTAS ($1 por día)
            limite = datetime.datetime.strptime(p["fecha_limite"], "%Y-%m-%d").date()
            hoy = datetime.date.today()
            
            if hoy > limite:                                   # Si se pasó de la fecha...
                dias = (hoy - limite).days                     # Resta de fechas para obtener días
                multa = dias * 1.0                             # REQUISITO: $1 de multa diaria
                usuario["multas"] += multa                     # Suma la deuda al perfil
                print(f"⚠️ ¡RETRASO! Generada multa de: ${multa:.2f}")

            # ACTUALIZACIÓN FINAL
            biblioteca[isbn]["disponibles"] += 1               # El libro regresa al estante físico
            usuario["libros_prestados"].remove(p)              # Se quita de la lista de pendientes
            return True                                        # Operación exitosa
            
    return False                                               # El usuario no tenía ese ISBN prestado
