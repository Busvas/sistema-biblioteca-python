# 📚 Sistema de Gestión Bibliotecaria Pro
**Autor:** RONNY FABRICIO TOCTAQUIZA PIEDRA  
**Curso:** Fundamentos de Python - Proyecto Final

## 📝 Descripción General
Este es un sistema integral desarrollado en **Python** para la administración de una biblioteca. El programa permite gestionar un catálogo de libros, registrar socios y controlar el ciclo de préstamos y devoluciones con un sistema automático de cálculo de multas.

### Características Principales:
* **Modularidad:** Código organizado en módulos independientes para facilitar el mantenimiento.
* **POO:** Uso de Clases y Objetos para representar Libros, Usuarios y Préstamos.
* **Persistencia:** Almacenamiento de datos en formato JSON para que la información perdure.
* **Lógica Financiera:** Cálculo automático de sanciones por entregas tardías.

---

## 🚀 Instalación y Ejecución

### Requisitos previos:
* Tener instalado **Python 3.8** o superior.
* No requiere librerías externas (usa módulos estándar de Python).

### Instrucciones:
1.  Descarga o clona los archivos `.py` en una carpeta local.
2.  Abre una terminal o consola de comandos en esa carpeta.
3.  Ejecuta el programa principal con el siguiente comando:
    ```bash
    python main_biblioteca.py
    ```

---

## 📖 Ejemplos de Uso

### 1. Registro de Libros
Al iniciar, puedes ir al menú de "Gestión de Libros" y registrar un nuevo ejemplar ingresando ISBN, título, autor y cantidad. El sistema asignará automáticamente la disponibilidad inicial.

### 2. Realizar un Préstamo
Selecciona un socio y un libro. El sistema verificará:
* Que el libro tenga stock.
* Que el usuario no tenga más de 3 libros.
* Que el usuario no tenga multas pendientes.

### 3. Devolución y Multas
Al devolver un libro fuera de la fecha límite (7 días), el sistema mostrará un mensaje: 
> *“Entrega fuera de tiempo. Multa generada: $X.0”*

---

## 📊 Arquitectura del Sistema 

## Diagrama de Clases
El sistema se basa en tres entidades principales interconectadas:

* **Clase Libro:** (Atributos: isbn, titulo, autor, categoria, cantidad, disponibles).
* **Clase Usuario:** (Atributos: id_usuario, nombre, libros_prestados, multas).
* **Clase Prestamo:** (Atributos: objeto_libro, objeto_usuario, fecha_prestamo, fecha_limite).

> **Lógica de Relación:** Un *Préstamo* vincula un *Libro* con un *Usuario*, afectando el stock del primero y el historial del segundo.

### Diagrama de Flujo Lógico
El programa sigue este flujo de ejecución:
1. **Inicio:** Carga datos desde `biblioteca_data.json`.
2. **Interacción:** El `main` gestiona el menú y las entradas del usuario.
3. **Procesamiento:** Los módulos `gestion_libros`, `usuarios` y `prestamos` ejecutan la lógica.
4. **Cierre:** Los datos se guardan automáticamente para la siguiente sesión.
