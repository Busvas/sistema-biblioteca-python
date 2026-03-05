def libros_mas_populares(biblioteca):                          # Reporte: Basado en número de préstamos
    print("\n" + "★"*10 + " TOP 5 LIBROS MÁS POPULARES " + "★"*10)
    # REQUISITO TÉCNICO: Uso de listas y ordenamiento avanzado
    # Convertimos los valores del diccionario en una lista y ordenamos por 'prestamos_totales'
    populares = sorted(biblioteca.values(), key=lambda x: x["prestamos_totales"], reverse=True)
    
    for i, libro in enumerate(populares[:5]):                  # Muestra solo los primeros 5
        print(f"{i+1}. {libro['titulo']} ({libro['prestamos_totales']} préstamos)")

def usuarios_con_multas(usuarios_db):                          # Reporte: Control de morosidad
    print("\n" + "!"*10 + " USUARIOS CON DEUDAS PENDIENTES " + "!"*10)
    hay_morosos = False
    for id_u, datos in usuarios_db.items():                    # Recorre el diccionario de usuarios
        if datos["multas"] > 0:                                # Filtra solo los que deben dinero
            print(f"ID: {id_u} | Nombre: {datos['nombre']} | Deuda: ${datos['multas']:.2f}")
            hay_morosos = True
    if not hay_morosos: print("✅ No existen usuarios con multas pendientes.")

def libros_prestados_actualmente(usuarios_db):                 # Reporte: Inventario fuera de estantería
    print("\n--- LIBROS ACTUALMENTE EN PRÉSTAMO ---")
    total = 0
    for id_u, datos in usuarios_db.items():
        for p in datos["libros_prestados"]:                    # Anidación de bucles para llegar a la lista
            print(f"- {p['titulo']} (Poseedor: {datos['nombre']} | Vence: {p['fecha_limite']})")
            total += 1
    print(f"Total de libros fuera: {total}")
    