import os
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=30, bottom=30, left=40, right=40):
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

def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def set_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def generar_documento_word(ruta_logo, ruta_grafico, ruta_docx):
    doc = docx.Document()

    # Márgenes de 0.85 pulgadas para que todo respire y quepa perfectamente en 6 páginas exactas
    for s in doc.sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    # Estilo base: Arial 12, interlineado 1.5
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Arial'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)

    def agregar_p(texto="", bold_prefix="", align=WD_ALIGN_PARAGRAPH.LEFT, space_after=3, space_before=0, line_spacing=1.5, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.widow_control = True
        if keep_with_next:
            p.paragraph_format.keep_with_next = True

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

    def agregar_titulo_seccion(texto, space_before=10, space_after=3):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.widow_control = True
        r = p.add_run(texto)
        r.font.name = 'Arial'
        r.font.size = Pt(13)
        r.bold = True
        return p

    def agregar_subtitulo(texto, space_before=8, space_after=2):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.keep_with_next = True
        p.paragraph_format.widow_control = True
        r = p.add_run(texto)
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        r.bold = True
        return p

    # =========================================================================
    # PÁGINA 1: PORTADA VERTICAL FORMAL (COPIA EXACTA DE LA REFERENCIA CON LOGO UNA)
    # =========================================================================
    if os.path.exists(ruta_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(12)
        p_logo.paragraph_format.space_after = Pt(16)
        doc.add_picture(ruta_logo, width=Inches(1.85))

    agregar_p("Sede Regional Brunca", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    doc.paragraphs[-1].runs[0].bold = True

    agregar_p("Campus Pérez Zeledón", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=26)

    agregar_p("Curso: Estructuras de Datos", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    agregar_p("Proyecto 1: Neon Tetris", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=26)
    doc.paragraphs[-1].runs[0].bold = True

    agregar_p("Estudiante:", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    agregar_p("Luis Andres Elizondo Hernandez", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=26)

    agregar_p("Profesores: Saray María Castro Mora", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    agregar_p("Pablo Andrés Venegas Elizondo", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    agregar_p("II Ciclo - NRC 51005 - Grupo 82", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=26)

    agregar_p("27 de septiembre del 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    # SALTO A PÁGINA 2
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 2: INTRODUCCIÓN Y ARQUITECTURA (PARTE 1)
    # =========================================================================
    agregar_titulo_seccion("Introducción y Descripción del Sistema", space_before=2)

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

    agregar_titulo_seccion("Arquitectura del Sistema y Relación entre Estructuras", space_before=8)

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

    # SALTO A PÁGINA 3 (ARQUITECTURA PARTE 2 + COMPLEJIDAD TEÓRICA ASINTÓTICA)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 3: ARQUITECTURA (FIN) Y TABLA DE COMPLEJIDAD TEÓRICA ASINTÓTICA
    # =========================================================================
    agregar_p(
        "En vez de ser una matriz estática en un bloque fijo de memoria, el tablero es una lista enlazada de 20 filas por 10 columnas donde cada celda apunta a sus "
        "vecinas (arriba, abajo, izquierda y derecha). Al fijarse una pieza, se revisa si hay filas llenas. Si las hay, se hace una animación visual de destello de "
        "250 ms y luego limpiarLineas() desconecta los punteros verticales de las filas llenas, libera los nodos con delete y agrega filas vacías al inicio.",
        bold_prefix="• Tablero como lista de filas (Tablero): ",
        space_before=2
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

    agregar_titulo_seccion("Complejidad Teórica Asintótica (Notación Big-O)", space_before=8)

    agregar_p("En la siguiente tabla resumimos la complejidad teórica de las operaciones principales de las estructuras implementadas en el proyecto:", space_after=3)

    tbl_comp = doc.add_table(rows=1, cols=7)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_comp.autofit = False

    encabezados_c = ["Estructura", "Operación", "Mejor", "Promedio", "Peor", "Espacio", "Descripción Breve"]
    anchos_c = [Inches(1.1), Inches(1.1), Inches(0.6), Inches(0.7), Inches(0.7), Inches(0.6), Inches(1.9)]

    hdr = tbl_comp.rows[0]
    set_table_header(hdr)
    prevent_row_split(hdr)
    for idx, nombre in enumerate(encabezados_c):
        cell = hdr.cells[idx]
        cell.width = anchos_c[idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=20, bottom=20, left=25, right=25)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(nombre)
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        r.bold = True

    filas_c = [
        ("Cola FIFO", "encolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta directo al final usando el puntero ultimo."),
        ("Cola FIFO", "desencolar()", "O(1)", "O(1)", "O(1)", "O(1)", "Saca del frente y libera el nodo con delete."),
        ("Cola FIFO", "obtenerEn(k)", "O(1)", "O(k)", "O(n)", "O(1)", "Recorre hasta la posición k para ver piezas futuras."),
        ("Pila LIFO", "apilar() / desapilar()", "O(1)", "O(1)", "O(1)", "O(1)", "Inserta o extrae directamente en el tope."),
        ("Lista Doble", "agregarEstado()", "O(1)", "O(1)", "O(1)", "O(F*C)", "Inserta al final; clona la matriz de 20x10 y puntaje."),
        ("Lista Doble", "retroceder() [Undo]", "O(1)", "O(1)", "O(1)", "O(1)", "Paso al nodo anterior: actual = actual->anterior."),
        ("Lista Doble", "avanzar() [Redo]", "O(1)", "O(1)", "O(1)", "O(1)", "Paso al nodo siguiente: actual = actual->siguiente."),
        ("Cola Prioridad", "encolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Inserta y se acomoda comparando con anteriores."),
        ("Cola Prioridad", "desencolar()", "O(1)", "O(log n)", "O(log n)", "O(1)", "Saca evento del frente y reacomoda el arreglo."),
        ("Cola Prioridad", "verTiempoFrente()", "O(1)", "O(1)", "O(1)", "O(1)", "Consulta directa al primer evento en arreglo[0]."),
        ("Tablero", "limpiarLineas()", "O(F*C)", "O(F*C)", "O(F*C)", "O(1)", "Reconecta punteros verticales y crea filas nuevas arriba."),
        ("Ordenamiento", "Bubble Sort", "O(n)", "O(n²)", "O(n²)", "O(1)", "Comparaciones e intercambios adyacentes de vecinos."),
        ("Ordenamiento", "Merge Sort", "O(n log n)", "O(n log n)", "O(n log n)", "O(n)", "Divide recursivamente y mezcla sub-arreglos.")
    ]

    for f_idx, fila in enumerate(filas_c):
        row = tbl_comp.add_row()
        prevent_row_split(row)
        color = "F9F9F9" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = anchos_c[c_idx]
            set_cell_background(cell, color)
            set_cell_margins(cell, top=14, bottom=14, left=25, right=25)
            p = cell.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(1)
            if c_idx in [2, 3, 4, 5]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = 'Arial'
            r.font.size = Pt(8.0)
            if c_idx in [2, 3, 4, 5]:
                r.bold = True

    # SALTO A PÁGINA 4 (SECCIÓN 4 COMPLETA: TABLA + GRÁFICO + ANÁLISIS)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 4: 4. COMPARACIÓN EMPÍRICA Y BENCHMARK (BURBUJA VS. MERGE SORT)
    # =========================================================================
    agregar_titulo_seccion("4. Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)", space_before=2, space_after=2)

    agregar_p(
        "Medimos con <chrono> en C++ el tiempo real en microsegundos ordenando listas aleatorias de jugadores con puntajes entre 0 y 100 000 "
        "para N = 10, 100, 1 000 y 10 000 registros (promedio de 5 corridas por caso):",
        space_after=3
    )

    tbl_bench = doc.add_table(rows=1, cols=6)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_bench.autofit = False

    encabezados_b = ["Tamaño (N)", "Bubble Sort (µs)", "Bubble Sort (ms)", "Merge Sort (µs)", "Merge Sort (ms)", "Diferencia de Rendimiento"]
    anchos_b = [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.3)]

    hdr_b = tbl_bench.rows[0]
    set_table_header(hdr_b)
    prevent_row_split(hdr_b)
    for idx, nombre in enumerate(encabezados_b):
        cell = hdr_b.cells[idx]
        cell.width = anchos_b[idx]
        set_cell_background(cell, "EAEAEA")
        set_cell_margins(cell, top=20, bottom=20, left=25, right=25)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(nombre)
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)
        r.bold = True

    datos_b = [
        ("N = 10", "0.90 µs", "0.0009 ms", "1.00 µs", "0.0010 ms", "Empate técnico (0.9x)"),
        ("N = 100", "117.50 µs", "0.1175 ms", "38.50 µs", "0.0385 ms", "Merge 3.05x más rápido"),
        ("N = 1 000", "12 333.00 µs", "12.33 ms", "650.00 µs", "0.65 ms", "Merge 18.97x más rápido"),
        ("N = 10 000", "1 309 150.00 µs", "1 309.15 ms", "5 857.00 µs", "5.86 ms", "Merge 223.51x más rápido")
    ]

    for f_idx, fila in enumerate(datos_b):
        row = tbl_bench.add_row()
        prevent_row_split(row)
        color = "F9F9F9" if f_idx % 2 == 0 else "FFFFFF"
        for c_idx, val in enumerate(fila):
            cell = row.cells[c_idx]
            cell.width = anchos_b[c_idx]
            set_cell_background(cell, color)
            set_cell_margins(cell, top=16, bottom=16, left=25, right=25)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(val)
            r.font.name = 'Arial'
            r.font.size = Pt(8.0)
            if c_idx == 5:
                r.bold = True

    # Gráfico embebido de curva benchmark personalizado (ancho calibrado a 3.8 in para que todo el análisis entre perfectamente)
    if os.path.exists(ruta_grafico):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(3)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.paragraph_format.keep_with_next = True
        doc.add_picture(ruta_grafico, width=Inches(3.75))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(2)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run("Figura 1: Curva de crecimiento en escala logarítmica comparando Bubble Sort y Merge Sort.")
        r_cap.font.name = 'Arial'
        r_cap.font.size = Pt(8.0)
        r_cap.italic = True

    agregar_p(
        "Análisis de resultados:\n"
        "• Con N = 10, los dos algoritmos tardan casi lo mismo (0.9 µs vs 1.0 µs). Bubble Sort fue una fracción más rápido "
        "porque trabaja sobre el mismo arreglo sin llamadas a funciones recursivas ni reserva de memoria para la mezcla.\n"
        "• Con N = 100, Merge Sort toma la delantera siendo 3 veces más veloz (38.5 µs frente a 117.5 µs).\n"
        "• Con N = 1 000, la diferencia se vuelve evidente: Merge Sort tarda solo 0.65 ms mientras que Bubble Sort tarda 12.33 ms (casi 19 veces más rápido).\n"
        "• Con N = 10 000, la diferencia es gigantesca: Bubble Sort tarda más de 1.3 segundos (1 309.15 ms), lo que congelaría la pantalla, "
        "mientras que Merge Sort completa todo en menos de 6 milisegundos (5.86 ms), siendo más de 223 veces más rápido.\n"
        "• En cuanto al crecimiento: al multiplicar los datos por 10 (de 1 000 a 10 000), Bubble Sort aumentó su tiempo unas 106 veces "
        "(de 12.33 ms a 1 309.15 ms). En cambio, Merge Sort solo aumentó 9 veces (de 0.65 ms a 5.86 ms), confirmando su comportamiento casi lineal O(n log n).",
        space_after=2
    )

    # SALTO A PÁGINA 5 (PREGUNTAS 1 Y 2)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 5: 5. RESPUESTAS A LAS PREGUNTAS DE ANÁLISIS (PREGUNTAS 1 Y 2)
    # =========================================================================
    agregar_titulo_seccion("5. Respuestas a las preguntas de análisis", space_before=2, space_after=4)

    # Pregunta 1
    agregar_subtitulo("Pregunta 1: Comparación de O(n²) vs. O(n log n), umbral de diferencia y notación asintótica", space_before=4)
    agregar_p(
        "Con pocos datos (N = 10), ambos algoritmos empatan técnicamente en rendimiento (0.9 µs para Bubble Sort y 1.0 µs para Merge Sort). "
        "Para tamaños muy pequeños las pocas operaciones directas de Bubble Sort son tan rápidas que compensan no tener la complejidad de Merge Sort, "
        "el cual gasta tiempo extra llamando funciones recursivas y pidiendo memoria para su arreglo temporal. "
        "La diferencia comienza a notarse claramente a partir de N = 100, donde Merge Sort ya es 3 veces más rápido. Con N = 1 000 ya es 19 veces más veloz, "
        "y con N = 10 000 la brecha es total: Bubble Sort tarda 1.31 segundos y Merge Sort apenas 5.86 milisegundos (más de 223 veces más rápido).\n"
        "Sí coincide plenamente con lo esperado: Bubble Sort es cuadrático O(n²) multiplicando su tiempo por 100 al multiplicar datos por 10 "
        "(en nuestra prueba aumentó 106 veces), mientras que Merge Sort escala como O(n log n) con un crecimiento mucho más suave y eficiente.",
        space_after=6
    )

    # Pregunta 2
    agregar_subtitulo("Pregunta 2: Representación del tablero como lista enlazada de filas y costo de operaciones", space_before=6)
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
        "que estaba arriba, actualizando el puntero origen del tablero. Toma 10 creaciones y unas 30 asignaciones de puntero: costo O(C) (O(1) constante).",
        space_after=4
    )

    # SALTO A PÁGINA 6 (PREGUNTAS 3 Y 4)
    doc.add_page_break()

    # =========================================================================
    # PÁGINA 6: 5. RESPUESTAS A LAS PREGUNTAS DE ANÁLISIS (PREGUNTAS 3 Y 4)
    # =========================================================================
    # Pregunta 3
    agregar_subtitulo("Pregunta 3: Necesidad de la lista doblemente enlazada para el replay y costo de avanzar y retroceder", space_before=2)
    agregar_p(
        "Para implementar las funciones de deshacer y el replay necesitamos movernos en el tiempo en ambas direcciones (hacia adelante y hacia atrás). "
        "En una lista simplemente enlazada cada nodo solo conoce al nodo siguiente. Avanzar en el tiempo es directo (actual = actual->siguiente), pero para "
        "retroceder un solo paso es imposible regresar desde el nodo actual: habría que empezar a buscar desde la cabeza de la lista recorriendo nodo por nodo "
        "hasta encontrar cuál apuntaba al actual. Si la partida lleva k jugadas, cada pulsación para retroceder tomaría O(k) operaciones, lo que causaría "
        "congelamientos y tirones de pantalla. La lista doblemente enlazada resuelve esto porque cada nodo guarda tanto su puntero siguiente como su puntero anterior.\n"
        "• Costo de avanzar un paso (historial.avanzar() / Tecla Y o botón Replay Adelante): Solo hace actual = actual->siguiente. Toma O(1) operaciones elementales.\n"
        "• Costo de retroceder un paso (historial.retroceder() / Tecla Z o botón Replay Atrás): Solo hace actual = actual->anterior. Toma O(1) operaciones elementales.",
        space_after=6
    )

    # Pregunta 4
    agregar_subtitulo("Pregunta 4: Garantía del evento más próximo al frente y costo de inserción en la cola de eventos", space_before=8)
    agregar_p(
        "Para la cola de eventos hicimos una estructura que se mantiene ordenada por tiempo. Cada vez que metemos un evento nuevo, se inserta y se va "
        "comparando con los elementos anteriores para acomodarse en su posición correcta según el segundo exacto en el que tiene que activarse. "
        "De esta forma, el evento que tiene que ocurrir más pronto siempre queda de primero (en la posición 0). Para revisar si ya le toca activarse, "
        "el juego solo tiene que consultar ese primer elemento en O(1). Insertar un evento nuevo solo toma O(log n) operaciones porque se va dividiendo "
        "a la mitad en cada paso, lo cual es muy rápido y evita tener que ordenar toda la lista desde cero cada vez."
    )

    # Guardar Word
    doc.save(ruta_docx)
    print(f"Documento Word guardado en: {ruta_docx}")

# =============================================================
# EXPORTAR WORD A PDF MEDIANTE MICROSOFT WORD COM
# =============================================================
def exportar_word_a_pdf(ruta_docx, ruta_pdf):
    ps_script = f'''
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    try {{
        $doc = $word.Documents.Open("{ruta_docx}")
        $doc.SaveAs([ref]"{ruta_pdf}", [ref]17)
        $doc.Close()
        Write-Host "Exportacion exitosa de PDF mediante Word"
    }} catch {{
        Write-Host "Error al exportar: " $_
    }} finally {{
        $word.Quit()
    }}
    '''
    ps_file = os.path.join(os.path.dirname(ruta_docx), "scratch", "export_pdf.ps1")
    with open(ps_file, "w", encoding="utf-8") as f:
        f.write(ps_script)

    result = subprocess.run(
        ["powershell", "-ExecutionPolicy", "Bypass", "-File", ps_file],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print("Stderr:", result.stderr)

if __name__ == '__main__':
    base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    logo = os.path.join(base, "scratch", "image1.png")
    grafico = os.path.join(base, "scratch", "benchmark_curva_pro.png")
    docx_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.docx")
    pdf_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.pdf")

    generar_documento_word(logo, grafico, docx_path)
    exportar_word_a_pdf(docx_path, pdf_path)
