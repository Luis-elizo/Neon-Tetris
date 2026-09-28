import os
import sys
from PIL import Image, ImageDraw, ImageFont
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# -------------------------------------------------------------
# 1. GENERAR GRÁFICO DEL BENCHMARK (PIL)
# -------------------------------------------------------------
def generar_grafico_benchmark(ruta_salida):
    ancho, alto = 1000, 560
    img = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    fuente_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    fuente_titulo = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 22)
    fuente_sub = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 14)
    fuente_ejes = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 13)
    fuente_ticks = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 12)
    fuente_leyenda = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 13)
    fuente_anot = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 11)

    # Título y subtítulo
    draw.text((80, 25), "Tiempo de Ejecución: Bubble Sort O(n²) vs. Merge Sort O(n log n)", fill=(25, 30, 45), font=fuente_titulo)
    draw.text((80, 55), "Medición empírica en microsegundos (µs) con escala logarítmica para N = 10, 100, 1000, 10000", fill=(100, 110, 125), font=fuente_sub)

    # Área de dibujo del gráfico
    margen_izq = 110
    margen_der = 920
    margen_sup = 100
    margen_inf = 480
    ancho_plot = margen_der - margen_izq
    alto_plot = margen_inf - margen_sup

    # Fondo del área de datos
    draw.rectangle([(margen_izq, margen_sup), (margen_der, margen_inf)], fill=(248, 249, 252), outline=(210, 215, 225), width=1)

    # Escala logarítmica en Y: desde 0.1 µs (10^-1) hasta 10,000,000 µs (10^7)
    # y_val -> log10(val)
    min_log = -0.5
    max_log = 6.5
    rango_log = max_log - min_log

    def y_a_pixel(val):
        import math
        log_v = math.log10(max(val, 0.1))
        frac = (log_v - min_log) / rango_log
        return margen_inf - (frac * alto_plot)

    # Rejilla horizontal y etiquetas en Y
    lineas_y = [
        (0.1, "0.1 µs"),
        (1.0, "1 µs"),
        (10.0, "10 µs"),
        (100.0, "100 µs"),
        (1000.0, "1 ms (1k µs)"),
        (10000.0, "10 ms"),
        (100000.0, "100 ms"),
        (1000000.0, "1 s (1M µs)")
    ]

    for val, etiqueta in lineas_y:
        py = y_a_pixel(val)
        draw.line([(margen_izq, py), (margen_der, py)], fill=(225, 230, 238), width=1)
        draw.text((margen_izq - 85, py - 7), etiqueta, fill=(110, 120, 135), font=fuente_ticks)

    # Coordenadas en X para N = [10, 100, 1000, 10000]
    n_puntos = [10, 100, 1000, 10000]
    etiquetas_x = ["N = 10", "N = 100", "N = 1,000", "N = 10,000"]
    x_pos = [
        margen_izq + ancho_plot * 0.12,
        margen_izq + ancho_plot * 0.37,
        margen_izq + ancho_plot * 0.63,
        margen_izq + ancho_plot * 0.88
    ]

    # Rejilla vertical y etiquetas X
    for xp, eti in zip(x_pos, etiquetas_x):
        draw.line([(xp, margen_sup), (xp, margen_inf)], fill=(230, 235, 242), width=1)
        draw.text((xp - 28, margen_inf + 12), eti, fill=(30, 40, 55), font=fuente_ejes)

    # Datos empíricos medidos (en µs)
    datos_bubble = [0.9, 117.5, 12333.0, 1309150.0]
    datos_merge = [1.0, 38.5, 650.0, 5857.0]

    # Puntos en píxeles
    puntos_bubble = [(xp, y_a_pixel(val)) for xp, val in zip(x_pos, datos_bubble)]
    puntos_merge = [(xp, y_a_pixel(val)) for xp, val in zip(x_pos, datos_merge)]

    # Dibujar líneas de conexión
    color_bubble = (220, 40, 70)     # Rojo/Carmín
    color_merge = (25, 120, 230)     # Azul Eléctrico

    draw.line(puntos_bubble, fill=color_bubble, width=4)
    draw.line(puntos_merge, fill=color_merge, width=4)

    # Dibujar marcadores y etiquetas en Bubble
    for i, (xp, yp) in enumerate(puntos_bubble):
        r = 6
        draw.ellipse([(xp - r, yp - r), (xp + r, yp + r)], fill=color_bubble, outline=(255, 255, 255), width=2)
        val_str = f"{datos_bubble[i]:.1f} µs" if datos_bubble[i] < 1000 else f"{datos_bubble[i]/1000:.1f} ms"
        if i == 3:
            val_str = f"{datos_bubble[i]/1000000:.2f} s"
        draw.text((xp - 25, yp - 24), val_str, fill=color_bubble, font=fuente_anot)

    # Dibujar marcadores y etiquetas en Merge
    for i, (xp, yp) in enumerate(puntos_merge):
        r = 6
        draw.rectangle([(xp - r, yp - r), (xp + r, yp + r)], fill=color_merge, outline=(255, 255, 255), width=2)
        val_str = f"{datos_merge[i]:.1f} µs" if datos_merge[i] < 1000 else f"{datos_merge[i]/1000:.2f} ms"
        draw.text((xp - 25, yp + 10), val_str, fill=color_merge, font=fuente_anot)

    # Brecha en N = 10,000 (Anotación destacada de Speedup)
    draw.line([(x_pos[3], puntos_bubble[3][1]), (x_pos[3], puntos_merge[3][1])], fill=(160, 60, 200), width=2)
    draw.text((x_pos[3] - 120, (puntos_bubble[3][1] + puntos_merge[3][1]) / 2 - 8), "223.5x más rápido", fill=(140, 30, 180), font=fuente_leyenda)

    # Leyenda en la parte superior derecha
    box_lx, box_ly = margen_der - 250, margen_sup + 15
    draw.rectangle([(box_lx, box_ly), (box_lx + 235, box_ly + 65)], fill=(255, 255, 255), outline=(200, 205, 215), width=1)

    # Item Bubble
    draw.line([(box_lx + 15, box_ly + 20), (box_lx + 45, box_ly + 20)], fill=color_bubble, width=3)
    draw.ellipse([(box_lx + 26, box_ly + 16), (box_lx + 34, box_ly + 24)], fill=color_bubble)
    draw.text((box_lx + 55, box_ly + 12), "Bubble Sort O(n²)", fill=(40, 45, 55), font=fuente_leyenda)

    # Item Merge
    draw.line([(box_lx + 15, box_ly + 45), (box_lx + 45, box_ly + 45)], fill=color_merge, width=3)
    draw.rectangle([(box_lx + 26, box_ly + 41), (box_lx + 34, box_ly + 49)], fill=color_merge)
    draw.text((box_lx + 55, box_ly + 37), "Merge Sort O(n log n)", fill=(40, 45, 55), font=fuente_leyenda)

    # Guardar imagen
    img.save(ruta_salida, format='PNG')
    print(f"Gráfico guardado en: {ruta_salida}")


# -------------------------------------------------------------
# 2. GENERAR DOCUMENTO WORD (DOCX)
# -------------------------------------------------------------
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def generar_documento_word(ruta_grafico, ruta_docx):
    doc = docx.Document()

    # Configuración de márgenes (2.0 cm para maximizar espacio útil en 5-6 páginas)
    secciones = doc.sections
    for s in secciones:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Colores corporativos UNA
    COLOR_TITULO = RGBColor(180, 20, 40)    # Rojo UNA
    COLOR_SUBTITULO = RGBColor(40, 50, 70)  # Azul oscuro
    COLOR_TEXTO = RGBColor(35, 35, 35)

    # 1. ENCABEZADO INSTITUCIONAL
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_inst.add_run("UNIVERSIDAD NACIONAL DE COSTA RICA\n")
    run_inst.bold = True
    run_inst.font.size = Pt(14)
    run_inst.font.name = "Calibri"
    run_inst.font.color.rgb = COLOR_TITULO

    run_sub = p_inst.add_run("SEDE REGIONAL BRUNCA — CAMPUS PÉREZ ZELEDÓN Y COTO\nESCUELA DE INFORMÁTICA | CURSO EIF207: ESTRUCTURAS DE DATOS\n")
    run_sub.font.size = Pt(10)
    run_sub.font.name = "Calibri"
    run_sub.font.color.rgb = COLOR_SUBTITULO

    # Título del Proyecto
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(8)
    p_tit.paragraph_format.space_after = Pt(12)
    run_t = p_tit.add_run("PROYECTO I: NEON TETRIS\nImplementación con Estructuras de Datos Lineales Dinámicas Propias")
    run_t.bold = True
    run_t.font.size = Pt(16)
    run_t.font.name = "Calibri"
    run_t.font.color.rgb = COLOR_SUBTITULO

    # Cuadro de Datos del Estudiante
    tbl_datos = doc.add_table(rows=2, cols=2)
    tbl_datos.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_datos.autofit = False

    datos_info = [
        ("Estudiante:", "Luis Andrés Elizondo Hernández", "Ciclo Lectivo:", "II Ciclo 2026"),
        ("Entorno de Desarrollo:", "ZinjaI / MinGW GCC (C++14)", "Librería Gráfica:", "Raylib (C++ Nativo)")
    ]

    for f_idx, fila in enumerate(tbl_datos.rows):
        c0, c1 = fila.cells[0], fila.cells[1]
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "F0F4F8")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        c0.width = Inches(3.4)
        c1.width = Inches(3.4)

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(datos_info[f_idx][0] + " ")
        r0.bold = True
        r0.font.size = Pt(9.5)
        p0.add_run(datos_info[f_idx][1]).font.size = Pt(9.5)

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(datos_info[f_idx][2] + " ")
        r1.bold = True
        r1.font.size = Pt(9.5)
        p1.add_run(datos_info[f_idx][3]).font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Helper para encabezados de sección
    def agregar_seccion(numero, titulo):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        run_h = h.add_run(f"{numero}. {titulo}")
        run_h.bold = True
        run_h.font.size = Pt(13)
        run_h.font.name = "Calibri"
        run_h.font.color.rgb = COLOR_TITULO

    def agregar_subseccion(titulo):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(3)
        run_h = h.add_run(titulo)
        run_h.bold = True
        run_h.font.size = Pt(11)
        run_h.font.name = "Calibri"
        run_h.font.color.rgb = COLOR_SUBTITULO

    # ---------------------------------------------------------
    # SECCIÓN 1: INTRODUCCIÓN
    # ---------------------------------------------------------
    agregar_seccion("1", "Introducción y Descripción del Sistema")
    p1 = doc.add_paragraph()
    p1.paragraph_format.space_after = Pt(6)
    p1.add_run(
        "El presente proyecto consiste en el diseño, desarrollo e implementación de un videojuego funcional basado en "
        "las mecánicas clásicas de Tetris (\"Neon Tetris\"), desarrollado en lenguaje C++. La premisa académica fundamental "
        "de este trabajo es la prohibición estricta de contenedores de la biblioteca estándar de plantillas (STL como std::vector, "
        "std::queue, std::stack, std::list, std::priority_queue), obligando al modelado manual de todas las estructuras de datos "
        "lineales mediante memoria dinámica, punteros explícitos y Tipos Abstractos de Datos (TADs).\n\n"
        "El sistema integra seis estructuras lineales especializadas, cada una acoplada de forma natural a una mecánica de juego: "
        "una Cola FIFO dinámica para la generación de piezas futuras mediante el algoritmo de bolsa de 7 (Fisher-Yates); una Pila "
        "LIFO dinámica de capacidad unitaria para la reserva e intercambio de piezas (Hold); una Lista doblemente enlazada para registrar "
        "cronológicamente los estados del tablero y permitir Deshacer (Undo), Rehacer (Redo) y Replay paso a paso; una Cola de Prioridad "
        "basada en Min-Heap para planificar eventos temporales de juego; una Matriz Ortogonal / Lista de Filas enlazada para el tablero; "
        "y algoritmos propios de ordenamiento (Bubble Sort y Merge Sort) para la tabla de mejores puntajes (Ranking) persistida en JSON."
    )

    # ---------------------------------------------------------
    # SECCIÓN 2: ARQUITECTURA DEL SISTEMA
    # ---------------------------------------------------------
    agregar_seccion("2", "Arquitectura del Sistema y Relación entre Estructuras")
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(6)
    p2.add_run(
        "La arquitectura del sistema sigue un patrón desacoplado en tres capas: Estructuras (gestión de punteros y memoria), "
        "Lógica (reglas del juego, rotación precalculada, colisiones y ordenamientos) e Interfaz de Usuario (pantallas en Raylib). "
        "A continuación se describe la interacción entre componentes:\n"
    )

    items_flujo = [
        ("Cola FIFO (Piezas Futuras): ", "Abastece continuamente al juego. Al vaciarse, la función LlenarBolsa() baraja 7 tetrominós (I, O, T, S, Z, J, L) mediante Fisher-Yates en O(n) y los encola. La pieza activa se extrae con desencolar() y la pantalla consulta obtenerEn(k) para mostrar las 3 piezas siguientes."),
        ("Pila LIFO (Hold): ", "Al pulsar Shift Derecho, intercambia la pieza activa con el tope de la pila. Si está vacía, apila la actual y desencola una nueva de la cola FIFO. Se limita a un solo intercambio por turno mediante una bandera de control."),
        ("Tablero Ortogonal (Lista de Filas): ", "Representa las 20 filas por 10 columnas como nodos enlazados en cuatro direcciones. Al fijarse una pieza, se evalúan líneas completas; tras una animación de destello de 250 ms, limpiarLineas() desvincula los nodos de las filas llenas e inserta filas vacías al inicio."),
        ("Lista Doblemente Enlazada (Historial / Replay): ", "Tras fijar una pieza o limpiar líneas, se captura una copia completa de la matriz y el puntaje en un NodoHistorial. Durante el juego, las teclas Z (deshacer) e Y (rehacer) navegan los punteros anterior y siguiente en O(1). Al finalizar la partida, el Replay permite revisar toda la partida con paso manual o reproducción automática."),
        ("Cola de Prioridad Min-Heap (Eventos Programados): ", "Mantiene ordenados cronológicamente por su timestamp eventos futuros como Fiebre de Velocidad (duplica velocidad 10 s), Terremoto (inserta línea de basura inferior) y Bonus (+500 puntos). Al cumplirse el tiempo de la raíz en O(1), se desencola en O(log n) y se aplica el efecto."),
        ("Módulo de Persistencia y Ordenamiento: ", "Los récords se guardan en scores.json sin dependencias externas. La pantalla de Ranking permite al usuario elegir entre Bubble Sort O(n²) y Merge Sort O(n log n) para ordenar los puntajes, visualizando la tabla ordenada y el tiempo de cómputo en microsegundos.")
    ]

    for neg, desc in items_flujo:
        p_item = doc.add_paragraph(style='List Bullet')
        p_item.paragraph_format.space_after = Pt(3)
        r_neg = p_item.add_run(neg)
        r_neg.bold = True
        p_item.add_run(desc)

    # ---------------------------------------------------------
    # SECCIÓN 3: COMPLEJIDAD TEÓRICA ASINTÓTICA
    # ---------------------------------------------------------
    agregar_seccion("3", "Complejidad Teórica Asintótica (Notación Big-O)")
    p3 = doc.add_paragraph()
    p3.paragraph_format.space_after = Pt(6)
    p3.add_run("La siguiente tabla detalla la complejidad formal temporal y espacial de cada operación implementada:")

    tbl_comp = doc.add_table(rows=1, cols=7)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_comp.autofit = False

    encabezados_c = ["Estructura", "Operación", "Mejor", "Promedio", "Peor", "Espacio", "Justificación Breve"]
    anchos_c = [Inches(1.1), Inches(1.1), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.6), Inches(2.0)]

    hdr_row = tbl_comp.rows[0]
    for c_idx, nombre in enumerate(encabezados_c):
        cell = hdr_row.cells[c_idx]
        cell.width = anchos_c[c_idx]
        set_cell_background(cell, "2B3A4A")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        r = p.add_run(nombre)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    filas_complejidad = [
        ("Cola FIFO", "encolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta en puntero ultimo."),
        ("Cola FIFO", "desencolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Extrae de puntero primero y libera nodo."),
        ("Cola FIFO", "obtenerEn(k)", "O(1)", "O(k)", "O(n)", "O(1)", "Recorre k nodos desde el frente."),
        ("Pila LIFO", "apilar() / desapilar()", "O(1)", "O(1)", "O(1)", "O(1)", "Modifica el nodo en tope."),
        ("Lista Doble", "agregarEstado()", "O(1)", "O(1)", "O(1)", "O(F*C)", "Inserta al final; clona matriz 20x10."),
        ("Lista Doble", "retroceder() [Undo]", "O(1)", "O(1)", "O(1)", "O(1)", "actual = actual->anterior."),
        ("Lista Doble", "avanzar() [Redo]", "O(1)", "O(1)", "O(1)", "O(1)", "actual = actual->siguiente."),
        ("Cola Prioridad", "encolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Flotación (sift-up) en montículo."),
        ("Cola Prioridad", "desencolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Hundimiento (sift-down) en montículo."),
        ("Cola Prioridad", "verTiempoFrente()", "O(1)", "O(1)", "O(1)", "O(1)", "Acceso directo a la raíz arreglo[0]."),
        ("Tablero", "limpiarLineas()", "O(F*C)", "O(F*C)", "O(F*C)", "O(1)", "Reconecta punteros de filas completas."),
        ("Ordenamiento", "Bubble Sort", "O(n)", "O(n²)", "O(n²)", "O(1)", "Comparaciones e intercambios adyacentes."),
        ("Ordenamiento", "Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "División recursiva y mezcla lineal.")
    ]

    for f_idx, fila_datos in enumerate(filas_complejidad):
        row = tbl_comp.add_row()
        color_fondo = "F8F9FA" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila_datos):
            cell = row.cells[c_idx]
            cell.width = anchos_c[c_idx]
            set_cell_background(cell, color_fondo)
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.0)
            if c_idx in [2, 3, 4, 5]:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ---------------------------------------------------------
    # SECCIÓN 4: COMPARACIÓN EMPÍRICA Y BENCHMARK
    # ---------------------------------------------------------
    agregar_seccion("4", "Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)")
    p4 = doc.add_paragraph()
    p4.paragraph_format.space_after = Pt(6)
    p4.add_run(
        "Se evaluó experimentalmente el desempeño de Bubble Sort frente a Merge Sort mediante mediciones reales de alta "
        "precisión con std::chrono::high_resolution_clock en C++. Cada experimento se promedió sobre 5 iteraciones con "
        "permutaciones aleatorias de registros idénticos conteniendo nombres sintéticos y puntajes en el rango [0, 100 000].\n"
    )

    # Tabla Benchmark
    tbl_bench = doc.add_table(rows=1, cols=6)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_bench.autofit = False

    encabezados_b = ["Tamaño (N)", "Bubble Sort (µs)", "Bubble Sort (ms)", "Merge Sort (µs)", "Merge Sort (ms)", "Factor Aceleración"]
    anchos_b = [Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.3)]

    hdr_bench = tbl_bench.rows[0]
    for c_idx, nombre in enumerate(encabezados_b):
        cell = hdr_bench.cells[c_idx]
        cell.width = anchos_b[c_idx]
        set_cell_background(cell, "8B1E2D") # Rojo oscuro UNA
        set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(nombre)
        r.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    datos_bench = [
        ("N = 10", "0.90 µs", "0.0009 ms", "1.00 µs", "0.0010 ms", "0.90x (Empate técnico)"),
        ("N = 100", "117.50 µs", "0.1175 ms", "38.50 µs", "0.0385 ms", "3.05x más rápido"),
        ("N = 1 000", "12 333.00 µs", "12.33 ms", "650.00 µs", "0.65 ms", "18.97x más rápido"),
        ("N = 10 000", "1 309 150.00 µs", "1 309.15 ms", "5 857.00 µs", "5.86 ms", "223.51x más rápido")
    ]

    for f_idx, fila_datos in enumerate(datos_bench):
        row = tbl_bench.add_row()
        color_fondo = "FFF5F5" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila_datos):
            cell = row.cells[c_idx]
            cell.width = anchos_b[c_idx]
            set_cell_background(cell, color_fondo)
            set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if c_idx == 5:
                r.bold = True

    # Gráfico embebido
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    if os.path.exists(ruta_grafico):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(ruta_grafico, width=Inches(6.2))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Figura 1: Comparación empírica en escala logarítmica de Bubble Sort O(n²) vs. Merge Sort O(n log n).")
        r_cap.font.size = Pt(8.5)
        r_cap.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)

    p_analisis = doc.add_paragraph()
    p_analisis.paragraph_format.space_after = Pt(6)
    p_analisis.add_run(
        "Análisis de Escalamiento:\n"
        "• Al multiplicar el tamaño de datos por 10 (de N = 1 000 a N = 10 000), el tiempo de Bubble Sort creció por un factor de "
        "106.1x (de 12.33 ms a 1 309.15 ms), correlacionando perfectamente con la tasa cuadrática teórica (10² = 100x).\n"
        "• Para el mismo incremento decádico, Merge Sort creció únicamente por un factor de 9.0x (de 0.65 ms a 5.86 ms), "
        "cumpliendo la cota teórica de O(n log n) que predice un factor de crecimiento aproximado de 13.3x."
    )

    # ---------------------------------------------------------
    # SECCIÓN 5: PREGUNTAS DE ANÁLISIS OBLIGATORIAS (SECCIÓN 7)
    # ---------------------------------------------------------
    agregar_seccion("5", "Respuestas a las Preguntas de Análisis Obligatorias (Sección 7)")

    preguntas = [
        (
            "Pregunta 1: Compare el tiempo de ordenar la tabla de puntajes con el algoritmo de complejidad O(n²) contra el de O(n log n), para tamaños crecientes de datos de prueba. ¿A partir de qué tamaño se nota la diferencia? ¿Coincide con lo que predice la notación asintótica?",
            "Respuesta Formativa:\n"
            "1. Umbral de Diferenciación Visible:\n"
            "Para un conjunto sumamente pequeño como N = 10, ambos algoritmos registran un empate técnico empírico (0.9 µs para Bubble Sort frente a 1.0 µs para Merge Sort). En este tamaño mínimo, Bubble Sort resulta incluso marginalmente superior debido a que opera in-place sin sobrecostos de llamadas recursivas ni asignaciones dinámicas de memoria auxiliar en el Heap. La divergencia comienza a notarse con claridad a partir de N = 100, donde Merge Sort es 3 veces más veloz (38.5 µs vs. 117.5 µs). A partir de N = 1 000 la brecha se amplía a 19x (0.65 ms vs. 12.33 ms), y al alcanzar N = 10 000 la superioridad es aplastante: Bubble Sort tarda más de 1.3 segundos (1 309 ms) congelando momentáneamente la fluidez del hilo principal, mientras que Merge Sort ordena la totalidad de registros en tan solo 5.86 milisegundos (aceleración superior a 223x).\n\n"
            "2. Coincidencia con la Notación Asintótica:\n"
            "Los resultados empíricos coinciden con exactitud matemática con la teoría asintótica. La función de tiempo de Bubble Sort escala de forma cuadrática T(n) ≈ c₁·n², lo que implica que cuadruplica su tiempo al duplicar datos y se multiplica por ~100 al decuplicarlos (en nuestra prueba real creció 106.1x al pasar de 1 000 a 10 000). Por su parte, Merge Sort se rige por la relación lineal-logarítmica T(n) ≈ c₂·n·log₂(n), manteniendo un incremento estable y suave incluso frente a volúmenes masivos de datos."
        ),
        (
            "Pregunta 2: Explique por qué representar el tablero como una lista enlazada de filas es una forma razonable de modelar la limpieza de líneas, y qué costo (en operaciones) tiene en su implementación insertar una fila vacía y eliminar una fila completa.",
            "Respuesta Formativa:\n"
            "1. Justificación del Modelado como Lista Enlazada:\n"
            "En una matriz estática contigua tradicional (como int tablero[20][10]), eliminar una fila completa intermedia obliga a 'desplazar físicamente' todos los elementos de las filas superiores hacia abajo mediante bucles anidados que realizan hasta 150 a 190 asignaciones de memoria redundantes. Al representar el tablero como una lista enlazada de filas (o matriz ortogonal de celdas bidireccionales), las filas superiores no requieren moverse de sus posiciones en memoria: simplemente se desenganchan los punteros verticales que conectaban a la fila eliminada, reconectando la fila inmediatamente superior con la fila inferior. Las filas superiores 'caen' por el simple hecho de que sus referencias ahora apuntan a la base correspondiente, conservando su configuración interna intacta.\n\n"
            "2. Costo en Operaciones en Nuestra Implementación:\n"
            "• Eliminación de una fila completa: Para C = 10 columnas, nuestra implementación itera por las 10 celdas desconectando los enlaces arriba->abajo y abajo->arriba de sus vecinos, liberando la memoria dinámica con delete nodoCelda. Esto requiere exactamente 10 liberaciones de memoria y 20 reasignaciones de puntero, representando un costo de O(C) operaciones (que es tiempo constante O(1) dado que C = 10 es fijo en Tetris).\n"
            "• Inserción de una fila vacía: Consiste en instanciar 10 nodos celda en el heap, enlazar sus punteros horizontales (izquierda/derecha) y conectar sus punteros abajo hacia la fila que anteriormente ocupaba la cúspide, actualizando el puntero origen del tablero. Esta operación requiere exactamente 10 llamadas a new y 30 asignaciones de puntero, representando un costo formal de O(C) operaciones (O(1) estricto)."
        ),
        (
            "Pregunta 3: ¿Por qué el replay requiere una lista doblemente enlazada y no una simplemente enlazada? ¿Qué costo tiene, en su implementación, retroceder o avanzar un paso?",
            "Respuesta Formativa:\n"
            "1. Necesidad de la Lista Doblemente Enlazada:\n"
            "La navegación temporal de jugadas requiere simetría bidireccional. En una lista simplemente enlazada, cada nodo únicamente cuenta con el puntero siguiente. Si bien avanzar en el tiempo es trivial (actual = actual->siguiente), retroceder un paso en una lista simple es imposible de forma local: para hallar el nodo anterior, la estructura estaría obligada a iniciar una búsqueda secuencial desde la cabeza de la lista hasta encontrar el nodo cuyo siguiente coincida con actual. En una partida de k movimientos, cada pulsación de retroceso tomaría O(k) operaciones, degradando severamente el rendimiento y la fluidez interactiva a 60 FPS. La lista doblemente enlazada resuelve esto integrando el puntero anterior en cada NodoHistorial, permitiendo retroceder instantáneamente sin importar si la partida tiene 10 o 5 000 jugadas registradas.\n\n"
            "2. Costo Operativo en Nuestra Implementación:\n"
            "• Avanzar un paso (historial.avanzar() / Tecla Y o Botón Adelante): Ejecuta una comprobación if (actual->siguiente != nullptr) y una única reasignación de puntero: actual = actual->siguiente. Costo: O(1) operaciones elementales.\n"
            "• Retroceder un paso (historial.retroceder() / Tecla Z o Botón Atrás): Ejecuta una comprobación if (actual->anterior != nullptr) y una única reasignación de puntero: actual = actual->anterior. Costo: O(1) operaciones elementales."
        ),
        (
            "Pregunta 4: ¿Cómo garantiza su implementación que la cola de eventos programados siempre mantenga al frente el evento más próximo a dispararse? ¿Qué complejidad tiene insertar un nuevo evento?",
            "Respuesta Formativa:\n"
            "1. Garantía del Evento Próximo al Frente (Min-Heap):\n"
            "Nuestra estructura ColaPrioridad no utiliza arreglos desordenados ni reordenamientos globales. Implementa un Montículo Binario Mínimo (Min-Heap) sobre un arreglo dinámico propio (NodoEvento* arreglo). La estructura mantiene de forma rigurosa la propiedad de orden de montículo:\n"
            "Para todo nodo en el índice i, su tiempoDisparo es menor o igual al tiempo de sus hijos ubicados en los índices 2i + 1 y 2i + 2:\n"
            "arreglo[i].tiempoDisparo <= arreglo[2i + 1].tiempoDisparo  y  arreglo[i].tiempoDisparo <= arreglo[2i + 2].tiempoDisparo.\n"
            "Por definición matemática, la raíz del montículo (índice arreglo[0]) contiene en todo momento el evento con el valor mínimo de tiempoDisparo de todo el conjunto. Consultar cuál es el próximo evento que debe dispararse (verTiempoFrente()) tiene un costo de tiempo constante O(1).\n\n"
            "2. Algoritmo y Complejidad de Inserción (encolar()):\n"
            "Al programar un nuevo evento, este se inserta inicialmente en la primera posición disponible al final del arreglo (índice k = tamano). Inmediatamente se ejecuta el proceso de flotación ascendente (sift-up): se compara el tiempo del nuevo nodo contra el de su padre en el índice floor((k - 1) / 2); si el nuevo evento debe ocurrir antes, se intercambian y se repite la comparación hacia arriba hasta que la propiedad de montículo quede satisfecha o se alcance la raíz.\n"
            "Dado que un árbol binario casi completo con n elementos tiene una altura estrictamente acotada por floor(log₂ n), la inserción realiza a lo sumo log₂ n intercambios. Por lo tanto, la inserción tiene una complejidad de O(log n) en el caso promedio y peor caso, y O(1) en el mejor caso (si el nuevo evento ocurre después que su padre directo). Esto cumple cabalmente la prohibición de la sección 3.3 de insertar al final y reordenar todo el arreglo (que tomaría O(n log n))."
        )
    ]

    for preg_tit, resp_cuerpo in preguntas:
        p_preg = doc.add_paragraph()
        p_preg.paragraph_format.space_before = Pt(8)
        p_preg.paragraph_format.space_after = Pt(3)
        r_p = p_preg.add_run(preg_tit)
        r_p.bold = True
        r_p.font.size = Pt(10.5)
        r_p.font.color.rgb = COLOR_SUBTITULO

        p_resp = doc.add_paragraph()
        p_resp.paragraph_format.space_after = Pt(6)
        p_resp.add_run(resp_cuerpo)

    # ---------------------------------------------------------
    # SECCIÓN 6: CONCLUSIONES
    # ---------------------------------------------------------
    agregar_seccion("6", "Conclusiones")
    conclusiones = [
        ("Acoplamiento Natural Estructura-Mecánica: ", "El desarrollo demostró que cada dinámica de juego cuenta con un modelo abstracto ideal: la Cola FIFO para secuencias futuras justas, la Pila LIFO para transacciones de intercambio reversible, la Lista Doblemente Enlazada para historiales simétricos en el tiempo y el Min-Heap para despachar eventos cronológicos sin sobrecarga computacional."),
        ("Disciplina en la Gestión Manual de Memoria: ", "La exclusión de la STL obligó a un control estricto de la memoria dinámica en C++, garantizando que cada operador new cuente con su contraparte delete en destructores y operaciones de extracción, logrando un aplicativo robusto y libre de fugas de memoria."),
        ("Corroboración Empírica de la Complejidad Asintótica: ", "El benchmark experimental confirmó que a partir de N = 100 registros la complejidad asintótica domina el rendimiento en sistemas reales. Para N = 10 000, la reducción de tiempo de 1.31 segundos (Bubble Sort) a 5.86 milisegundos (Merge Sort) demostró que una adecuada selección algorítmica es indispensable para mantener tasas de refresco interactivas de 60 cuadros por segundo.")
    ]

    for neg, desc in conclusiones:
        p_concl = doc.add_paragraph(style='List Bullet')
        p_concl.paragraph_format.space_after = Pt(4)
        r_neg = p_concl.add_run(neg)
        r_neg.bold = True
        p_concl.add_run(desc)

    doc.save(ruta_docx)
    print(f"Documento Word guardado exitosamente en: {ruta_docx}")

# -------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------
if __name__ == '__main__':
    directorio_base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    ruta_grafico = os.path.join(directorio_base, "scratch", "benchmark_chart.png")
    ruta_docx = os.path.join(directorio_base, "INFORME_PROYECTO1_EIF207.docx")

    os.makedirs(os.path.join(directorio_base, "scratch"), exist_ok=True)
    generar_grafico_benchmark(ruta_grafico)
    generar_documento_word(ruta_grafico, ruta_docx)
