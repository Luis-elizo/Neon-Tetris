import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def generar_pdf(ruta_grafico, ruta_pdf):
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    estilo_inst = ParagraphStyle(
        'Institucional',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#8B1E2D')
    )
    estilo_sub_inst = ParagraphStyle(
        'SubInstitucional',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#2C3E50')
    )
    estilo_tit = ParagraphStyle(
        'TituloProyecto',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1A252F')
    )
    estilo_sec = ParagraphStyle(
        'Seccion',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#8B1E2D'),
        spaceBefore=10,
        spaceAfter=4
    )
    estilo_cuerpo = ParagraphStyle(
        'Cuerpo',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#222222')
    )
    estilo_bullet = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11,
        leftIndent=15,
        firstLineIndent=-10,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor('#222222')
    )
    estilo_tabla = ParagraphStyle(
        'CeldaTabla',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        alignment=TA_LEFT
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
    estilo_pregunta = ParagraphStyle(
        'Pregunta',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor('#2C3E50'),
        spaceBefore=6,
        spaceAfter=3
    )

    story = []

    # Encabezado
    story.append(Paragraph("UNIVERSIDAD NACIONAL DE COSTA RICA", estilo_inst))
    story.append(Paragraph("SEDE REGIONAL BRUNCA — CAMPUS PÉREZ ZELEDÓN Y COTO<br/>ESCUELA DE INFORMÁTICA | CURSO EIF207: ESTRUCTURAS DE DATOS (II CICLO 2026)", estilo_sub_inst))
    story.append(Spacer(1, 4))
    story.append(Paragraph("PROYECTO I: NEON TETRIS<br/><font size=10>Implementación con Estructuras de Datos Lineales Dinámicas Propias</font>", estilo_tit))
    story.append(Spacer(1, 6))

    # Tabla Info Estudiante
    info_data = [
        [
            Paragraph("<b>Estudiante:</b> Luis Andrés Elizondo Hernández", estilo_tabla),
            Paragraph("<b>Entorno:</b> ZinjaI / MinGW GCC (C++14)", estilo_tabla)
        ],
        [
            Paragraph("<b>Curso:</b> EIF207 Estructuras de Datos (15%)", estilo_tabla),
            Paragraph("<b>Librería Gráfica:</b> Raylib (C++ Nativo)", estilo_tabla)
        ]
    ]
    t_info = Table(info_data, colWidths=[265, 265])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D5DBDB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E8E8')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_info)
    story.append(Spacer(1, 6))

    # 1. Introducción
    story.append(Paragraph("1. Introducción y Descripción del Sistema", estilo_sec))
    story.append(Paragraph(
        "El presente proyecto consiste en el desarrollo de un videojuego funcional basado en Tetris (\"Neon Tetris\") en lenguaje C++. "
        "La premisa académica central es la prohibición estricta de la biblioteca estándar de plantillas (STL: std::vector, std::queue, "
        "std::stack, std::list, std::priority_queue), requiriendo el modelado manual de todas las estructuras lineales mediante punteros explícitos "
        "y asignación dinámica de memoria.<br/>"
        "El sistema integra seis estructuras lineales: <b>Cola FIFO</b> (piezas futuras con bolsa de 7 mediante Fisher-Yates), <b>Pila LIFO</b> "
        "(reserva unitaria de Hold), <b>Lista Doblemente Enlazada</b> (historial bidireccional para Deshacer multi-paso, Rehacer y Replay), "
        "<b>Cola de Prioridad Min-Heap</b> (programación de eventos temporales), <b>Matriz Ortogonal / Lista de Filas</b> (tablero dinámico) "
        "y <b>Algoritmos Propios de Ordenamiento</b> (Burbuja y Merge Sort) para clasificar mejores puntajes persistidos en JSON.",
        estilo_cuerpo
    ))

    # 2. Arquitectura
    story.append(Paragraph("2. Arquitectura del Sistema y Relación entre Estructuras", estilo_sec))
    story.append(Paragraph(
        "La arquitectura sigue un modelo en tres capas: <b>Estructuras</b> (punteros y memoria), <b>Lógica</b> (tetrominós, rotación fija sin wall-kicks, colisiones y ordenamientos) "
        "e <b>Interfaz de Usuario</b> (pantallas en Raylib). Las estructuras se articulan del siguiente modo:<br/>"
        "• <b>Cola FIFO (Piezas Futuras):</b> Abastece piezas continuas. Al vaciarse, LlenarBolsa() genera los 7 tetrominós y los baraja en O(n) con Fisher-Yates. Se desencola la pieza en juego y la UI consulta obtenerEn(k) para mostrar 3 piezas siguientes.<br/>"
        "• <b>Pila LIFO (Hold):</b> Al pulsar Shift Derecho, intercambia la pieza activa con el tope en O(1). Si la pila está vacía, apila la actual y extrae una nueva de la Cola FIFO (máximo 1 swap por turno).<br/>"
        "• <b>Tablero (Lista de Filas):</b> Red ortogonal 20x10. Tras la fijación y un flash visual de 250 ms, limpiarLineas() desvincula nodos de filas completas e inserta filas vacías al inicio en O(C).<br/>"
        "• <b>Lista Doble (Historial / Replay):</b> Captura estados (matriz 20x10 y puntaje). En partida, las teclas Z (Undo) e Y (Redo) mueven el puntero actual en O(1). En Game Over, el Replay reproduce paso a paso o en autoplay cada 0.5 s.<br/>"
        "• <b>Cola de Prioridad (Min-Heap):</b> Mantiene eventos programados ordenados por timestamp (Fiebre de Velocidad, Terremoto/Basura y Bonus). Al vencer el tiempo de la raíz O(1), se extrae en O(log n) y se aplica el efecto.<br/>"
        "• <b>Persistencia y Ranking:</b> Lee/escribe scores.json. La pantalla de clasificación permite alternar Bubble Sort O(n²) o Merge Sort O(n log n) para ordenar los puntajes y comparar tiempos en microsegundos.",
        estilo_cuerpo
    ))

    # 3. Complejidad
    story.append(Paragraph("3. Complejidad Teórica Asintótica (Notación Big-O)", estilo_sec))
    comp_headers = [
        Paragraph("Estructura", estilo_tabla_hdr),
        Paragraph("Operación", estilo_tabla_hdr),
        Paragraph("Mejor", estilo_tabla_hdr),
        Paragraph("Prom.", estilo_tabla_hdr),
        Paragraph("Peor", estilo_tabla_hdr),
        Paragraph("Espacio", estilo_tabla_hdr),
        Paragraph("Justificación Breve", estilo_tabla_hdr)
    ]
    comp_rows = [
        comp_headers,
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Inserción directa en puntero ultimo.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Extracción en primero y liberación de memoria.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("obtenerEn(k)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(k)", estilo_tabla), Paragraph("O(n)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Recorrido secuencial hasta el índice k.", estilo_tabla)],
        [Paragraph("Pila LIFO", estilo_tabla), Paragraph("apilar / desapilar", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Acceso y modificación en el puntero tope.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("agregarEstado()", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(F*C)", estilo_tabla), Paragraph("Inserción al final; clona matriz 20x10.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("retroceder [Undo]", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Transición de puntero: actual = actual->anterior.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("avanzar [Redo]", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Transición de puntero: actual = actual->siguiente.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(log n)", estilo_tabla), Paragraph("O(log n)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Flotación ascendente (sift-up) en montículo.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(log n)", estilo_tabla), Paragraph("O(log n)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Hundimiento (sift-down) restaurando montículo.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("verTiempoFrente()", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Acceso directo indexado a la raíz arreglo[0].", estilo_tabla)],
        [Paragraph("Tablero", estilo_tabla), Paragraph("limpiarLineas()", estilo_tabla), Paragraph("O(F*C)", estilo_tabla), Paragraph("O(F*C)", estilo_tabla), Paragraph("O(F*C)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Desconecta nodos de filas llenas; inserta al tope.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Bubble Sort", estilo_tabla), Paragraph("O(n)", estilo_tabla), Paragraph("O(n²)", estilo_tabla), Paragraph("O(n²)", estilo_tabla), Paragraph("O(1)", estilo_tabla), Paragraph("Intercambios contiguos adyacentes.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Merge Sort", estilo_tabla), Paragraph("O(n log n)", estilo_tabla), Paragraph("O(n log n)", estilo_tabla), Paragraph("O(n log n)", estilo_tabla), Paragraph("O(n)", estilo_tabla), Paragraph("División recursiva y mezcla lineal en buffer temporal.", estilo_tabla)]
    ]
    t_comp = Table(comp_rows, colWidths=[65, 80, 42, 45, 45, 42, 211])
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

    # 4. Benchmark
    story.append(Paragraph("4. Comparación Empírica y Benchmark (Burbuja vs. Merge Sort)", estilo_sec))
    story.append(Paragraph(
        "Se evaluaron experimentalmente Bubble Sort y Merge Sort mediante std::chrono::high_resolution_clock en C++ "
        "(5 repeticiones independientes con permutaciones aleatorias de registros Jugador con puntajes entre 0 y 100 000).",
        estilo_cuerpo
    ))
    bench_headers = [
        Paragraph("Tamaño (N)", estilo_tabla_hdr),
        Paragraph("Bubble Sort (µs)", estilo_tabla_hdr),
        Paragraph("Bubble Sort (ms)", estilo_tabla_hdr),
        Paragraph("Merge Sort (µs)", estilo_tabla_hdr),
        Paragraph("Merge Sort (ms)", estilo_tabla_hdr),
        Paragraph("Factor Aceleración", estilo_tabla_hdr)
    ]
    bench_rows = [
        bench_headers,
        [Paragraph("N = 10", estilo_tabla), Paragraph("0.90 µs", estilo_tabla), Paragraph("0.0009 ms", estilo_tabla), Paragraph("1.00 µs", estilo_tabla), Paragraph("0.0010 ms", estilo_tabla), Paragraph("<b>0.90x (Empate)</b>", estilo_tabla)],
        [Paragraph("N = 100", estilo_tabla), Paragraph("117.50 µs", estilo_tabla), Paragraph("0.1175 ms", estilo_tabla), Paragraph("38.50 µs", estilo_tabla), Paragraph("0.0385 ms", estilo_tabla), Paragraph("<b>3.05x más rápido</b>", estilo_tabla)],
        [Paragraph("N = 1 000", estilo_tabla), Paragraph("12 333.00 µs", estilo_tabla), Paragraph("12.33 ms", estilo_tabla), Paragraph("650.00 µs", estilo_tabla), Paragraph("0.65 ms", estilo_tabla), Paragraph("<b>18.97x más rápido</b>", estilo_tabla)],
        [Paragraph("N = 10 000", estilo_tabla), Paragraph("1 309 150.00 µs", estilo_tabla), Paragraph("1 309.15 ms", estilo_tabla), Paragraph("5 857.00 µs", estilo_tabla), Paragraph("5.86 ms", estilo_tabla), Paragraph("<b>223.51x más rápido</b>", estilo_tabla)]
    ]
    t_bench = Table(bench_rows, colWidths=[75, 90, 90, 85, 85, 105])
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

    # Imagen del gráfico
    if os.path.exists(ruta_grafico):
        img_w = 510
        img_h = 510 * (560 / 1000)
        story.append(Image(ruta_grafico, width=img_w, height=img_h))
        story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Análisis de Escalamiento:</b> Al multiplicar N por 10 (de 1 000 a 10 000), Bubble Sort aumentó su tiempo por un factor de <b>106.1x</b> "
        "(de 12.33 ms a 1 309.15 ms), correlacionando estrechamente con la predicción teórica cuadrática (10² = 100x). Merge Sort creció por un "
        "factor de apenas <b>9.0x</b> (de 0.65 ms a 5.86 ms), cumpliendo holgadamente la cota O(n log n) teórica (~13.3x).",
        estilo_cuerpo
    ))

    # 5. Preguntas de Análisis
    story.append(Paragraph("5. Respuestas a las Preguntas de Análisis Obligatorias (Sección 7)", estilo_sec))

    # P1
    story.append(Paragraph("Pregunta 1: Comparación de O(n²) vs. O(n log n), umbral de divergencia y notación asintótica", estilo_pregunta))
    story.append(Paragraph(
        "<b>1. Umbral visible:</b> Para N = 10 existe un empate técnico (0.9 µs Bubble vs. 1.0 µs Merge) debido a que Bubble Sort opera in-place sin sobrecostos por llamadas recursivas ni asignación de buffers auxiliares. La diferencia se vuelve evidente a partir de N = 100 (Merge Sort es 3x más rápido: 38.5 µs vs. 117.5 µs), se consolida en N = 1 000 (19x: 0.65 ms vs. 12.33 ms) y resulta abrumadora en N = 10 000, donde Bubble Sort tarda 1.31 s (congelando la pantalla) mientras Merge Sort finaliza en 5.86 ms (aceleración superior a <b>223x</b>).<br/>"
        "<b>2. Concordancia asintótica:</b> La coincidencia es matemática: Bubble Sort escala como T(n) ≈ c₁·n² (crece ~100x ante aumentos de factor 10), mientras que Merge Sort sigue T(n) ≈ c₂·n·log₂(n), escalando de forma casi lineal.",
        estilo_cuerpo
    ))

    # P2
    story.append(Paragraph("Pregunta 2: Representación del tablero como lista enlazada de filas y costo de operaciones", estilo_pregunta))
    story.append(Paragraph(
        "<b>1. Justificación:</b> En un arreglo estático contiguo (int tablero[20][10]), eliminar una fila completa intermedia exige copiar en bucle todos los bloques superiores una fila hacia abajo (hasta 190 copias de memoria). Al modelar el tablero como una lista enlazada de filas (matriz ortogonal de celdas), las filas superiores <b>no se desplazan en memoria</b>: simplemente se desconectan los punteros verticales arriba y abajo de la fila eliminada y se reconecta la fila superior con la inferior. Las filas superiores 'caen' instantáneamente al quedar re-enlazadas.<br/>"
        "<b>2. Costo operativo:</b><br/>"
        "• <i>Eliminar fila completa:</i> Se recorren las C = 10 columnas desconectando enlaces arriba/abajo y liberando memoria con delete. Toma exactamente 10 liberaciones y 20 reasignaciones de puntero: costo <b>O(C)</b> (tiempo constante O(1) con C = 10 fijo).<br/>"
        "• <i>Insertar fila vacía al tope:</i> Se instancian 10 celdas vacías con new, se enlazan horizontalmente y se conectan sus punteros abajo a la fila superior existente. Toma 10 news y 30 asignaciones de puntero: costo <b>O(C)</b> (tiempo constante O(1)).",
        estilo_cuerpo
    ))

    # P3
    story.append(Paragraph("Pregunta 3: Necesidad de lista doblemente enlazada para Replay y costo de paso", estilo_pregunta))
    story.append(Paragraph(
        "<b>1. Justificación frente a lista simple:</b> La navegación de jugadas requiere bidireccionalidad simétrica. En una lista simplemente enlazada sólo se tiene el puntero siguiente. Si bien avanzar es trivial, retroceder un paso desde el nodo actual es imposible de forma local: requeriría recorrer desde la cabeza toda la lista hasta localizar el nodo cuyo siguiente == actual, incurriendo en un costo <b>O(k)</b> en cada retroceso (donde k es el turno actual). En una partida larga esto deteriora los 60 FPS. La lista doblemente enlazada resuelve esto incluyendo el puntero anterior en cada NodoHistorial, posibilitando retroceso local instantáneo.<br/>"
        "<b>2. Costo operativo:</b><br/>"
        "• <i>Avanzar (historial.avanzar() / Tecla Y):</i> Verifica actual->siguiente != nullptr y ejecuta actual = actual->siguiente. Costo: <b>O(1)</b> operaciones elementales.<br/>"
        "• <i>Retroceder (historial.retroceder() / Tecla Z):</i> Verifica actual->anterior != nullptr y ejecuta actual = actual->anterior. Costo: <b>O(1)</b> operaciones elementales.",
        estilo_cuerpo
    ))

    # P4
    story.append(Paragraph("Pregunta 4: Garantía de elemento más próximo en cola de eventos y costo de inserción", estilo_pregunta))
    story.append(Paragraph(
        "<b>1. Garantía del frente (Min-Heap):</b> ColaPrioridad implementa un Montículo Binario Mínimo sobre un arreglo dinámico propio (NodoEvento*). Mantiene el invariante: arreglo[i].tiempoDisparo <= arreglo[2i+1].tiempoDisparo y arreglo[i].tiempoDisparo <= arreglo[2i+2].tiempoDisparo. Por inducción, la raíz (índice 0) contiene de forma permanente el evento con el menor tiempo de disparo de todo el sistema. Consultar el próximo evento con verTiempoFrente() toma <b>O(1)</b> tiempo constante.<br/>"
        "<b>2. Costo de inserción (encolar()):</b> El nuevo evento se ubica al final del montículo (índice k = tamano) y flota hacia arriba (sift-up) comparándose e intercambiándose con su padre en floor((k-1)/2). Como la altura del árbol binario es h = floor(log₂ n), realiza a lo sumo log₂ n pasos. Costo: <b>O(log n)</b> en peor y caso promedio, y O(1) en mejor caso. Cumple la restricción estricta de no insertar al final y reordenar todo con O(n log n).",
        estilo_cuerpo
    ))

    # 6. Conclusiones
    story.append(Paragraph("6. Conclusiones", estilo_sec))
    story.append(Paragraph(
        "1. <b>Adecuación de TADs:</b> Cada mecánica del juego se resolvió naturalmente con su estructura óptima: Cola FIFO para la rotación de bolsas; Pila LIFO para la reserva unitaria; Lista Doble para el historial reversible simétrico; y Min-Heap para despachar eventos temporales con mínimo consumo de CPU.<br/>"
        "2. <b>Control Riguroso de Memoria:</b> La ausencia de STL garantizó que cada new tenga su contraparte delete en destructores y extracciones, logrando un aplicativo libre de fugas de memoria verificado bajo compilación limpia con MinGW GCC.<br/>"
        "3. <b>Comprobación Empírica de la Teoría Asintótica:</b> Para N = 10 000, la reducción de tiempo de 1.31 s (Burbuja) a 5.86 ms (Merge Sort) demostró que el diseño algorítmico asintótico es indispensable para el rendimiento interactivo en tiempo real.",
        estilo_cuerpo
    ))

    doc.build(story)
    print(f"Documento PDF generado exitosamente en: {ruta_pdf}")

if __name__ == '__main__':
    directorio_base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    ruta_grafico = os.path.join(directorio_base, "scratch", "benchmark_chart.png")
    ruta_pdf = os.path.join(directorio_base, "INFORME_PROYECTO1_EIF207.pdf")
    generar_pdf(ruta_grafico, ruta_pdf)
