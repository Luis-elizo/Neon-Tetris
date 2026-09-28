# Registro de Cambios (Changelog) - Neon Tetris

Todos los cambios notables de este proyecto están documentados en este archivo, siguiendo el formato estándar de versionado semántico y las buenas prácticas de desarrollo de software para el curso **EIF207 Estructuras de Datos**.

---

## [1.0.0] - 2026-09-27 (Versión Final de Entrega)

### Añadido
- **Persistencia JSON (`estructuras/ManejadorJSON`):** Serializador y deserializador manual para el archivo `scores.json` sin utilizar librerías externas ni contenedores STL.
- **Algoritmos de Ordenamiento (`logica/ordenamientos`):** Implementaciones manuales de Bubble Sort y Merge Sort.
- **Pantalla de Ranking (`ui/rankingScreen`):** Visualización de la tabla de mejores registros con benchmark interactivo y medición de tiempo en nanosegundos y microsegundos con `std::chrono`.
- **Efectos y Controles Visuales:**
  - Animación de destello blanco/rosa intermitente durante 250 ms al limpiar líneas en `gameScreen`.
  - Botones interactivos en pantalla con soporte de ratón y teclado para el modo Replay (`<- ATRAS`, `> REPRODUCIR / || PAUSA`, `ADELANTE ->`, `SALIR`).
- **Documentación Completa:**
  - `README.md` con manual de usuario, mapeo de estructuras, guía de descarga de Raylib 4.0 y ejecución en ZinjaI con tecla F9.
  - Informe técnico formal en formato Word (`INFORME_PROYECTO1_Luis_Andrés_Elizondo_Hernández.docx`) y versión exportada a PDF de 6 páginas exactas (`INFORME_PROYECTO1_Luis_Andrés_Elizondo_Hernández.pdf`) con portada vertical institucional UNA, tablas y curvas de rendimiento.

### Modificado
- **Refactorización de Código:** Sustitución de variables de una sola letra y abreviaturas por nombres semánticos descriptivos (`indiceFila`, `indiceColumna`, `posicion`, `colorBloque`, etc.).
- **Comentarios del Código:** Reemplazo de explicaciones teóricas complejas por anotaciones concisas y directas estilo apuntes de estudiante en todos los archivos `.h` y `.cpp`.
- **Configuración de ZinjaI (`NeonTetris.zpr`):** Inclusión de rutas y librerías tanto para el modo `Debug` como para `Release`.

---

## [0.6.0] - 2026-09-24

### Añadido
- **Cola de Prioridad (`estructuras/ColaPrioridad`):** Implementación de cola con prioridad ordenada por tiempo de ejecución para detonar eventos dinámicos (*Fiebre de Velocidad*, *Terremoto / Línea de Basura* y *Bonus de Puntaje*).
- **Mecánica de Deshacer (Undo / Rewind):** Integración de la tecla `Z` para retroceder turnos en la partida restaurando el tablero desde `ListaDoble`.

---

## [0.5.0] - 2026-09-23

### Añadido
- **Modo Replay y Grabación de Snapshots:** Conexión de `ListaDoble` en `main.cpp` para capturar el estado completo del tablero y puntaje al fijar cada pieza.
- **Visualizador de Repetición:** Función `DrawReplay` en `gameScreen` para navegar fotogramas históricos tras la derrota.

---

## [0.4.0] - 2026-09-22

### Añadido
- **Lista Doblemente Enlazada (`estructuras/ListaDoble`):** Nodos con punteros `anterior` y `siguiente` que almacenan una matriz de 20x10 celdas y el puntaje acumulado.

---

## [0.3.0] - 2026-09-21

### Añadido
- **Mecánica de Hold (Casilla de Espera):** Intercambio de la pieza activa mediante la tecla `Shift Derecho` utilizando la estructura `Pila` (LIFO) con límite de un intercambio por turno.

---

## [0.2.5] - 2026-09-20

### Añadido
- **Estructura Pila (`estructuras/Pila`):** Pila básica con nodos propios para almacenar tipos de pieza.
- **Bolsa de 7 Piezas (7-bag System):** Barajado aleatorio con algoritmo de Fisher-Yates manual.
- **Previsualización de Siguientes:** Método `obtenerEn()` en la clase `Cola` para pintar las 3 próximas piezas en pantalla.

---

## [0.2.0] - 2026-09-17

### Añadido
- **Estructura Cola (`estructuras/Cola`):** Cola FIFO dinámica basada en nodos enlazados propios.
- **Limpieza de Líneas y Sistema de Puntaje:** Detección de filas llenas en el tablero, reconexión de filas vacías en la parte superior y otorgamiento de puntos según líneas simultáneas (100, 300, 500, 800).

---

## [0.1.5] - 2026-09-16

### Añadido
- **Estructura Tablero (`estructuras/Tablero`):** Lista enlazada de 20 nodos de fila, cada uno con 10 nodos de celda (matriz ortogonal dinámica).
- **Físicas y Reglas del Juego:** Gravedad paso a paso, colisiones contra bordes y piezas fijas, y movimiento horizontal.

---

## [0.1.0] - 2026-09-03

### Añadido
- **Estructura del Proyecto:** Separación de código en carpetas modulares (`estructuras/`, `logica/`, `ui/`).
- **Clase Pieza (`logica/Pieza`):** Definición de las 7 piezas clásicas con sus 4 rotaciones precalculadas.
- **Máquina de Estados y Pantallas Base:** Interfaces para `MenuScreen`, `PauseScreen` y `GameOverScreen`.

---

## [0.0.1] - 2026-08-20

### Añadido
- **Inicio del Repositorio:** Configuración inicial del control de versiones con Git.
- **Integración con Raylib:** Creación de la ventana básica de 1000x900 px a 60 FPS y validación del entorno de compilación MinGW.
