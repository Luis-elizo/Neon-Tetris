import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=90, right=90):
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

# =============================================================
# 1. GENERAR DOCUMENTO WORD (DOCX)
# =============================================================
def generar_word(ruta_logo, ruta_grafico, ruta_docx):
    doc = docx.Document()

    # Márgenes: 0.8 pulgadas para un documento académico estructurado y limpio
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)

    # Colores institucionales sobrios
    COLOR_UNA = RGBColor(160, 20, 35)      # Rojo UNA
    COLOR_AZUL = RGBColor(40, 55, 75)      # Azul Pizarra Oscuro
    COLOR_TEXTO = RGBColor(30, 30, 30)

    # ------------------ PORTADA ------------------
    if os.path.exists(ruta_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(8)
        doc.add_picture(ruta_logo, width=Inches(2.1))

    # Título institucional
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_after = Pt(2)
    r = p_inst.add_run("UNIVERSIDAD NACIONAL DE COSTA RICA\n")
    r.font.name = 'Calibri'
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = COLOR_UNA

    r2 = p_inst.add_run("FACULTAD DE CIENCIAS EXACTAS Y NATURALES\nESCUELA DE INFORMÁTICA — SEDE REGIONAL BRUNCA\nCAMPUS PÉREZ ZELEDÓN\nCARRERA DE INGENIERÍA EN SISTEMAS DE INFORMACIÓN")
    r2.font.name = 'Calibri'
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = COLOR_AZUL

    # Espacio intermedio
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(18)
    p_sp.paragraph_format.space_after = Pt(4)

    # Título del Proyecto
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_after = Pt(4)
    r_tit = p_tit.add_run("PROYECTO I: NEON TETRIS\n")
    r_tit.font.name = 'Calibri'
    r_tit.font.size = Pt(18)
    r_tit.bold = True
    r_tit.font.color.rgb = COLOR_UNA

    r_sub = p_tit.add_run("Implementación con Estructuras de Datos Lineales Dinámicas Propias")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(12)
    r_sub.italic = True
    r_sub.font.color.rgb = COLOR_AZUL

    # Espacio antes del cuadro
    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(24)
    p_sp2.paragraph_format.space_after = Pt(8)

    # Tabla con datos del curso tomados de la Carta al Estudiante
    tbl_portada = doc.add_table(rows=4, cols=2)
    tbl_portada.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_portada.autofit = False

    datos_portada = [
        ("Curso:", "EIF207 — Estructuras de Datos", "Ciclo Lectivo:", "II Ciclo Lectivo 2026"),
        ("Estudiante:", "Luis Andrés Elizondo Hernández", "Código del Curso:", "EIF207 (BA-INFORM 572101)"),
        ("Docentes:", "M.Sc. Saray María Castro Mora\nM.Sc. Pablo Andrés Venegas Elizondo", "Grupo / Sede:", "Grupo 82 — Campus Pérez Zeledón"),
        ("Entorno de Desarrollo:", "IDE ZinjaI / GCC MinGW (C++14)", "Fecha de Entrega:", "27 de septiembre del 2026")
    ]

    for f_idx, fila in enumerate(tbl_portada.rows):
        c0, c1 = fila.cells[0], fila.cells[1]
        c0.width = Inches(3.4)
        c1.width = Inches(3.4)
        set_cell_background(c0, "F5F7FA")
        set_cell_background(c1, "F5F7FA")
        set_cell_margins(c0, top=60, bottom=60, left=90, right=90)
        set_cell_margins(c1, top=60, bottom=60, left=90, right=90)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        r0_b = p0.add_run(datos_portada[f_idx][0] + " ")
        r0_b.bold = True
        r0_b.font.size = Pt(9.5)
        p0.add_run(datos_portada[f_idx][1]).font.size = Pt(9.5)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.space_after = Pt(2)
        r1_b = p1.add_run(datos_portada[f_idx][2] + " ")
        r1_b.bold = True
        r1_b.font.size = Pt(9.5)
        p1.add_run(datos_portada[f_idx][3]).font.size = Pt(9.5)

    doc.add_page_break()

    # ------------------ HELPERS DE SECCIÓN ------------------
    def agregar_seccion(num, titulo):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"{num}. {titulo}")
        r.font.name = 'Calibri'
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = COLOR_UNA
        return p

    def agregar_subseccion(titulo):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(titulo)
        r.font.name = 'Calibri'
        r.font.size = Pt(11)
        r.bold = True
        r.font.color.rgb = COLOR_AZUL
        return p

    def agregar_p(texto, bold_prefix="", space_after=5):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(space_after)
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = 'Calibri'
            r_b.font.size = Pt(10.5)
            r_b.bold = True
        if texto:
            r_t = p.add_run(texto)
            r_t.font.name = 'Calibri'
            r_t.font.size = Pt(10.5)
            r_t.font.color.rgb = COLOR_TEXTO
        return p

    # ------------------ SECCIÓN 1 ------------------
    agregar_seccion("1", "Introducción y Descripción del Sistema")
    agregar_p(
        "En este primer proyecto del curso desarrollamos una versión completa de Tetris llamada \"Neon Tetris\" programada en C++ "
        "con la librería gráfica Raylib. La meta principal fue poner en práctica las estructuras de datos lineales que vimos en clase "
        "(pilas, colas, listas enlazadas, colas de prioridad y algoritmos de ordenamiento), pero hechas totalmente a mano mediante nodos, "
        "punteros y memoria dinámica con new y delete, sin usar ningún contenedor de la biblioteca estándar (STL como std::vector, std::queue o std::stack)."
    )
    agregar_p(
        "El juego se desarrolla en un tablero de 10 columnas por 20 filas donde caen 7 tipos de piezas clásicas (tetrominós). "
        "Cada mecánica clave del juego fue pensada para resolverse con la estructura lineal que le corresponde de forma natural: "
        "la secuencia de piezas que van a salir usa una cola; la reserva de una pieza para después (hold) usa una pila; el historial para "
        "deshacer jugadas y el replay usa una lista doblemente enlazada; los eventos con temporizador usan un montículo de prioridad; "
        "y el tablero completo se modela como una lista enlazada de filas. Además, implementamos dos métodos de ordenamiento (Burbuja y Merge Sort) "
        "para ordenar la tabla de puntajes guardada en JSON y comparamos sus tiempos de ejecución reales para ver cómo encajan con la teoría."
    )

    # ------------------ SECCIÓN 2 ------------------
    agregar_seccion("2", "Arquitectura del Sistema y Relación entre Estructuras")
    agregar_p(
        "El proyecto está dividido en tres capas para mantener el código claro y ordenado: estructuras (clases de datos y punteros), "
        "lógica (piezas, rotaciones precalculadas y ordenamientos) y ui (pantallas y diseño visual con Raylib). "
        "En el archivo principal main.cpp se conectan todas las estructuras en un bucle que funciona de la siguiente manera:"
    )

    items_estructuras = [
        ("Cola de piezas futuras (Cola): ", "Se encarga de abastecer las piezas del juego. Para evitar que salgan piezas repetidas muchas veces seguidas, usamos el sistema oficial de bolsa de 7: se mezclan las 7 piezas clásicas con el algoritmo de Fisher-Yates en O(n) y se encolan. Conforme caen, se van sacando con desencolar(), y en la pantalla se muestran las 3 siguientes consultando los primeros nodos con obtenerEn(k). Al vaciarse la cola, se baraja y se encola una nueva bolsa automáticamente."),
        ("Pila para la pieza en espera (Pila): ", "La mecánica de Hold permite apartar la pieza actual para usarla después con la tecla Shift Derecho. Lo resolvimos con una pila de capacidad 1. Si la pila está vacía, la pieza actual se apila y se saca una nueva de la cola de piezas; si ya había una pieza guardada, se intercambian sacando la guardada y apilando la que estaba cayendo. Se usa una bandera para que el jugador solo pueda hacer un cambio por turno hasta que la pieza se fije."),
        ("Tablero como lista de filas (Tablero): ", "En vez de ser una matriz estática en un bloque fijo de memoria, el tablero es una lista enlazada de 20 filas por 10 columnas donde cada celda apunta a sus vecinas (arriba, abajo, izquierda y derecha). Al fijarse una pieza, se revisa si hay filas llenas. Si las hay, se hace una animación visual de destello de 250 ms y luego limpiarLineas() desconecta los punteros verticales de las filas llenas, libera los nodos con delete y agrega filas vacías al inicio."),
        ("Lista doblemente enlazada para historial y replay (ListaDoble): ", "Cada vez que se coloca una pieza o se limpian líneas, se guarda una copia del tablero y del puntaje en un nodo de la lista doble. Al tener punteros siguiente y anterior, durante la partida el jugador puede presionar Z para deshacer jugadas (retroceder) o Y para rehacerlas (avanzar) en tiempo real. Cuando la partida termina en Game Over, esta misma lista permite el modo Replay, donde se puede recorrer toda la partida paso a paso o en reproducción continua automática cada 0.5 s."),
        ("Cola de prioridad para eventos programados (ColaPrioridad): ", "Planifica eventos dinámicos que cambian la partida: aumento de velocidad temporal, líneas de basura desde abajo (Terremoto) o bonos de puntaje. La estructura es un montículo binario mínimo (Min-Heap) ordenado por la marca de tiempo (timestamp). Como el evento que debe ocurrir más pronto queda siempre en la raíz (posición 0), consultarlo con verTiempoFrente() toma O(1), y al llegar la hora se extrae en O(log n) y se aplica su efecto."),
        ("Persistencia y ordenamiento de la tabla de puntajes: ", "Al terminar una partida, el jugador puede ingresar su nombre y el puntaje se guarda en scores.json usando la clase ManejadorJSON. En la pantalla de Ranking, el jugador puede ver la lista de récords y puede alternar entre Bubble Sort (O(n²)) y Merge Sort (O(n log n)), viendo en pantalla el tiempo exacto que tardó cada uno en microsegundos.")
    ]

    for neg, desc in items_estructuras:
        agregar_p(desc, bold_prefix=neg)

    # ------------------ SECCIÓN 3 ------------------
    agregar_seccion("3", "Complejidad Teórica Asintótica (Notación Big-O)")
    agregar_p("A continuación se presenta la tabla con la complejidad teórica temporal y espacial de cada operación implementada:")

    tbl_comp = doc.add_table(rows=1, cols=7)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_comp.autofit = False

    encabezados_c = ["Estructura", "Operación", "Mejor", "Promedio", "Peor", "Espacio", "Descripción Breve"]
    anchos_c = [Inches(1.1), Inches(1.1), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.6), Inches(1.8)]

    hdr = tbl_comp.rows[0]
    for idx, nombre in enumerate(encabezados_c):
        cell = hdr.cells[idx]
        cell.width = anchos_c[idx]
        set_cell_background(cell, "2B3A4A")
        set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(nombre)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    filas_c = [
        ("Cola FIFO", "encolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta directo al final usando el puntero ultimo."),
        ("Cola FIFO", "desencolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Saca del frente y libera el nodo con delete."),
        ("Cola FIFO", "obtenerEn(k)", "O(1)", "O(k)", "O(n)", "O(1)", "Recorre secuencialmente hasta ver las 3 piezas siguientes."),
        ("Pila LIFO", "apilar() / desapilar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta o extrae directamente en el puntero tope."),
        ("Lista Doble", "agregarEstado()", "O(1)", "O(1)", "O(1)", "O(F*C)", "Inserta al final; clona la matriz de 20x10 y puntaje."),
        ("Lista Doble", "retroceder() [Undo]", "O(1)", "O(1)", "O(1)", "O(1)", "Paso al nodo anterior: actual = actual->anterior."),
        ("Lista Doble", "avanzar() [Redo]", "O(1)", "O(1)", "O(1)", "O(1)", "Paso al nodo siguiente: actual = actual->siguiente."),
        ("Cola Prioridad", "encolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Inserta al final y flota hacia arriba (sift-up)."),
        ("Cola Prioridad", "desencolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Saca la raíz y reacomoda hacia abajo (sift-down)."),
        ("Cola Prioridad", "verTiempoFrente()", "O(1)", "O(1)", "O(1)", "O(1)", "Consulta directa a la raíz en la posición arreglo[0]."),
        ("Tablero", "limpiarLineas()", "O(F*C)", "O(F*C)", "O(F*C)", "O(1)", "Reconecta punteros verticales y crea filas nuevas arriba."),
        ("Ordenamiento", "Bubble Sort", "O(n)", "O(n²)", "O(n²)", "O(1)", "Comparaciones e intercambios adyacentes de vecinos."),
        ("Ordenamiento", "Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "División recursiva y mezcla lineal en buffer temporal.")
    ]

    for f_idx, fila in enumerate(filas_c):
        row = tbl_comp.add_row()
        color = "F6F8FA" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = anchos_c[c_idx]
            set_cell_background(cell, color)
            set_cell_margins(cell, top=40, bottom=40, left=45, right=45)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            if c_idx in [2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx in [2, 3, 4, 5]:
                r.bold = True

    p_sp3 = doc.add_paragraph()
    p_sp3.paragraph_format.space_after = Pt(4)

    # ------------------ SECCIÓN 4 ------------------
    agregar_seccion("4", "Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)")
    agregar_p(
        "Para comprobar cómo se comportan estos algoritmos en la práctica, creamos un programa de pruebas (benchmark.cpp) "
        "utilizando la librería <chrono> de C++ para medir tiempos en microsegundos (µs). Generamos listas aleatorias de jugadores "
        "con puntajes entre 0 y 100 000 para tamaños de 10, 100, 1 000 y 10 000 registros, promediando 5 repeticiones por cada caso:"
    )

    tbl_bench = doc.add_table(rows=1, cols=6)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_bench.autofit = False

    encabezados_b = ["Tamaño (N)", "Bubble Sort (µs)", "Bubble Sort (ms)", "Merge Sort (µs)", "Merge Sort (ms)", "Diferencia de Rendimiento"]
    anchos_b = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.2)]

    hdr_b = tbl_bench.rows[0]
    for idx, nombre in enumerate(encabezados_b):
        cell = hdr_b.cells[idx]
        cell.width = anchos_b[idx]
        set_cell_background(cell, "8B1E2D")
        set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(nombre)
        r.font.name = 'Calibri'
        r.font.size = Pt(8.5)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    datos_b = [
        ("N = 10", "0.90 µs", "0.0009 ms", "1.00 µs", "0.0010 ms", "Empate técnico (0.9x)"),
        ("N = 100", "117.50 µs", "0.1175 ms", "38.50 µs", "0.0385 ms", "Merge 3.05x más rápido"),
        ("N = 1 000", "12 333.00 µs", "12.33 ms", "650.00 µs", "0.65 ms", "Merge 18.97x más rápido"),
        ("N = 10 000", "1 309 150.00 µs", "1 309.15 ms", "5 857.00 µs", "5.86 ms", "Merge 223.51x más rápido")
    ]

    for f_idx, fila in enumerate(datos_b):
        row = tbl_bench.add_row()
        color = "FFF5F5" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = anchos_b[c_idx]
            set_cell_background(cell, color)
            set_cell_margins(cell, top=40, bottom=40, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(8.5)
            if c_idx == 5:
                r.bold = True

    p_sp4 = doc.add_paragraph()
    p_sp4.paragraph_format.space_after = Pt(4)

    # Gráfico embebido
    if os.path.exists(ruta_grafico):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(ruta_grafico, width=Inches(5.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run("Figura 1: Gráfico comparativo de tiempos entre Bubble Sort y Merge Sort en escala logarítmica.")
        r_cap.font.name = 'Calibri'
        r_cap.font.size = Pt(8.5)
        r_cap.italic = True
        r_cap.font.color.rgb = RGBColor(100, 100, 100)

    agregar_p(
        "Análisis de los resultados:\n"
        "• Con N = 10, los dos algoritmos tardan casi lo mismo (0.9 µs vs 1.0 µs). De hecho, Bubble Sort fue una fracción más rápido "
        "porque trabaja sobre el mismo arreglo sin el sobrecosto de llamadas a funciones recursivas ni la reserva de memoria dinámica para la mezcla.\n"
        "• Con N = 100, Merge Sort ya toma la delantera siendo 3 veces más veloz (38.5 µs frente a 117.5 µs).\n"
        "• Con N = 1 000, la diferencia se vuelve evidente: Merge Sort tarda solo 0.65 ms mientras que Bubble Sort tarda 12.33 ms (casi 19 veces más rápido).\n"
        "• Con N = 10 000, la diferencia es gigantesca: Bubble Sort tarda más de 1.3 segundos (1 309.15 ms), lo que en un juego congelaría la pantalla "
        "de forma notoria, mientras que Merge Sort completa todo en menos de 6 milisegundos (5.86 ms), siendo más de 223 veces más rápido.\n"
        "• En cuanto al crecimiento: al multiplicar los datos por 10 (de 1 000 a 10 000), Bubble Sort aumentó su tiempo unas 106 veces "
        "(de 12.33 ms a 1 309.15 ms), lo que confirma su comportamiento cuadrático O(n²) donde (10)² = 100. En cambio, Merge Sort solo aumentó "
        "9 veces (de 0.65 ms a 5.86 ms), cumpliendo con la tasa suave que predice O(n log n)."
    )

    # ------------------ SECCIÓN 5 ------------------
    agregar_seccion("5", "Respuestas a las Preguntas de Análisis Obligatorias (Sección 7)")

    agregar_subseccion("Pregunta 1: Comparación de O(n²) vs. O(n log n), umbral de diferencia y notación asintótica")
    agregar_p(
        "Con pocos datos (N = 10), ambos algoritmos empatan técnicamente en rendimiento (0.9 µs para Bubble Sort y 1.0 µs para Merge Sort). "
        "Para tamaños muy pequeños las pocas operaciones directas de Bubble Sort son tan rápidas que compensan no tener la complejidad matemática de Merge Sort, "
        "el cual gasta tiempo extra llamando funciones recursivas y pidiendo memoria para su buffer temporal. "
        "La diferencia comienza a notarse claramente a partir de N = 100, donde Merge Sort es 3 veces más rápido. Con N = 1 000 ya es 19 veces más veloz, "
        "y con N = 10 000 la brecha es total: Bubble Sort tarda 1.31 segundos y Merge Sort apenas 5.86 milisegundos (más de 223 veces más rápido).\n"
        "Sí coincide plenamente con lo que predice la notación asintótica: Bubble Sort es cuadrático (O(n²)), por lo que si los datos aumentan 10 veces, "
        "el tiempo de cómputo se multiplica por ~100 (en la prueba creció 106 veces). Mientras tanto, Merge Sort es O(n log n), creciendo a un ritmo "
        "casi lineal y manteniéndose sumamente eficiente sin importar el volumen de datos."
    )

    agregar_subseccion("Pregunta 2: Representación del tablero como lista enlazada de filas y costo de operaciones")
    agregar_p(
        "En un arreglo estático común de 20x10, cuando se llena una fila en el medio hay que hacer bucles para copiar y mover físicamente hacia abajo "
        "todas las celdas de las filas superiores, haciendo hasta 190 copias de memoria innecesarias. Al modelar el tablero como una lista enlazada de filas, "
        "las filas de arriba no se tienen que mover en la memoria: simplemente se desconectan los punteros verticales (arriba y abajo) de la fila que se completó, "
        "se reconecta la fila inmediatamente superior con la inferior y se libera la fila eliminada. Las filas superiores 'bajan' automáticamente porque sus enlaces "
        "ahora apuntan a la fila correcta sin tocar su contenido interno.\n"
        "• Costo de eliminar una fila completa: Se recorren las 10 columnas desconectando los punteros verticales y liberando las celdas con delete. "
        "Esto toma exactamente 10 liberaciones y 20 reasignaciones de puntero, representando un costo de O(C) operaciones (que es O(1) tiempo constante "
        "porque el ancho de 10 columnas es fijo).\n"
        "• Costo de insertar una fila vacía: Se crean 10 celdas vacías con new, se enlazan de izquierda a derecha y se conectan sus punteros abajo a la fila "
        "que estaba arriba, actualizando el puntero origen del tablero. Toma 10 creaciones y unas 30 asignaciones de puntero: costo O(C) (O(1) constante)."
    )

    agregar_subseccion("Pregunta 3: Necesidad de la lista doblemente enlazada para el replay y costo de avanzar y retroceder")
    agregar_p(
        "Para implementar las funciones de deshacer y el replay necesitamos movernos en el tiempo en ambas direcciones (hacia adelante y hacia atrás). "
        "En una lista simplemente enlazada cada nodo solo conoce al nodo siguiente. Avanzar en el tiempo es directo (actual = actual->siguiente), pero para "
        "retroceder un solo paso es imposible regresar desde el nodo actual: habría que empezar a buscar desde la cabeza de la lista recorriendo nodo por nodo "
        "hasta encontrar cuál apuntaba al actual. Si la partida lleva k jugadas, cada pulsación para retroceder tomaría O(k) operaciones, lo que causaría "
        "congelamientos y tirones de pantalla. La lista doblemente enlazada resuelve esto porque cada nodo guarda tanto su puntero siguiente como su puntero anterior.\n"
        "• Costo de avanzar un paso (historial.avanzar() / Tecla Y o botón Replay Adelante): Solo hace actual = actual->siguiente. Toma O(1) operaciones elementales.\n"
        "• Costo de retroceder un paso (historial.retroceder() / Tecla Z o botón Replay Atrás): Solo hace actual = actual->anterior. Toma O(1) operaciones elementales."
    )

    agregar_subseccion("Pregunta 4: Garantía del evento más próximo al frente y costo de inserción en la cola de eventos")
    agregar_p(
        "Nuestra clase ColaPrioridad está construida sobre un montículo binario mínimo (Min-Heap) en un arreglo dinámico. La estructura garantiza en todo "
        "momento la propiedad de montículo: el tiempo de disparo de cualquier nodo padre siempre es menor o igual al tiempo de sus dos nodos hijos "
        "(arreglo[i].tiempo <= arreglo[2i+1].tiempo y arreglo[i].tiempo <= arreglo[2i+2].tiempo). Por definición matemática, el evento que tiene el menor "
        "tiempo de disparo (el que debe ocurrir más pronto) queda garantizado en la raíz del árbol (posición arreglo[0]). Consultar cuál es el próximo evento "
        "con verTiempoFrente() cuesta O(1) tiempo constante.\n"
        "• Costo de inserción (encolar()): El nuevo evento se coloca al final del arreglo y se compara con su padre (flotación o sift-up). Si su tiempo es "
        "menor que el del padre, se intercambian y se sigue subiendo hasta que se cumpla la propiedad o se llegue a la raíz. Como un árbol binario casi completo "
        "de n elementos tiene una altura de floor(log₂ n), a lo sumo se hacen log₂ n intercambios. Por eso la inserción toma O(log n) en el caso promedio y peor caso, "
        "y O(1) en el mejor caso, cumpliendo estrictamente la instrucción de no insertar al final y reordenar todo (que tomaría O(n log n))."
    )

    # ------------------ SECCIÓN 6 ------------------
    agregar_seccion("6", "Conclusiones")
    conclusiones = [
        ("Uso de estructuras sin STL: ", "Resolver el proyecto sin librerías estándar nos ayudó a comprender a fondo el funcionamiento interno de la memoria dinámica, el manejo de punteros simples y dobles, y la responsabilidad de liberar con delete cada objeto creado con new para evitar fugas de memoria."),
        ("Acoplamiento natural con el juego: ", "Comprobamos que cada mecánica tiene una estructura ideal: la cola para turnos justos de piezas, la pila para intercambios de hold reversibles, la lista de filas para evitar mover memoria en el tablero, la lista doble para retroceder jugadas y el montículo para programar eventos en tiempo real."),
        ("Confirmación de la teoría asintótica: ", "El benchmark dejó en evidencia que para pocos datos algoritmos sencillos como Bubble Sort funcionan perfectamente, pero al trabajar con volúmenes reales como 10 000 datos, la diferencia de 1.31 segundos contra 5.86 milisegundos de Merge Sort (223.5x más rápido) demuestra que la eficiencia algorítmica es indispensable para mantener un juego fluido a 60 fotogramas por segundo.")
    ]

    for neg, desc in conclusiones:
        agregar_p(desc, bold_prefix="• " + neg)

    doc.save(ruta_docx)
    print(f"Documento Word formal generado en: {ruta_docx}")

# =============================================================
# 2. GENERAR DOCUMENTO PDF
# =============================================================
def generar_pdf(ruta_logo, ruta_grafico, ruta_pdf):
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    estilo_inst = ParagraphStyle(
        'InstUNA',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#A01423')
    )
    estilo_sub_inst = ParagraphStyle(
        'SubInstUNA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#28374B')
    )
    estilo_tit = ParagraphStyle(
        'TitProy',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#A01423')
    )
    estilo_subtit_proy = ParagraphStyle(
        'SubTitProy',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#28374B')
    )
    estilo_sec = ParagraphStyle(
        'Seccion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14.5,
        textColor=colors.HexColor('#A01423'),
        spaceBefore=9,
        spaceAfter=3
    )
    estilo_sub_sec = ParagraphStyle(
        'SubSeccion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor('#28374B'),
        spaceBefore=6,
        spaceAfter=2
    )
    estilo_cuerpo = ParagraphStyle(
        'Cuerpo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#1E1E1E'),
        spaceAfter=4
    )
    estilo_tabla = ParagraphStyle(
        'CeldaTabla',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        alignment=TA_LEFT
    )
    estilo_tabla_center = ParagraphStyle(
        'CeldaTablaCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        alignment=TA_CENTER
    )
    estilo_tabla_hdr = ParagraphStyle(
        'CeldaTablaHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=colors.white
    )

    story = []

    # ------------------ PORTADA ------------------
    story.append(Spacer(1, 10))
    if os.path.exists(ruta_logo):
        story.append(Image(ruta_logo, width=150, height=150 * (145 / 271)))
        story.append(Spacer(1, 10))

    story.append(Paragraph("UNIVERSIDAD NACIONAL DE COSTA RICA", estilo_inst))
    story.append(Paragraph("FACULTAD DE CIENCIAS EXACTAS Y NATURALES<br/>ESCUELA DE INFORMÁTICA — SEDE REGIONAL BRUNCA<br/>CAMPUS PÉREZ ZELEDÓN<br/>CARRERA DE INGENIERÍA EN SISTEMAS DE INFORMACIÓN", estilo_sub_inst))
    story.append(Spacer(1, 25))

    story.append(Paragraph("PROYECTO I: NEON TETRIS", estilo_tit))
    story.append(Paragraph("Implementación con Estructuras de Datos Lineales Dinámicas Propias", estilo_subtit_proy))
    story.append(Spacer(1, 30))

    # Cuadro de datos portada
    datos_box = [
        [
            Paragraph("<b>Curso:</b> EIF207 — Estructuras de Datos", estilo_tabla),
            Paragraph("<b>Ciclo Lectivo:</b> II Ciclo Lectivo 2026", estilo_tabla)
        ],
        [
            Paragraph("<b>Estudiante:</b> Luis Andrés Elizondo Hernández", estilo_tabla),
            Paragraph("<b>Código:</b> EIF207 (BA-INFORM 572101)", estilo_tabla)
        ],
        [
            Paragraph("<b>Docentes:</b> M.Sc. Saray María Castro Mora<br/>M.Sc. Pablo Andrés Venegas Elizondo", estilo_tabla),
            Paragraph("<b>Grupo / Sede:</b> Grupo 82 — Campus Pérez Zeledón", estilo_tabla)
        ],
        [
            Paragraph("<b>Entorno:</b> IDE ZinjaI / GCC MinGW (C++14)", estilo_tabla),
            Paragraph("<b>Fecha de Entrega:</b> 27 de septiembre del 2026", estilo_tabla)
        ]
    ]
    t_box = Table(datos_box, colWidths=[260, 260])
    t_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F5F7FA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D5DBDB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E8E8')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_box)
    story.append(PageBreak())

    # ------------------ CONTENIDO ------------------
    story.append(Paragraph("1. Introducción y Descripción del Sistema", estilo_sec))
    story.append(Paragraph(
        "En este primer proyecto del curso desarrollamos una versión completa de Tetris llamada \"Neon Tetris\" programada en C++ "
        "con la librería gráfica Raylib. La meta principal fue poner en práctica las estructuras de datos lineales que vimos en clase "
        "(pilas, colas, listas enlazadas, colas de prioridad y algoritmos de ordenamiento), pero hechas totalmente a mano mediante nodos, "
        "punteros y memoria dinámica con new y delete, sin usar ningún contenedor de la biblioteca estándar (STL como std::vector, std::queue o std::stack).<br/>"
        "El juego se desarrolla en un tablero de 10 columnas por 20 filas donde caen 7 tipos de piezas clásicas (tetrominós). "
        "Cada mecánica clave del juego fue pensada para resolverse con la estructura lineal que le corresponde de forma natural: "
        "la secuencia de piezas que van a salir usa una cola; la reserva de una pieza para después (hold) usa una pila; el historial para "
        "deshacer jugadas y el replay usa una lista doblemente enlazada; los eventos con temporizador usan un montículo de prioridad; "
        "y el tablero completo se modela como una lista enlazada de filas. Además, implementamos dos métodos de ordenamiento (Burbuja y Merge Sort) "
        "para ordenar la tabla de puntajes guardada en JSON y comparamos sus tiempos de ejecución reales para ver cómo encajan con la teoría.",
        estilo_cuerpo
    ))

    story.append(Paragraph("2. Arquitectura del Sistema y Relación entre Estructuras", estilo_sec))
    story.append(Paragraph(
        "El proyecto está dividido en tres capas: estructuras (clases de datos y punteros), lógica (piezas, rotaciones precalculadas y ordenamientos) "
        "y ui (pantallas y diseño visual con Raylib). En el archivo principal main.cpp se conectan todas las estructuras en un bucle interactivo:<br/>"
        "• <b>Cola de piezas futuras (Cola):</b> Abastece las piezas del juego. Usamos el sistema oficial de bolsa de 7: se barajan las 7 piezas con Fisher-Yates en O(n) y se encolan. Conforme caen, se extraen con desencolar() y la pantalla muestra las 3 siguientes consultando con obtenerEn(k). Al vaciarse la cola, se genera otra bolsa.<br/>"
        "• <b>Pila para la pieza en espera (Pila):</b> Hold con capacidad 1 activado con Shift Derecho. Si la pila está vacía, guarda la actual y extrae una nueva; si ya había una, las intercambia. Se limita a un solo cambio por turno hasta fijar la pieza.<br/>"
        "• <b>Tablero como lista de filas (Tablero):</b> Lista enlazada de 20 filas por 10 columnas con celdas conectadas en cuatro direcciones. Al completarse líneas, tras un flash de 250 ms, limpiarLineas() desvincula los nodos de las filas llenas, libera la memoria con delete y agrega filas vacías al inicio.<br/>"
        "• <b>Lista doblemente enlazada (ListaDoble):</b> Guarda una copia del tablero y puntaje tras cada jugada. Durante la partida, Z (deshacer) e Y (rehacer) mueven el puntero actual en O(1). En Game Over, el modo Replay reproduce toda la partida paso a paso o en autoplay cada 0.5 s.<br/>"
        "• <b>Cola de prioridad para eventos programados (ColaPrioridad):</b> Montículo binario mínimo (Min-Heap) ordenado por tiempo (timestamp). Como el evento que debe ocurrir antes queda siempre en la raíz (posición 0), consultarlo con verTiempoFrente() toma O(1), y al llegar la hora se extrae en O(log n) y se aplica su efecto.<br/>"
        "• <b>Persistencia y ordenamiento:</b> Los récords se guardan en scores.json con ManejadorJSON. En el Ranking, el jugador puede alternar entre Bubble Sort (O(n²)) y Merge Sort (O(n log n)), viendo el tiempo exacto en microsegundos.",
        estilo_cuerpo
    ))

    story.append(Paragraph("3. Complejidad Teórica Asintótica (Notación Big-O)", estilo_sec))
    comp_headers = [
        Paragraph("Estructura", estilo_tabla_hdr),
        Paragraph("Operación", estilo_tabla_hdr),
        Paragraph("Mejor", estilo_tabla_hdr),
        Paragraph("Prom.", estilo_tabla_hdr),
        Paragraph("Peor", estilo_tabla_hdr),
        Paragraph("Espacio", estilo_tabla_hdr),
        Paragraph("Descripción Breve", estilo_tabla_hdr)
    ]
    comp_rows = [
        comp_headers,
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta directo al final usando puntero ultimo.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Saca del frente y libera el nodo con delete.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("obtenerEn(k)", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(k)", estilo_tabla_center), Paragraph("O(n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Recorre secuencialmente para ver piezas siguientes.", estilo_tabla)],
        [Paragraph("Pila LIFO", estilo_tabla), Paragraph("apilar / desapilar", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta o extrae directamente en el tope.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("agregarEstado()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("Inserta al final; clona matriz 20x10 y puntaje.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("retroceder [Undo]", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Paso al nodo anterior: actual = actual->anterior.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("avanzar [Redo]", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Paso al nodo siguiente: actual = actual->siguiente.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta al final y flota hacia arriba (sift-up).", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Saca la raíz y reacomoda hacia abajo (sift-down).", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("verTiempoFrente()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Consulta directa a la raíz en arreglo[0].", estilo_tabla)],
        [Paragraph("Tablero", estilo_tabla), Paragraph("limpiarLineas()", estilo_tabla), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Reconecta punteros verticales y crea filas arriba.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Bubble Sort", estilo_tabla), Paragraph("O(n)", estilo_tabla_center), Paragraph("O(n²)", estilo_tabla_center), Paragraph("O(n²)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Comparaciones e intercambios de vecinos.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Merge Sort", estilo_tabla), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n)", estilo_tabla_center), Paragraph("División recursiva y mezcla lineal en buffer temporal.", estilo_tabla)]
    ]
    t_comp = Table(comp_rows, colWidths=[65, 80, 42, 45, 45, 42, 201])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2B3A4A')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#E5E8E8')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F8F9FA'), colors.white]),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)", estilo_sec))
    story.append(Paragraph(
        "Medimos con &lt;chrono&gt; en C++ el tiempo real en microsegundos (µs) ordenando listas aleatorias de jugadores con puntajes "
        "entre 0 y 100 000 para N = 10, 100, 1 000 y 10 000 registros (promedio de 5 corridas por caso):",
        estilo_cuerpo
    ))

    bench_headers = [
        Paragraph("Tamaño (N)", estilo_tabla_hdr),
        Paragraph("Bubble Sort (µs)", estilo_tabla_hdr),
        Paragraph("Bubble Sort (ms)", estilo_tabla_hdr),
        Paragraph("Merge Sort (µs)", estilo_tabla_hdr),
        Paragraph("Merge Sort (ms)", estilo_tabla_hdr),
        Paragraph("Diferencia de Rendimiento", estilo_tabla_hdr)
    ]
    bench_rows = [
        bench_headers,
        [Paragraph("N = 10", estilo_tabla_center), Paragraph("0.90 µs", estilo_tabla_center), Paragraph("0.0009 ms", estilo_tabla_center), Paragraph("1.00 µs", estilo_tabla_center), Paragraph("0.0010 ms", estilo_tabla_center), Paragraph("Empate técnico (0.9x)", estilo_tabla_center)],
        [Paragraph("N = 100", estilo_tabla_center), Paragraph("117.50 µs", estilo_tabla_center), Paragraph("0.1175 ms", estilo_tabla_center), Paragraph("38.50 µs", estilo_tabla_center), Paragraph("0.0385 ms", estilo_tabla_center), Paragraph("Merge 3.05x más rápido", estilo_tabla_center)],
        [Paragraph("N = 1 000", estilo_tabla_center), Paragraph("12 333.00 µs", estilo_tabla_center), Paragraph("12.33 ms", estilo_tabla_center), Paragraph("650.00 µs", estilo_tabla_center), Paragraph("0.65 ms", estilo_tabla_center), Paragraph("Merge 18.97x más rápido", estilo_tabla_center)],
        [Paragraph("N = 10 000", estilo_tabla_center), Paragraph("1 309 150.00 µs", estilo_tabla_center), Paragraph("1 309.15 ms", estilo_tabla_center), Paragraph("5 857.00 µs", estilo_tabla_center), Paragraph("5.86 ms", estilo_tabla_center), Paragraph("<b>Merge 223.51x más rápido</b>", estilo_tabla_center)]
    ]
    t_bench = Table(bench_rows, colWidths=[70, 85, 85, 80, 80, 120])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8B1E2D')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#E5E8E8')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#FFF5F5'), colors.white]),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 4))

    if os.path.exists(ruta_grafico):
        story.append(Image(ruta_grafico, width=500, height=500 * (560 / 1000)))
        story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Análisis de resultados:</b> Con N = 10 ambos empatan (0.9 µs vs 1.0 µs) por la simpleza de Bubble sin llamadas recursivas ni buffers. "
        "En N = 100 Merge ya es 3x más rápido, en N = 1 000 es 19x más rápido y en N = 10 000 la diferencia es total: Bubble tarda 1.31 s "
        "mientras que Merge finaliza en 5.86 ms (<b>223.5x más veloz</b>). Al multiplicar N por 10 (de 1 000 a 10 000), Bubble aumentó su tiempo 106 veces "
        "(teoría cuadrática: 10² = 100), mientras que Merge creció solo 9 veces, confirmando su comportamiento casi lineal O(n log n).",
        estilo_cuerpo
    ))

    story.append(Paragraph("5. Respuestas a las Preguntas de Análisis Obligatorias (Sección 7)", estilo_sec))

    story.append(Paragraph("Pregunta 1: Comparación de O(n²) vs. O(n log n), umbral de diferencia y notación asintótica", estilo_sub_sec))
    story.append(Paragraph(
        "Con pocos datos (N = 10) ambos empatan (0.9 µs vs 1.0 µs) porque las pocas comparaciones de Bubble Sort son tan rápidas que compensan no tener la complejidad matemática de Merge Sort, el cual gasta tiempo en recursión y memoria para su buffer temporal. La diferencia se nota con claridad a partir de N = 100 (Merge 3x más veloz), en N = 1 000 es 19x más rápido y en N = 10 000 la brecha es total (Bubble 1.31 s vs Merge 5.86 ms, 223.5x más rápido). Coincide plenamente con la notación asintótica: Bubble Sort es cuadrático O(n²) multiplicando su tiempo por ~100 al multiplicar datos por 10, mientras Merge Sort escala como O(n log n).",
        estilo_cuerpo
    ))

    story.append(Paragraph("Pregunta 2: Representación del tablero como lista enlazada de filas y costo de operaciones", estilo_sub_sec))
    story.append(Paragraph(
        "En una matriz común de 20x10, al llenarse una fila en el medio hay que hacer bucles para copiar y mover físicamente hacia abajo todas las celdas superiores (hasta 190 copias de memoria). Con la lista enlazada de filas, las filas superiores no se mueven de la memoria: simplemente se desconectan los punteros verticales de la fila llena, se reconecta la fila superior con la inferior y se libera la fila con delete. Las filas de arriba 'caen' automáticamente porque sus enlaces ahora apuntan abajo sin alterar su contenido.<br/>"
        "• <i>Eliminar fila completa:</i> Recorre las 10 columnas desconectando enlaces y liberando memoria: toma 10 deletes y 20 reasignaciones de puntero, costo <b>O(C)</b> (O(1) constante con C = 10 fijo).<br/>"
        "• <i>Insertar fila vacía al tope:</i> Crea 10 celdas con new y conecta punteros abajo a la fila superior existente: toma 10 news y 30 asignaciones de puntero, costo <b>O(C)</b> (O(1) constante).",
        estilo_cuerpo
    ))

    story.append(Paragraph("Pregunta 3: Necesidad de la lista doblemente enlazada para el replay y costo de avanzar y retroceder", estilo_sub_sec))
    story.append(Paragraph(
        "Para deshacer y ver el replay necesitamos movernos en ambas direcciones. En una lista simple cada nodo solo conoce al siguiente: avanzar es directo (actual = actual->siguiente), pero retroceder obligaría a buscar desde la cabeza nodo por nodo hasta encontrar cuál apuntaba al actual. En una partida de k jugadas, cada retroceso costaría O(k) operaciones, congelando la pantalla. La lista doble resuelve esto porque cada nodo guarda tanto siguiente como anterior.<br/>"
        "• <i>Avanzar (historial.avanzar() / Tecla Y):</i> Ejecuta actual = actual->siguiente en <b>O(1)</b> operaciones.<br/>"
        "• <i>Retroceder (historial.retroceder() / Tecla Z):</i> Ejecuta actual = actual->anterior en <b>O(1)</b> operaciones.",
        estilo_cuerpo
    ))

    story.append(Paragraph("Pregunta 4: Garantía del evento más próximo al frente y costo de inserción en la cola de eventos", estilo_sub_sec))
    story.append(Paragraph(
        "ColaPrioridad implementa un montículo binario mínimo (Min-Heap) en un arreglo dinámico. Garantiza que el tiempo de disparo del padre siempre es menor o igual al de sus hijos. Por definición matemática, el evento con el menor tiempo (el que debe ocurrir antes) queda siempre en la raíz (arreglo[0]). Consultar el próximo evento con verTiempoFrente() cuesta <b>O(1)</b>.<br/>"
        "• <i>Inserción (encolar):</i> El nuevo evento se coloca al final y flota hacia arriba (sift-up) comparándose con su padre. Como el árbol casi completo tiene altura floor(log₂ n), a lo sumo realiza log₂ n intercambios. Toma <b>O(log n)</b> en caso promedio y peor caso, y O(1) en mejor caso, evitando reordenar todo con O(n log n).",
        estilo_cuerpo
    ))

    story.append(Paragraph("6. Conclusiones", estilo_sec))
    story.append(Paragraph(
        "• <b>Uso de estructuras sin STL:</b> Resolver el proyecto sin librerías estándar nos ayudó a comprender el funcionamiento interno de la memoria dinámica, el manejo de punteros y la disciplina de liberar con delete cada objeto creado con new para evitar fugas.<br/>"
        "• <b>Acoplamiento con las mecánicas:</b> Comprobamos que cada dinámica tiene una estructura ideal: la cola para turnos justos de piezas, la pila para hold reversible, la lista de filas para evitar mover memoria en el tablero, la lista doble para historial simétrico y el montículo para eventos por tiempo.<br/>"
        "• <b>Comprobación empírica:</b> El benchmark evidenció que para pocos datos algoritmos simples como Bubble Sort funcionan bien, pero con 10 000 datos la brecha de 1.31 s contra 5.86 ms de Merge Sort (223.5x) demuestra que la eficiencia algorítmica es indispensable para mantener 60 FPS en un juego.",
        estilo_cuerpo
    ))

    doc.build(story)
    print(f"Documento PDF formal generado en: {ruta_pdf}")

# =============================================================
# EJECUCIÓN PRINCIPAL
# =============================================================
if __name__ == '__main__':
    base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    logo = os.path.join(base, "scratch", "image1.png")
    graf = os.path.join(base, "scratch", "benchmark_chart.png")
    docx_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.docx")
    pdf_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.pdf")

    generar_word(logo, graf, docx_path)
    generar_pdf(logo, graf, pdf_path)
