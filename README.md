# Neon Tetris - Proyecto I (EIF207 Estructuras de Datos)

**Universidad Nacional de Costa Rica (UNA)**  
**Sede Regional Brunca - Campus Coto / Pérez Zeledón**  
**Escuela de Informática**  
**Curso:** EIF207 Estructuras de Datos  
**Ponderación:** 15% de la nota final  

---

## 1. Descripción General

**Neon Tetris** es una implementación completa y personalizada del clásico juego Tetris bajo una estética visual *Cyberpunk / Neón*, desarrollada en **C++** utilizando la biblioteca gráfica **Raylib** y el entorno **ZinjaI**.

El proyecto resuelve cada mecánica de juego utilizando de forma estricta estructuras de datos lineales implementadas manualmente mediante punteros y memoria dinámica. **No se utiliza ningún contenedor de la biblioteca estándar (STL)** como `std::vector`, `std::queue`, `std::stack`, `std::list`, `std::priority_queue` ni algoritmos como `std::sort`.

---

## 2. Mapeo de Estructuras de Datos a Mecánicas de Juego

| Mecánica | Estructura de Datos | Implementación Propia | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **Tablero de Juego** | Lista enlazada de listas enlazadas | [`estructuras/Tablero.h`](estructuras/Tablero.h) | 20 nodos de fila, cada uno con 10 nodos de celda. Permite eliminar filas llenas y reconectar nuevas filas vacías en la cabeza sin desplazar bloques de memoria fija. |
| **Piezas Siguientes** | Cola FIFO (First-In, First-Out) | [`estructuras/Cola.h`](estructuras/Cola.h) | Secuencia generada mediante "Bolsa de 7" con barajado Fisher-Yates manual. Muestra en pantalla las 3 próximas piezas en espera. |
| **Casilla de Espera (Hold)** | Pila LIFO (Capacidad 1) | [`estructuras/Pila.h`](estructuras/Pila.h) | Pila con tope restringido a 1 elemento para almacenar e intercambiar la pieza activa mediante la tecla `Shift Derecho`. |
| **Historial y Modo Replay** | Lista Doblemente Enlazada | [`estructuras/ListaDoble.h`](estructuras/ListaDoble.h) | Nodos con punteros `anterior` y `siguiente` que capturan el estado completo del tablero y puntaje. Permite **Deshacer (`Z`)** y **Rehacer (`Y`)** multi-paso en partida, y reproducción paso a paso o automática tras Game Over. |
| **Eventos Programados** | Cola de Prioridad | [`estructuras/ColaPrioridad.h`](estructuras/ColaPrioridad.h) | Ordenada ascendentemente por tiempo de ejecución ($O(n)$ al insertar, $O(1)$ al extraer el frente). Dispara eventos de *Fiebre de Velocidad*, *Terremoto (Línea de basura)* y *Bonus de Puntaje*. |
| **Tabla de Clasificación** | Arreglo de Registros + Algoritmos de Ordenamiento | [`logica/ordenamientos.h`](logica/ordenamientos.h), [`estructuras/ManejadorJSON.h`](estructuras/ManejadorJSON.h) | Persistencia manual en archivo JSON (`scores.json`). Permite alternar interactivamente entre **Bubble Sort** $O(n^2)$ y **Merge Sort** $O(n \log n)$ midiendo tiempos reales con `std::chrono`. |

---

## 3. Biblioteca Gráfica y Elementos Visuales

- **Librería Gráfica:** [Raylib](https://www.raylib.com/) (versión compatible con MinGW/GCC).
- **Resolución:** Ventana de $1000 \times 900$ píxeles a $60\text{ FPS}$ estables.
- **Paleta Neón:** Colores Cyan, Rosa Neón, Morado Eléctrico y Amarillo Neón definidos en [`ui/colors.h`](ui/colors.h).
- **Animaciones:** Destello intermitente (blanco/rosa) durante 250 ms al completarse una o más líneas antes de su eliminación física.
- **Controles Visuales de Replay:** Botones interactivos en pantalla (`<- ATRAS`, `> REPRODUCIR / || PAUSA`, `ADELANTE ->`, `SALIR`) con soporte para clic de ratón y atajos de teclado.

---

## 4. Controles del Juego

### Durante la Partida
| Tecla | Acción |
| :--- | :--- |
| `<-` / `->` | Mover la pieza a la izquierda / derecha |
| `Flecha Arriba` | Rotar la pieza (4 orientaciones fijas, sin wall-kick) |
| `Flecha Abajo` | Caída acelerada (Soft Drop) |
| `Shift Derecho` | Enviar a / intercambiar con la casilla de espera (**Hold**) |
| `Z` | **Deshacer** movimiento (retrocede en el historial) |
| `Y` | **Rehacer** movimiento (avanza en el historial) |
| `Escape` | Pausar la partida |

### En la Pantalla de Replay (Fin de Partida)
| Control | Acción |
| :--- | :--- |
| `<-` o Botón `<- ATRAS` | Retroceder un paso en la repetición |
| `->` o Botón `ADELANTE ->` | Avanzar un paso en la repetición |
| `Espacio` o Botón `> REPRODUCIR` | Iniciar / pausar la reproducción automática (cada 0.5s) |
| `M` o Botón `SALIR` | Salir al Menú Principal |

### En la Pantalla de Ranking
- Clic en **Bubble Sort $O(n^2)$** o **Merge Sort $O(n \log n)$** para ordenar en vivo y observar la medición en nanosegundos / microsegundos.
- Clic en **VOLVER** para regresar al Menú Principal.

---

## 5. Preparación del Entorno, Instalación y Ejecución

Para ejecutar el proyecto en **ZinjaI**, el único requisito previo es contar con **Raylib** instalado en la ruta estándar de Windows.

### 5.1. Descarga de Herramientas y Versión Correcta

1. **Entorno ZinjaI:**
   - Descargar la versión estándar de **ZinjaI para Windows** con compilador MinGW/GCC integrado desde su sitio oficial ([zinjai.sourceforge.net](http://zinjai.sourceforge.net/)).
2. **Biblioteca Raylib:**
   - **Versión Recomendada:** **Raylib 4.0** (o 4.2 / 4.x con soporte para MinGW 32-bit `i686-w64-mingw32`).
   - **Enlace de Descarga Oficial:** Disponible en [raylib.com](https://www.raylib.com/) o directamente en los [Releases de GitHub de Raylib](https://github.com/raysan5/raylib/releases/tag/4.0.0).
   - **Paquete sugerido:** `raylib_installer_v4.0.0.exe` (instalador automático de Windows) o el archivo comprimido `raylib-4.0.0_win32_mingw.zip`.
   - **Ruta de Instalación Obligatoria:** Instalar o extraer en **`C:\raylib`** (la ruta por defecto del instalador). De esta manera, ZinjaI encontrará los encabezados y librerías de forma automática sin necesidad de configurar nada manualmente.

---

### 5.2. ¿Con solo descargar Raylib se puede abrir y correr el proyecto?

**Sí.** Si instalaste Raylib en su ruta estándar `C:\raylib`, los pasos son directos:

1. Abre **ZinjaI**.
2. Ve al menú superior: **Archivo -> Abrir Proyecto...**
3. Selecciona el archivo [`NeonTetris.zpr`](NeonTetris.zpr) en la carpeta raíz del proyecto.
4. Presiona la tecla **F9** (o haz clic en el botón verde con el engranaje/flecha de *Ejecutar*).
5. ZinjaI compilará todos los archivos fuente (`estructuras/`, `logica/`, `ui/` y `main.cpp`) y lanzará la ventana de **Neon Tetris** a 60 FPS.

*Nota:* El archivo de proyecto [`NeonTetris.zpr`](NeonTetris.zpr) ya incluye preconfiguradas las opciones para `Debug` y `Release`:
- **Cabeceras (Include):** `C:\raylib\w64devkit\i686-w64-mingw32\include`
- **Bibliotecas (Lib):** `C:\raylib\w64devkit\i686-w64-mingw32\lib`
- **Banderas de Vinculación (Linker):** `raylib opengl32 gdi32 winmm`

---

### 5.3. ¿Qué hacer si Raylib está instalado en otra carpeta? (Ajuste rápido)

Si tu instalación de Raylib se encuentra en otro disco o ruta (por ejemplo, `D:\raylib` o `C:\Users\...\raylib`), solo debes actualizar las rutas dentro de ZinjaI:

1. En ZinjaI, con el proyecto abierto, ve a: **Proyecto -> Opciones del proyecto...**
2. Dirígete a la pestaña **Rutas**:
   - En **Directorios de Cabeceras (Include)**, cambia la ruta a tu carpeta `include` de Raylib (o la carpeta `src` de Raylib donde esté `raylib.h`).
   - En **Directorios de Bibliotecas (Lib)**, cambia la ruta a tu carpeta `lib` de Raylib (o la carpeta `src` donde esté `libraylib.a`).
3. En la pestaña **Vinculación**, verifica que en *Otras bibliotecas para el enlazador* figuren:
   ```text
   raylib opengl32 gdi32 winmm
   ```
4. Haz clic en **Aceptar** y presiona **F9**.

---

### 5.4. Opción Alternativa: Compilación Manual por Terminal (MinGW / GCC)

Si prefieres compilar sin abrir ZinjaI directamente desde PowerShell o CMD con MinGW:

```bash
g++ -std=c++14 -O2 -o NeonTetris.exe \
    main.cpp \
    estructuras/Tablero.cpp \
    estructuras/Cola.cpp \
    estructuras/Pila.cpp \
    estructuras/ListaDoble.cpp \
    estructuras/ColaPrioridad.cpp \
    estructuras/ManejadorJSON.cpp \
    logica/Pieza.cpp \
    logica/ordenamientos.cpp \
    ui/gameScreen.cpp \
    ui/menuScreen.cpp \
    ui/pauseScreen.cpp \
    ui/gameOverScreen.cpp \
    ui/rankingScreen.cpp \
    -IC:/raylib/w64devkit/i686-w64-mingw32/include \
    -LC:/raylib/w64devkit/i686-w64-mingw32/lib \
    -lraylib -lopengl32 -lgdi32 -lwinmm
```

Para ejecutar el binario generado:
```bash
./NeonTetris.exe
```

---

## 6. Estructura del Código Fuente

```text
Neon-Tetris/
├── NeonTetris.zpr             # Archivo de configuración de proyecto para ZinjaI
├── main.cpp                   # Ciclo principal del juego, máquina de estados y eventos
├── scores.json                # Archivo de persistencia de mejores puntajes
├── README.md                  # Este documento
│
├── estructuras/               # Estructuras de datos lineales propias
│   ├── Tablero.h / .cpp       # Lista enlazada de filas (matriz dinámica no-STL)
│   ├── Cola.h / .cpp          # Cola FIFO para piezas siguientes (bolsa de 7)
│   ├── Pila.h / .cpp          # Pila LIFO de capacidad 1 para casilla Hold
│   ├── ListaDoble.h / .cpp    # Lista doblemente enlazada para historial y replay
│   ├── ColaPrioridad.h / .cpp # Cola de prioridad ordenada por tiempo de ejecución
│   └── ManejadorJSON.h / .cpp # Serializador y deserializador manual para scores.json
│
├── logica/                    # Lógica de juego y ordenamiento
│   ├── Pieza.h / .cpp         # Tetrominós, rotaciones precalculadas y coordenadas
│   └── ordenamientos.h / .cpp # Implementaciones de Bubble Sort y Merge Sort
│
└── ui/                        # Interfaz gráfica y pantallas (Raylib)
    ├── colors.h               # Paleta de colores neón y tema visual
    ├── menuScreen.h / .cpp    # Menú principal (Jugar, Ranking, Salir)
    ├── gameScreen.h / .cpp    # Renderizado del tablero, hold, next, alertas y replay
    ├── pauseScreen.h / .cpp   # Menú de pausa
    ├── gameOverScreen.h / .cpp# Pantalla de fin de juego y registro de nombre
    └── rankingScreen.h / .cpp # Pantalla de clasificación con benchmark interactivo
```

---

## 7. Resultados del Benchmark Experimental de Ordenamiento

Como parte del análisis comparativo solicitado en las especificaciones del proyecto, se evaluaron Bubble Sort ($O(n^2)$) y Merge Sort ($O(n \log n)$) utilizando datos aleatorios uniformes con mediciones de `std::chrono::high_resolution_clock`:

| Tamaño ($N$) | Bubble Sort $O(n^2)$ | Merge Sort $O(n \log n)$ | Aceleración ($T_{\text{burbuja}} / T_{\text{merge}}$) |
| :---: | :---: | :---: | :---: |
| **$10$** | $0.9\ \mu\text{s}$ ($0.0009\text{ ms}$) | $1.0\ \mu\text{s}$ ($0.0010\text{ ms}$) | **$1.00\times$** (Empate técnico por sobrecarga de llamadas) |
| **$100$** | $117.5\ \mu\text{s}$ ($0.1175\text{ ms}$) | $38.5\ \mu\text{s}$ ($0.0385\text{ ms}$) | **$3.05\times$** a favor de Merge Sort |
| **$1\,000$** | $12\,333\ \mu\text{s}$ ($12.33\text{ ms}$) | $650\ \mu\text{s}$ ($0.65\text{ ms}$) | **$18.97\times$** a favor de Merge Sort |
| **$10\,000$** | $1\,309\,150\ \mu\text{s}$ ($1.309\text{ s}$) | $5\,857\ \mu\text{s}$ ($5.86\text{ ms}$) | **$223.49\times$** a favor de Merge Sort |

---

## 8. Autoría y Control de Versiones

- **Desarrollo:** Realizado de forma individual con historial de control de versiones incremental mediante **Git**.
- **Registro de Versiones:** Consulte el archivo [`CHANGELOG.md`](CHANGELOG.md) para el detalle cronológico de cada hito y funcionalidad implementada.
- **Herramientas de Asistencia:** Se utilizaron herramientas asistivas durante el desarrollo conforme a las directrices de la sección 4 y 6 de la especificación de cátedra, manteniendo el dominio y comprensión técnica total del código fuente para la defensa oral individual.
