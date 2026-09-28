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

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
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
def generar_word_final(ruta_logo, ruta_grafico, ruta_docx):
    doc = docx.Document()

    # Márgenes de 1 pulgada estándar
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Configuración de estilo normal: Arial 12, interlineado 1.5
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)

    def agregar_p(texto="", bold_prefix="", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0, line_spacing=1.5):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)

        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.name = 'Arial'
            r_b.font.size = Pt(12)
            r_b.bold = True

        if texto:
            r_t = p.add_run(texto)
            r_t.font.name = 'Arial'
            r_t.font.size = Pt(12)

        return p

    def agregar_titulo_seccion(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(texto)
        r.font.name = 'Arial'
        r.font.size = Pt(14)
        r.bold = True
        return p

    def agregar_subtitulo(texto):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(texto)
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        r.bold = True
        return p

    # ------------------ PORTADA (ESTRUCTURA VERTICAL EXACTA DEL WORD EJEMPLO) ------------------
    if os.path.exists(ruta_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(20)
        p_logo.paragraph_format.space_after = Pt(14)
        doc.add_picture(ruta_logo, width=Inches(2.0))

    agregar_p("Sede Regional Brunca", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    doc.paragraphs[-1].runs[0].bold = True

    agregar_p("Campus Pérez Zeledón", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    agregar_p("Curso: Estructuras de Datos", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    agregar_p("Proyecto 1: Neon Tetris", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)
    doc.paragraphs[-1].runs[0].bold = True

    agregar_p("Estudiante:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    agregar_p("Luis Andres Elizondo Hernandez", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    agregar_p("Profesores: Saray María Castro Mora", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    agregar_p("Pablo Andrés Venegas Elizondo", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    agregar_p("II Ciclo - NRC 51005 - Grupo 82", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    agregar_p("27 de septiembre del 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)

    # Salto de página para que el contenido empiece en la página 2
    doc.add_page_break()

    # ------------------ INTRODUCCIÓN Y DESCRIPCIÓN DEL SISTEMA ------------------
    agregar_titulo_seccion("Introducción y Descripción del Sistema")

    agregar_p(
        "En este primer proyecto del curso de Estructuras de Datos desarrollamos una versión funcional de Tetris llamada \"Neon Tetris\" "
        "en C++, utilizando la biblioteca gráfica Raylib y el entorno ZinjaI. El objetivo principal fue programar todas las estructuras de "
        "datos lineales vistas en clase (colas, pilas, listas enlazadas y ordenamientos) desde cero con nodos y punteros en memoria dinámica, "
        "sin usar las librerías estándar de C++ (STL)."
    )

    agregar_p(
        "El juego se desarrolla en un tablero de 10 columnas por 20 filas donde caen 7 tipos de piezas clásicas. "
        "Cada mecánica clave del juego fue pensada para resolverse con la estructura lineal que le corresponde de forma natural: "
        "la secuencia de piezas que van a salir usa una cola; la reserva de una pieza para después (hold) usa una pila; el historial para "
        "deshacer jugadas y el replay usa una lista doblemente enlazada; los eventos con temporizador usan una cola de prioridad; "
        "y el tablero completo se modela como una lista enlazada de filas. Además, implementamos dos métodos de ordenamiento (Burbuja y Merge Sort) "
        "para ordenar la tabla de puntajes guardada en JSON y comparamos sus tiempos de ejecución reales para ver cómo rinden en la práctica."
    )

    # ------------------ ARQUITECTURA DEL SISTEMA ------------------
    agregar_titulo_seccion("Arquitectura del Sistema y Relación entre Estructuras")

    agregar_p(
        "El proyecto está dividido en tres carpetas para mantener el código ordenado: estructuras (clases de datos y punteros), "
        "lógica (piezas, rotaciones precalculadas y ordenamientos) y ui (pantallas y diseño visual con Raylib). "
        "En el archivo principal main.cpp se conectan todas las estructuras en un bucle que funciona de la siguiente manera:"
    )

    agregar_p(
        "Se encarga de abastecer las piezas del juego. Para evitar que salgan piezas repetidas muchas veces seguidas o pase mucho tiempo sin una pieza larga, "
        "usamos el sistema oficial de bolsa de 7: se mezclan las 7 piezas clásicas con el algoritmo de Fisher-Yates en O(n) y se encolan. Conforme caen, se van "
        "sacando con desencolar(), y en la pantalla se muestran las 3 siguientes consultando los primeros nodos con obtenerEn(k). Al vaciarse la cola, se baraja "
        "y se encola una nueva bolsa automáticamente.",
        bold_prefix="• Cola de piezas siguientes (Cola): "
    )

    agregar_p(
        "La mecánica de Hold permite apartar la pieza actual para usarla después con la tecla Shift Derecho. Lo resolvimos con una pila de capacidad 1. "
        "Si la pila está vacía, la pieza actual se apila y se saca una nueva de la cola de piezas; si ya había una pieza guardada, se intercambian sacando la guardada "
        "y apilando la que estaba cayendo. Se usa una bandera para que el jugador solo pueda hacer un cambio por turno hasta que la pieza caiga.",
        bold_prefix="• Pila para la pieza en espera (Pila): "
    )

    agregar_p(
        "En vez de ser una matriz estática en un bloque fijo de memoria, el tablero es una lista enlazada de 20 filas por 10 columnas donde cada celda apunta a sus "
        "vecinas (arriba, abajo, izquierda y derecha). Al fijarse una pieza, se revisa si hay filas llenas. Si las hay, se hace una animación visual de destello de "
        "250 ms y luego limpiarLineas() desconecta los punteros verticales de las filas llenas, libera los nodos con delete y agrega filas vacías al inicio.",
        bold_prefix="• Tablero como lista de filas (Tablero): "
    )

    agregar_p(
        "Cada vez que se coloca una pieza o se limpian líneas, se guarda una copia del tablero y del puntaje en un nodo de la lista doble. Al tener punteros "
        "siguiente y anterior, durante la partida el jugador puede presionar Z para deshacer jugadas (retroceder) o Y para rehacerlas (avanzar) en tiempo real. "
        "Cuando la partida termina en Game Over, esta misma lista permite el modo Replay, donde se puede recorrer toda la partida paso a paso o en reproducción "
        "continua automática cada 0.5 s.",
        bold_prefix="• Lista doblemente enlazada para historial y replay (ListaDoble): "
    )

    agregar_p(
        "Planifica eventos dinámicos que cambian la partida: aumento de velocidad temporal, líneas de basura desde abajo (Terremoto) o bonos de puntaje. "
        "La cola mantiene los eventos ordenados por tiempo. Como el evento que debe ocurrir más pronto queda siempre al frente (en la posición 0), "
        "consultarlo con verTiempoFrente() toma O(1), y al cumplirse el tiempo de la partida se extrae en O(log n) y se aplica su efecto.",
        bold_prefix="• Cola de prioridad para eventos programados (ColaPrioridad): "
    )

    agregar_p(
        "Al terminar una partida, el jugador puede ingresar su nombre y el puntaje se guarda en scores.json usando la clase ManejadorJSON. "
        "En la pantalla de Ranking, el jugador puede ver la lista de récords y puede alternar entre Bubble Sort (O(n²)) y Merge Sort (O(n log n)), "
        "viendo en pantalla el tiempo exacto que tardó cada uno en microsegundos.",
        bold_prefix="• Persistencia y ordenamiento de puntajes: "
    )

    # ------------------ COMPLEJIDAD TEÓRICA ------------------
    agregar_titulo_seccion("Complejidad Teórica Asintótica (Notación Big-O)")

    agregar_p("En la siguiente tabla resumimos la complejidad teórica de las operaciones principales de las estructuras implementadas en el proyecto:")

    tbl_comp = doc.add_table(rows=1, cols=7)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_comp.autofit = False

    encabezados_c = ["Estructura", "Operación", "Mejor", "Promedio", "Peor", "Espacio", "Descripción Breve"]
    anchos_c = [Inches(1.1), Inches(1.1), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.6), Inches(1.7)]

    hdr = tbl_comp.rows[0]
    for idx, nombre in enumerate(encabezados_c):
        cell = hdr.cells[idx]
        cell.width = anchos_c[idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(nombre)
        r.font.name = 'Arial'
        r.font.size = Pt(9.0)
        r.bold = True

    filas_c = [
        ("Cola FIFO", "encolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta directo al final usando el puntero ultimo."),
        ("Cola FIFO", "desencolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Saca del frente y libera el nodo con delete."),
        ("Cola FIFO", "obtenerEn(k)", "O(1)", "O(k)", "O(n)", "O(1)", "Recorre hasta la posición k para ver piezas futuras."),
        ("Pila LIFO", "apilar() / desapilar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta o extrae directamente en el tope."),
        ("Lista Doble", "agregarEstado()", "O(1)", "O(1)", "O(1)", "O(F*C)", "Inserta al final; clona la matriz de 20x10 y puntaje."),
        ("Lista Doble", "retroceder() [Undo]", "O(1)", "O(1)", "O(1)", "O(1)", "Paso al nodo anterior: actual = actual->anterior."),
        ("Lista Doble", "avanzar() [Redo]", "O(1)", "O(1)", "O(1)", "O(1)", "Paso al nodo siguiente: actual = actual->siguiente."),
        ("Cola Prioridad", "encolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Inserta y se acomoda comparando con los anteriores."),
        ("Cola Prioridad", "desencolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Saca el evento del frente y reacomoda el arreglo."),
        ("Cola Prioridad", "verTiempoFrente()", "O(1)", "O(1)", "O(1)", "O(1)", "Consulta directa al primer evento en arreglo[0]."),
        ("Tablero", "limpiarLineas()", "O(F*C)", "O(F*C)", "O(F*C)", "O(1)", "Reconecta punteros verticales y crea filas nuevas arriba."),
        ("Ordenamiento", "Bubble Sort", "O(n)", "O(n²)", "O(n²)", "O(1)", "Comparaciones e intercambios adyacentes de vecinos."),
        ("Ordenamiento", "Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Divide recursivamente y mezcla sub-arreglos.")
    ]

    for f_idx, fila in enumerate(filas_c):
        row = tbl_comp.add_row()
        color = "F9F9F9" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = anchos_c[c_idx]
            set_cell_background(cell, color)
            set_cell_margins(cell, top=35, bottom=35, left=45, right=45)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            if c_idx in [2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            if c_idx in [2, 3, 4, 5]:
                r.bold = True

    # SALTO DE PÁGINA OBLIGATORIO: Para que la Sección 4 (Benchmark) NUNCA quede cortada entre páginas
    doc.add_page_break()

    # ------------------ COMPARACIÓN EMPÍRICA Y BENCHMARK ------------------
    agregar_titulo_seccion("4. Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)")

    agregar_p(
        "Medimos con <chrono> en C++ el tiempo real en microsegundos ordenando listas aleatorias de jugadores con puntajes entre 0 y 100 000 "
        "para N = 10, 100, 1 000 y 10 000 registros (promedio de 5 corridas por caso):"
    )

    tbl_bench = doc.add_table(rows=1, cols=6)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_bench.autofit = False

    encabezados_b = ["Tamaño (N)", "Bubble Sort (µs)", "Bubble Sort (ms)", "Merge Sort (µs)", "Merge Sort (ms)", "Diferencia de Rendimiento"]
    anchos_b = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)]

    hdr_b = tbl_bench.rows[0]
    for idx, nombre in enumerate(encabezados_b):
        cell = hdr_b.cells[idx]
        cell.width = anchos_b[idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=45, bottom=45, left=45, right=45)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(nombre)
        r.font.name = 'Arial'
        r.font.size = Pt(9.0)
        r.bold = True

    datos_b = [
        ("N = 10", "0.90 µs", "0.0009 ms", "1.00 µs", "0.0010 ms", "Empate técnico (0.9x)"),
        ("N = 100", "117.50 µs", "0.1175 ms", "38.50 µs", "0.0385 ms", "Merge 3.05x más rápido"),
        ("N = 1 000", "12 333.00 µs", "12.33 ms", "650.00 µs", "0.65 ms", "Merge 18.97x más rápido"),
        ("N = 10 000", "1 309 150.00 µs", "1 309.15 ms", "5 857.00 µs", "5.86 ms", "Merge 223.51x más rápido")
    ]

    for f_idx, fila in enumerate(datos_b):
        row = tbl_bench.add_row()
        color = "F9F9F9" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = anchos_b[c_idx]
            set_cell_background(cell, color)
            set_cell_margins(cell, top=35, bottom=35, left=40, right=40)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(val)
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            if c_idx == 5:
                r.bold = True

    # Espacio antes del gráfico
    p_sp_g = doc.add_paragraph()
    p_sp_g.paragraph_format.space_before = Pt(8)
    p_sp_g.paragraph_format.space_after = Pt(2)

    # Gráfico embebido personalizado
    if os.path.exists(ruta_grafico):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_after = Pt(2)
        doc.add_picture(ruta_grafico, width=Inches(5.9))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        r_cap = p_cap.add_run("Figura 1: Comparación de tiempos reales y factor de aceleración entre Bubble Sort y Merge Sort.")
        r_cap.font.name = 'Arial'
        r_cap.font.size = Pt(9.0)
        r_cap.italic = True

    agregar_p(
        "Análisis de resultados:\n"
        "• Con N = 10, los dos algoritmos tardan casi lo mismo (0.9 µs vs 1.0 µs). De hecho, Bubble Sort fue una fracción más rápido "
        "porque trabaja sobre el mismo arreglo sin el sobrecosto de llamadas a funciones recursivas ni la reserva de memoria dinámica para la mezcla.\n"
        "• Con N = 100, Merge Sort ya toma la delantera siendo 3 veces más veloz (38.5 µs frente a 117.5 µs).\n"
        "• Con N = 1 000, la diferencia se vuelve evidente: Merge Sort tarda solo 0.65 ms mientras que Bubble Sort tarda 12.33 ms (casi 19 veces más rápido).\n"
        "• Con N = 10 000, la diferencia es gigantesca: Bubble Sort tarda más de 1.3 segundos (1 309.15 ms), lo que en un juego congelaría la pantalla "
        "de forma notoria, mientras que Merge Sort completa todo en menos de 6 milisegundos (5.86 ms), siendo más de 223 veces más rápido.\n"
        "• En cuanto al crecimiento: al multiplicar los datos por 10 (de 1 000 a 10 000), Bubble Sort aumentó su tiempo unas 106 veces "
        "(de 12.33 ms a 1 309.15 ms). En cambio, Merge Sort solo aumentó 9 veces (de 0.65 ms a 5.86 ms), confirmando su comportamiento casi lineal O(n log n)."
    )

    # ------------------ RESPUESTAS A PREGUNTAS ------------------
    agregar_titulo_seccion("5. Respuestas a las preguntas de análisis")

    agregar_subtitulo("Pregunta 1: Comparación de O(n²) vs. O(n log n), umbral de diferencia y notación asintótica")
    agregar_p(
        "Con pocos datos (N = 10), ambos algoritmos empatan técnicamente en rendimiento (0.9 µs para Bubble Sort y 1.0 µs para Merge Sort). "
        "Para tamaños muy pequeños las pocas operaciones directas de Bubble Sort son tan rápidas que compensan no tener la complejidad de Merge Sort, "
        "el cual gasta tiempo extra llamando funciones recursivas y pidiendo memoria para su arreglo temporal. "
        "La diferencia comienza a notarse claramente a partir de N = 100, donde Merge Sort ya es 3 veces más rápido. Con N = 1 000 ya es 19 veces más veloz, "
        "y con N = 10 000 la brecha es total: Bubble Sort tarda 1.31 segundos y Merge Sort apenas 5.86 milisegundos (más de 223 veces más rápido).\n"
        "Sí coincide plenamente con lo esperado: Bubble Sort es cuadrático O(n²) multiplicando su tiempo por 100 al multiplicar datos por 10 "
        "(en nuestra prueba aumentó 106 veces), mientras que Merge Sort escala como O(n log n) con un crecimiento mucho más suave y eficiente."
    )

    agregar_subtitulo("Pregunta 2: Representación del tablero como lista enlazada de filas y costo de operaciones")
    agregar_p(
        "En un arreglo estático común de 20x10, cuando se llena una fila en el medio hay que hacer bucles para copiar y mover físicamente hacia abajo "
        "todas las celdas de las filas superiores, haciendo hasta 190 copias de memoria innecesarias. Al modelar el tablero como una lista enlazada de filas, "
        "las filas de arriba no se tienen que mover en la memoria: simplemente se desconectan los punteros verticales (arriba y abajo) de la fila que se completó, "
        "se reconecta la fila inmediatamente superior con la inferior y se libera la fila eliminada. Las filas superiores bajan automáticamente porque sus enlaces "
        "ahora apuntan a la fila correcta sin tocar su contenido interno.\n"
        "• Costo de eliminar una fila completa: Se recorren las 10 columnas desconectando los punteros verticales y liberando las celdas con delete. "
        "Esto toma exactamente 10 liberaciones y 20 reasignaciones de puntero, representando un costo de O(C) operaciones (que es O(1) tiempo constante "
        "porque el ancho de 10 columnas es fijo).\n"
        "• Costo de insertar una fila vacía: Se crean 10 celdas vacías con new, se enlazan de izquierda a derecha y se conectan sus punteros abajo a la fila "
        "que estaba arriba, actualizando el puntero origen del tablero. Toma 10 creaciones y unas 30 asignaciones de puntero: costo O(C) (O(1) constante)."
    )

    agregar_subtitulo("Pregunta 3: Necesidad de la lista doblemente enlazada para el replay y costo de avanzar y retroceder")
    agregar_p(
        "Para implementar las funciones de deshacer y el replay necesitamos movernos en el tiempo en ambas direcciones (hacia adelante y hacia atrás). "
        "En una lista simplemente enlazada cada nodo solo conoce al nodo siguiente. Avanzar en el tiempo es directo (actual = actual->siguiente), pero para "
        "retroceder un solo paso es imposible regresar desde el nodo actual: habría que empezar a buscar desde la cabeza de la lista recorriendo nodo por nodo "
        "hasta encontrar cuál apuntaba al actual. Si la partida lleva k jugadas, cada pulsación para retroceder tomaría O(k) operaciones, lo que causaría "
        "congelamientos y tirones de pantalla. La lista doblemente enlazada resuelve esto porque cada nodo guarda tanto su puntero siguiente como su puntero anterior.\n"
        "• Costo de avanzar un paso (historial.avanzar() / Tecla Y o botón Replay Adelante): Solo hace actual = actual->siguiente. Toma O(1) operaciones elementales.\n"
        "• Costo de retroceder un paso (historial.retroceder() / Tecla Z o botón Replay Atrás): Solo hace actual = actual->anterior. Toma O(1) operaciones elementales."
    )

    agregar_subtitulo("Pregunta 4: Garantía del evento más próximo al frente y costo de inserción en la cola de eventos")
    agregar_p(
        "Para la cola de eventos hicimos una estructura que se mantiene ordenada por tiempo. Cada vez que metemos un evento nuevo, se inserta y se va "
        "comparando con los elementos anteriores para acomodarse en su posición correcta según el segundo exacto en el que tiene que activarse. "
        "De esta forma, el evento que tiene que ocurrir más pronto siempre queda de primero (en la posición 0). Para revisar si ya le toca activarse, "
        "el juego solo tiene que consultar ese primer elemento en O(1). Insertar un evento nuevo solo toma O(log n) operaciones porque se va dividiendo "
        "a la mitad en cada paso, lo cual es muy rápido y evita tener que ordenar toda la lista desde cero cada vez."
    )

    # ------------------ CONCLUSIONES ------------------
    agregar_titulo_seccion("Conclusiones")
    agregar_p(
        "Hacer el proyecto sin usar la STL nos ayudó a entender cómo funcionan los punteros y la memoria dinámica por dentro, "
        "y lo importante que es liberar siempre con delete para no dejar fugas de memoria.",
        bold_prefix="• "
    )
    agregar_p(
        "Cada mecánica del juego tuvo sentido con su estructura: la cola para las piezas que vienen, la pila para el hold, "
        "la lista de filas para el tablero, la lista doble para deshacer jugadas y el replay, y la cola de prioridad para los eventos del juego.",
        bold_prefix="• "
    )
    agregar_p(
        "Con las pruebas de rendimiento vimos de forma real lo que nos enseñan en clase: con poquitos datos casi cualquier algoritmo sirve, "
        "pero ya con 10 000 datos Merge Sort tarda 5 milisegundos mientras que Bubble Sort se queda pegado más de un segundo.",
        bold_prefix="• "
    )

    doc.save(ruta_docx)
    print(f"Documento Word final generado en: {ruta_docx}")

# =============================================================
# 2. GENERAR DOCUMENTO PDF (CON MISMOS TEXTOS Y SALTO DE PÁGINA)
# =============================================================
def generar_pdf_final(ruta_logo, ruta_grafico, ruta_pdf):
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    estilo_portada_bold = ParagraphStyle(
        'PortadaBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    estilo_portada = ParagraphStyle(
        'Portada',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    estilo_titulo = ParagraphStyle(
        'TituloSeccion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=6
    )
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=3
    )
    estilo_cuerpo = ParagraphStyle(
        'Cuerpo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=5
    )
    estilo_tabla = ParagraphStyle(
        'CeldaTabla',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        alignment=TA_LEFT
    )
    estilo_tabla_center = ParagraphStyle(
        'CeldaTablaCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        alignment=TA_CENTER
    )
    estilo_tabla_hdr = ParagraphStyle(
        'CeldaTablaHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    story = []

    # ------------------ PORTADA VERTICAL ------------------
    story.append(Spacer(1, 15))
    if os.path.exists(ruta_logo):
        story.append(Image(ruta_logo, width=145, height=145 * (145 / 271)))
        story.append(Spacer(1, 15))

    story.append(Paragraph("Sede Regional Brunca", estilo_portada_bold))
    story.append(Paragraph("Campus Pérez Zeledón", estilo_portada))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Curso: Estructuras de Datos", estilo_portada))
    story.append(Paragraph("Proyecto 1: Neon Tetris", estilo_portada_bold))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Estudiante:", estilo_portada))
    story.append(Paragraph("Luis Andres Elizondo Hernandez", estilo_portada))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Profesores: Saray María Castro Mora", estilo_portada))
    story.append(Paragraph("Pablo Andrés Venegas Elizondo", estilo_portada))
    story.append(Paragraph("II Ciclo - NRC 51005 - Grupo 82", estilo_portada))
    story.append(Spacer(1, 35))

    story.append(Paragraph("27 de septiembre del 2026", estilo_portada))
    story.append(PageBreak())

    # ------------------ CONTENIDO ------------------
    story.append(Paragraph("Introducción y Descripción del Sistema", estilo_titulo))
    story.append(Paragraph(
        "En este primer proyecto del curso de Estructuras de Datos desarrollamos una versión funcional de Tetris llamada \"Neon Tetris\" "
        "en C++, utilizando la biblioteca gráfica Raylib y el entorno ZinjaI. El objetivo principal fue programar todas las estructuras de "
        "datos lineales vistas en clase (colas, pilas, listas enlazadas y ordenamientos) desde cero con nodos y punteros en memoria dinámica, "
        "sin usar las librerías estándar de C++ (STL).",
        estilo_cuerpo
    ))
    story.append(Paragraph(
        "El juego se desarrolla en un tablero de 10 columnas por 20 filas donde caen 7 tipos de piezas clásicas. "
        "Cada mecánica clave del juego fue pensada para resolverse con la estructura lineal que le corresponde de forma natural: "
        "la secuencia de piezas que van a salir usa una cola; la reserva de una pieza para después (hold) usa una pila; el historial para "
        "deshacer jugadas y el replay usa una lista doblemente enlazada; los eventos con temporizador usan una cola de prioridad; "
        "y el tablero completo se modela como una lista enlazada de filas. Además, implementamos dos métodos de ordenamiento (Burbuja y Merge Sort) "
        "para ordenar la tabla de puntajes guardada en JSON y comparamos sus tiempos de ejecución reales para ver cómo rinden en la práctica.",
        estilo_cuerpo
    ))

    story.append(Paragraph("Arquitectura del Sistema y Relación entre Estructuras", estilo_titulo))
    story.append(Paragraph(
        "El proyecto está dividido en tres carpetas: estructuras (clases de datos y punteros), lógica (piezas, rotaciones precalculadas y ordenamientos) "
        "y ui (pantallas y diseño visual con Raylib). En el archivo principal main.cpp se conectan todas las estructuras en un bucle interactivo:<br/>"
        "• <b>Cola de piezas siguientes (Cola):</b> Abastece las piezas del juego con la bolsa de 7 mediante Fisher-Yates en O(n). Conforme caen, se extraen con desencolar() y la pantalla muestra las 3 siguientes consultando con obtenerEn(k). Al vaciarse, se encola otra bolsa.<br/>"
        "• <b>Pila para la pieza en espera (Pila):</b> Hold con capacidad 1 activado con Shift Derecho. Si la pila está vacía, guarda la actual y extrae una nueva; si ya había una, las intercambia. Se limita a un solo cambio por turno.<br/>"
        "• <b>Tablero como lista de filas (Tablero):</b> Lista enlazada de 20 filas por 10 columnas con celdas conectadas en cuatro direcciones. Al completarse líneas, tras un flash de 250 ms, limpiarLineas() desvincula los nodos de las filas llenas, libera la memoria con delete y agrega filas vacías al inicio.<br/>"
        "• <b>Lista doblemente enlazada para historial y replay (ListaDoble):</b> Guarda una copia del tablero y puntaje tras cada jugada. Durante la partida, Z (deshacer) e Y (rehacer) mueven el puntero actual en O(1). En Game Over, el modo Replay reproduce toda la partida paso a paso o en autoplay cada 0.5 s.<br/>"
        "• <b>Cola de prioridad para eventos programados (ColaPrioridad):</b> Planifica eventos por tiempo (aumento de velocidad, líneas de basura o bonos). Mantiene los eventos ordenados por tiempo. Como el evento que debe ocurrir antes queda siempre al frente (posición 0), consultarlo con verTiempoFrente() toma O(1), y al vencer el tiempo se extrae en O(log n) y se aplica su efecto.<br/>"
        "• <b>Persistencia y ordenamiento de puntajes:</b> Los récords se guardan en scores.json con ManejadorJSON. En el Ranking, el jugador puede alternar entre Bubble Sort (O(n²)) y Merge Sort (O(n log n)), viendo el tiempo exacto en microsegundos.",
        estilo_cuerpo
    ))

    story.append(Paragraph("Complejidad Teórica Asintótica (Notación Big-O)", estilo_titulo))
    story.append(Paragraph("En la siguiente tabla resumimos la complejidad teórica de las operaciones principales de las estructuras implementadas en el proyecto:", estilo_cuerpo))

    filas_c = [
        [Paragraph("<b>Estructura</b>", estilo_tabla_hdr), Paragraph("<b>Operación</b>", estilo_tabla_hdr), Paragraph("<b>Mejor</b>", estilo_tabla_hdr), Paragraph("<b>Prom.</b>", estilo_tabla_hdr), Paragraph("<b>Peor</b>", estilo_tabla_hdr), Paragraph("<b>Espacio</b>", estilo_tabla_hdr), Paragraph("<b>Descripción Breve</b>", estilo_tabla_hdr)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta directo al final usando puntero ultimo.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Saca del frente y libera el nodo con delete.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("obtenerEn(k)", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(k)", estilo_tabla_center), Paragraph("O(n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Recorre secuencialmente para ver piezas siguientes.", estilo_tabla)],
        [Paragraph("Pila LIFO", estilo_tabla), Paragraph("apilar / desapilar", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta o extrae directamente en el tope.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("agregarEstado()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("Inserta al final; clona matriz 20x10 y puntaje.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("retroceder [Undo]", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Paso al nodo anterior: actual = actual->anterior.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("avanzar [Redo]", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Paso al nodo siguiente: actual = actual->siguiente.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta y se acomoda comparando con anteriores.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Saca evento del frente y reacomoda el arreglo.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("verTiempoFrente()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Consulta directa al primer evento en arreglo[0].", estilo_tabla)],
        [Paragraph("Tablero", estilo_tabla), Paragraph("limpiarLineas()", estilo_tabla), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Reconecta punteros verticales y crea filas arriba.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Bubble Sort", estilo_tabla), Paragraph("O(n)", estilo_tabla_center), Paragraph("O(n²)", estilo_tabla_center), Paragraph("O(n²)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Comparaciones e intercambios de vecinos.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Merge Sort", estilo_tabla), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n)", estilo_tabla_center), Paragraph("División recursiva y mezcla lineal en buffer temporal.", estilo_tabla)]
    ]
    t_comp = Table(filas_c, colWidths=[65, 80, 40, 44, 44, 42, 197])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EAEAEA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#DDDDDD')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F9F9F9'), colors.white]),
    ]))
    story.append(t_comp)

    # SALTO DE PÁGINA EN PDF: Para que la tabla de benchmark y gráfico empiecen juntos en página nueva
    story.append(PageBreak())

    # ------------------ BENCHMARK ------------------
    story.append(Paragraph("4. Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)", estilo_titulo))
    story.append(Paragraph(
        "Medimos con &lt;chrono&gt; en C++ el tiempo real en microsegundos ordenando listas aleatorias de jugadores con puntajes "
        "entre 0 y 100 000 para N = 10, 100, 1 000 y 10 000 registros (promedio de 5 corridas por caso):",
        estilo_cuerpo
    ))

    filas_b = [
        [Paragraph("<b>Tamaño (N)</b>", estilo_tabla_hdr), Paragraph("<b>Bubble Sort (µs)</b>", estilo_tabla_hdr), Paragraph("<b>Bubble Sort (ms)</b>", estilo_tabla_hdr), Paragraph("<b>Merge Sort (µs)</b>", estilo_tabla_hdr), Paragraph("<b>Merge Sort (ms)</b>", estilo_tabla_hdr), Paragraph("<b>Diferencia de Rendimiento</b>", estilo_tabla_hdr)],
        [Paragraph("N = 10", estilo_tabla_center), Paragraph("0.90 µs", estilo_tabla_center), Paragraph("0.0009 ms", estilo_tabla_center), Paragraph("1.00 µs", estilo_tabla_center), Paragraph("0.0010 ms", estilo_tabla_center), Paragraph("Empate técnico (0.9x)", estilo_tabla_center)],
        [Paragraph("N = 100", estilo_tabla_center), Paragraph("117.50 µs", estilo_tabla_center), Paragraph("0.1175 ms", estilo_tabla_center), Paragraph("38.50 µs", estilo_tabla_center), Paragraph("0.0385 ms", estilo_tabla_center), Paragraph("Merge 3.05x más rápido", estilo_tabla_center)],
        [Paragraph("N = 1 000", estilo_tabla_center), Paragraph("12 333.00 µs", estilo_tabla_center), Paragraph("12.33 ms", estilo_tabla_center), Paragraph("650.00 µs", estilo_tabla_center), Paragraph("0.65 ms", estilo_tabla_center), Paragraph("Merge 18.97x más rápido", estilo_tabla_center)],
        [Paragraph("N = 10 000", estilo_tabla_center), Paragraph("1 309 150.00 µs", estilo_tabla_center), Paragraph("1 309.15 ms", estilo_tabla_center), Paragraph("5 857.00 µs", estilo_tabla_center), Paragraph("5.86 ms", estilo_tabla_center), Paragraph("<b>Merge 223.51x más rápido</b>", estilo_tabla_center)]
    ]
    t_bench = Table(filas_b, colWidths=[70, 85, 85, 80, 80, 112])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EAEAEA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#DDDDDD')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F9F9F9'), colors.white]),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 6))

    if os.path.exists(ruta_grafico):
        story.append(Image(ruta_grafico, width=490, height=490 * (540 / 1000)))
        story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Análisis de resultados:</b> Con N = 10 ambos empatan (0.9 µs vs 1.0 µs) por la simpleza de Bubble sin llamadas recursivas ni buffers. "
        "En N = 100 Merge ya es 3x más rápido, en N = 1 000 es 19x más rápido y en N = 10 000 la diferencia es total: Bubble tarda 1.31 s "
        "mientras que Merge finaliza en 5.86 ms (<b>223.5x más veloz</b>). Al multiplicar N por 10 (de 1 000 a 10 000), Bubble aumentó su tiempo 106 veces "
        "(de 12.33 ms a 1 309.15 ms). En cambio, Merge creció solo 9 veces, confirmando su comportamiento casi lineal O(n log n).",
        estilo_cuerpo
    ))

    # ------------------ RESPUESTAS ------------------
    story.append(Paragraph("5. Respuestas a las preguntas de análisis", estilo_titulo))

    story.append(Paragraph("Pregunta 1: Comparación de O(n²) vs. O(n log n), umbral de diferencia y notación asintótica", estilo_subtitulo))
    story.append(Paragraph(
        "Con pocos datos (N = 10) ambos empatan (0.9 µs vs 1.0 µs) porque las pocas comparaciones de Bubble Sort son tan rápidas que compensan no tener la complejidad de Merge Sort, el cual gasta tiempo en recursión y memoria para su arreglo temporal. La diferencia se nota con claridad a partir de N = 100 (Merge 3x más veloz), en N = 1 000 es 19x más rápido y en N = 10 000 la brecha es total (Bubble 1.31 s vs Merge 5.86 ms, 223.5x más rápido). Sí coincide plenamente con lo esperado: Bubble Sort es cuadrático O(n²) multiplicando su tiempo por 100 al multiplicar datos por 10 (en nuestra prueba aumentó 106 veces), mientras que Merge Sort escala como O(n log n) con un crecimiento mucho más suave y eficiente.",
        estilo_cuerpo
    ))

    story.append(Paragraph("Pregunta 2: Representación del tablero como lista enlazada de filas y costo de operaciones", estilo_subtitulo))
    story.append(Paragraph(
        "En una matriz común de 20x10, al llenarse una fila en el medio hay que hacer bucles para copiar y mover físicamente hacia abajo todas las celdas superiores (hasta 190 copias de memoria). Con la lista enlazada de filas, las filas superiores no se mueven de la memoria: simplemente se desconectan los punteros verticales de la fila llena, se reconecta la fila superior con la inferior y se libera la fila con delete. Las filas de arriba bajan automáticamente porque sus enlaces ahora apuntan abajo sin alterar su contenido.<br/>"
        "• <i>Eliminar fila completa:</i> Recorre las 10 columnas desconectando enlaces y liberando memoria: toma 10 deletes y 20 reasignaciones de puntero, costo <b>O(C)</b> (O(1) constante con C = 10 fijo).<br/>"
        "• <i>Insertar fila vacía al tope:</i> Crea 10 celdas con new y conecta punteros abajo a la fila superior existente: toma 10 news y 30 asignaciones de puntero, costo <b>O(C)</b> (O(1) constante).",
        estilo_cuerpo
    ))

    story.append(Paragraph("Pregunta 3: Necesidad de la lista doblemente enlazada para el replay y costo de avanzar y retroceder", estilo_subtitulo))
    story.append(Paragraph(
        "Para deshacer y ver el replay necesitamos movernos en ambas direcciones. En una lista simple cada nodo solo conoce al siguiente: avanzar es directo (actual = actual->siguiente), pero retroceder obligaría a buscar desde la cabeza nodo por nodo hasta encontrar cuál apuntaba al actual. En una partida de k jugadas, cada retroceso costaría O(k) operaciones, congelando la pantalla. La lista doble resuelve esto porque cada nodo guarda tanto siguiente como anterior.<br/>"
        "• <i>Avanzar (historial.avanzar() / Tecla Y):</i> Ejecuta actual = actual->siguiente en <b>O(1)</b> operaciones.<br/>"
        "• <i>Retroceder (historial.retroceder() / Tecla Z):</i> Ejecuta actual = actual->anterior en <b>O(1)</b> operaciones.",
        estilo_cuerpo
    ))

    story.append(Paragraph("Pregunta 4: Garantía del evento más próximo al frente y costo de inserción en la cola de eventos", estilo_subtitulo))
    story.append(Paragraph(
        "Para la cola de eventos hicimos una estructura que se mantiene ordenada por tiempo. Cada vez que metemos un evento nuevo, se inserta y se va comparando con los elementos anteriores para acomodarse en su posición correcta según el segundo exacto en el que tiene que activarse. De esta forma, el evento que tiene que ocurrir más pronto siempre queda de primero (en la posición 0). Para revisar si ya le toca activarse, el juego solo tiene que consultar ese primer elemento en O(1). Insertar un evento nuevo solo toma O(log n) operaciones porque se va dividiendo a la mitad en cada paso, lo cual es muy rápido y evita tener que ordenar toda la lista desde cero cada vez.",
        estilo_cuerpo
    ))

    story.append(Paragraph("Conclusiones", estilo_titulo))
    story.append(Paragraph(
        "• Hacer el proyecto sin usar la STL nos ayudó a entender cómo funcionan los punteros y la memoria dinámica por dentro, y lo importante que es liberar siempre con delete para no dejar fugas de memoria.<br/>"
        "• Cada mecánica del juego tuvo sentido con su estructura: la cola para las piezas que vienen, la pila para el hold, la lista de filas para el tablero, la lista doble para deshacer jugadas y el replay, y la cola de prioridad para los eventos del juego.<br/>"
        "• Con las pruebas de rendimiento vimos de forma real lo que nos enseñan en clase: con poquitos datos casi cualquier algoritmo sirve, pero ya con 10 000 datos Merge Sort tarda 5 milisegundos mientras que Bubble Sort se queda pegado más de un segundo.",
        estilo_cuerpo
    ))

    doc.build(story)
    print(f"Documento PDF final generado en: {ruta_pdf}")

if __name__ == '__main__':
    base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    logo = os.path.join(base, "scratch", "image1.png")
    graf = os.path.join(base, "scratch", "benchmark_custom.png")
    docx_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.docx")
    pdf_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.pdf")

    generar_word_final(logo, graf, docx_path)
    generar_pdf_final(logo, graf, pdf_path)
