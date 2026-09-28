import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT

def generar_pdf_normal(ruta_grafico, ruta_pdf):
    doc = SimpleDocTemplate(
        ruta_pdf,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    estilo_portada_bold = ParagraphStyle(
        'PortadaBold',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    estilo_portada = ParagraphStyle(
        'Portada',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    estilo_titulo = ParagraphStyle(
        'TituloSeccion',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceBefore=14,
        spaceAfter=10
    )
    estilo_subtitulo = ParagraphStyle(
        'Subtitulo',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=4
    )
    estilo_cuerpo = ParagraphStyle(
        'Cuerpo',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10.5,
        leading=14.5,
        alignment=TA_JUSTIFY,
        textColor=colors.black,
        spaceAfter=6
    )
    estilo_tabla = ParagraphStyle(
        'CeldaTabla',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=TA_LEFT
    )
    estilo_tabla_center = ParagraphStyle(
        'CeldaTablaCenter',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER
    )
    estilo_tabla_hdr = ParagraphStyle(
        'CeldaTablaHdr',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    story = []

    # ------------------ PORTADA ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("Sede Regional Brunca", estilo_portada_bold))
    story.append(Paragraph("Campus Pérez Zeledón", estilo_portada))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Curso: EIF207 Estructuras de Datos", estilo_portada))
    story.append(Paragraph("Proyecto 1: Neon Tetris", estilo_portada_bold))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Estudiante:", estilo_portada))
    story.append(Paragraph("Luis Andres Elizondo Hernandez", estilo_portada))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Profesor: [Nombre del profesor]", estilo_portada))
    story.append(Paragraph("II Ciclo 2026", estilo_portada))
    story.append(Spacer(1, 40))
    story.append(Paragraph("27 de septiembre del 2026", estilo_portada))
    story.append(PageBreak())

    # ------------------ INTRODUCCIÓN ------------------
    story.append(Paragraph("Introducción", estilo_titulo))
    story.append(Paragraph(
        "En este primer proyecto del curso de Estructuras de Datos desarrollamos una versión funcional del juego clásico Tetris, "
        "llamada \"Neon Tetris\", programada en C++ y utilizando la biblioteca gráfica Raylib. El propósito principal del proyecto "
        "fue aplicar de forma práctica las estructuras de datos lineales que estudiamos en las primeras semanas del ciclo (pilas, colas, "
        "listas enlazadas, colas de prioridad y algoritmos de ordenamiento), pero con la condición indispensable de implementarlas "
        "desde cero mediante nodos, punteros y memoria dinámica, sin usar ninguna de las estructuras de la biblioteca estándar (STL).",
        estilo_cuerpo
    ))
    story.append(Paragraph(
        "Cada una de las mecánicas que tiene el juego está conectada directamente con una estructura de datos específica. Por ejemplo, "
        "la fila de piezas que van a salir se maneja con una cola; la mecánica de guardar una pieza para después (hold) se resuelve con una pila; "
        "el historial que permite deshacer jugadas y ver el replay usa una lista doblemente enlazada; los eventos aleatorios que modifican la "
        "partida usan una cola de prioridad basada en un montículo (heap); y el tablero del juego se representa como una lista enlazada de filas. "
        "Además, implementamos dos métodos de ordenamiento (Burbuja y Merge Sort) para organizar la tabla de mejores puntajes y comparamos sus "
        "tiempos de ejecución reales para ver si coincidían con la teoría de complejidad asintótica.",
        estilo_cuerpo
    ))
    story.append(Paragraph(
        "En este informe explicamos la arquitectura y la relación entre todas estas estructuras, detallamos la complejidad de cada operación "
        "implementada, presentamos las pruebas de rendimiento con sus gráficos y respondemos a las preguntas de análisis requeridas.",
        estilo_cuerpo
    ))

    # ------------------ DESARROLLO ------------------
    story.append(Paragraph("Desarrollo", estilo_titulo))

    story.append(Paragraph("1. Descripción del juego y arquitectura general", estilo_subtitulo))
    story.append(Paragraph(
        "El juego sigue la lógica básica de Tetris en un tablero de 10 columnas por 20 filas. Las piezas caen de forma constante y el jugador "
        "puede moverlas hacia los lados, rotarlas y acelerar su caída. Cuando se completa una línea horizontal, esta se limpia, sumando puntos "
        "y haciendo que los bloques superiores desciendan. Si los bloques acumulados llegan arriba y una nueva pieza no puede entrar, la partida "
        "termina (Game Over).<br/>"
        "Para mantener el código ordenado y fácil de mantener, organizamos el proyecto en tres carpetas principales:<br/>"
        "• <b>estructuras:</b> Contiene las clases de las estructuras de datos hechas a mano con sus nodos y punteros (Cola, Pila, ListaDoble, "
        "ColaPrioridad, Tablero y ManejadorJSON).<br/>"
        "• <b>logica:</b> Contiene la definición de las piezas con sus rotaciones (Pieza) y las funciones de ordenamiento (ordenamientos).<br/>"
        "• <b>ui:</b> Maneja las distintas pantallas del juego (Menú principal, Pantalla de juego, Pausa, Game Over y Ranking) junto con los colores neón.",
        estilo_cuerpo
    ))

    story.append(Paragraph("2. Relación y funcionamiento de las estructuras de datos", estilo_subtitulo))
    story.append(Paragraph(
        "En lugar de ver las estructuras como elementos aislados, cada una cumple un rol esencial dentro del ciclo de juego en main.cpp:<br/>"
        "• <b>Cola de piezas futuras (Cola):</b> En Tetris las piezas no deben salir completamente al azar porque podrían repetirse muchas veces la misma o pasar mucho tiempo "
        "sin que salga una pieza larga (la I). Por eso se usa el sistema de \"bolsa de 7\": se toman las 7 piezas clásicas, se mezclan aleatoriamente "
        "con el algoritmo de Fisher-Yates y se meten a la cola. Conforme el jugador va jugando, se van sacando con desencolar() y en pantalla se muestran "
        "las siguientes 3 piezas mirando los primeros nodos de la cola. Cuando la cola se vacía, se genera otra bolsa de 7 y se vuelve a llenar.<br/>"
        "• <b>Pila para la pieza en espera (Pila):</b> La mecánica de \"Hold\" permite guardar la pieza actual para usarla en otro momento. Esto lo modelamos con una pila de capacidad 1. "
        "Si la pila está vacía y el jugador presiona Shift, la pieza actual se mete a la pila y se saca una nueva de la cola de piezas. Si ya había una pieza "
        "guardada, se intercambian: se desapila la que estaba guardada para pasarla al juego y se apila la que estaba cayendo. Para que el jugador no abuse "
        "de esto, solo se permite un cambio por turno hasta que la pieza caiga y se fije en el tablero.<br/>"
        "• <b>Tablero como lista de filas (Tablero):</b> El tablero de 20x10 no es un simple arreglo estático bidimensional, sino una estructura de filas y celdas enlazadas mediante punteros en "
        "cuatro direcciones (arriba, abajo, izquierda, derecha). Cuando se llena una fila, no hay que copiar todos los números de arriba para bajarlos: "
        "simplemente se desenganchan los punteros de la fila llena, se liberan sus nodos con delete, se conectan los vecinos y se crea una fila vacía "
        "nueva arriba en el tope.<br/>"
        "• <b>Lista doblemente enlazada para historial y replay (ListaDoble):</b> Cada vez que una pieza se coloca en el tablero o se limpian líneas, se guarda una copia del tablero y del puntaje en un nodo de la lista doble. "
        "Como cada nodo tiene punteros siguiente y anterior, durante la partida el jugador puede presionar la tecla Z para deshacer jugadas (retroceder en el "
        "historial) o la tecla Y para rehacerlas (avanzar en el historial). Cuando la partida termina en Game Over, esta misma lista sirve para el modo Replay, "
        "donde se puede volver a ver toda la partida paso a paso o en reproducción automática.<br/>"
        "• <b>Cola de prioridad para eventos programados (ColaPrioridad):</b> Para hacer el juego más dinámico, programamos eventos que ocurren cada cierto tiempo: un aumento temporal de velocidad (\"Fiebre de velocidad\"), "
        "una línea de basura que sube desde el fondo (\"Terremoto\") o un bono de +500 puntos. Estos eventos se guardan en una cola de prioridad implementada "
        "como un montículo mínimo (Min-Heap), donde la prioridad es la marca de tiempo (timestamp) en la que deben ocurrir. De esta forma, el evento que tiene "
        "que ejecutarse más pronto siempre queda en la raíz (al frente), y cuando el tiempo de la partida llega a esa marca, se saca y se aplica su efecto.<br/>"
        "• <b>Persistencia y ordenamiento de puntajes:</b> Los mejores puntajes se guardan en un archivo scores.json. Desde el menú de Ranking, el jugador puede ver la lista de récords ordenada "
        "de mayor a menor y puede elegir si quiere ordenarla usando Bubble Sort o Merge Sort, viendo en pantalla cuántos microsegundos tardó cada algoritmo.",
        estilo_cuerpo
    ))

    story.append(Paragraph("3. Análisis de complejidad teórica (Notación Big-O)", estilo_subtitulo))
    story.append(Paragraph("En la siguiente tabla resumimos la complejidad teórica de las operaciones principales de las estructuras implementadas en el proyecto:", estilo_cuerpo))

    # Tabla Complejidad
    filas_c = [
        [Paragraph("<b>Estructura</b>", estilo_tabla_hdr), Paragraph("<b>Operación</b>", estilo_tabla_hdr), Paragraph("<b>Mejor</b>", estilo_tabla_hdr), Paragraph("<b>Prom.</b>", estilo_tabla_hdr), Paragraph("<b>Peor</b>", estilo_tabla_hdr), Paragraph("<b>Espacio</b>", estilo_tabla_hdr), Paragraph("<b>Descripción breve</b>", estilo_tabla_hdr)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta directo al final usando puntero ultimo.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Saca del frente y libera la memoria con delete.", estilo_tabla)],
        [Paragraph("Cola FIFO", estilo_tabla), Paragraph("obtenerEn(k)", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(k)", estilo_tabla_center), Paragraph("O(n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Recorre hasta la posición k para ver piezas futuras.", estilo_tabla)],
        [Paragraph("Pila LIFO", estilo_tabla), Paragraph("apilar / desapilar", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Modifica directamente el nodo que está en el tope.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("agregarEstado()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("Agrega al final; copia la matriz de 20x10.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("retroceder [Undo]", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Mueve el puntero: actual = actual->anterior.", estilo_tabla)],
        [Paragraph("Lista Doble", estilo_tabla), Paragraph("avanzar [Redo]", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Mueve el puntero: actual = actual->siguiente.", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("encolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Inserta al final y flota hacia arriba (sift-up).", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("desencolar()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(log n)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Saca la raíz y reacomoda hacia abajo (sift-down).", estilo_tabla)],
        [Paragraph("Cola Prioridad", estilo_tabla), Paragraph("verTiempoFrente()", estilo_tabla), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Accede directo a la raíz arreglo[0].", estilo_tabla)],
        [Paragraph("Tablero", estilo_tabla), Paragraph("limpiarLineas()", estilo_tabla), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(F*C)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Reconecta punteros de filas llenas y crea nuevas.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Bubble Sort", estilo_tabla), Paragraph("O(n)", estilo_tabla_center), Paragraph("O(n²)", estilo_tabla_center), Paragraph("O(n²)", estilo_tabla_center), Paragraph("O(1)", estilo_tabla_center), Paragraph("Compara e intercambia elementos vecinos.", estilo_tabla)],
        [Paragraph("Ordenamiento", estilo_tabla), Paragraph("Merge Sort", estilo_tabla), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n log n)", estilo_tabla_center), Paragraph("O(n)", estilo_tabla_center), Paragraph("Divide recursivamente y mezcla sub-arreglos.", estilo_tabla)]
    ]
    t_c = Table(filas_c, colWidths=[65, 80, 40, 44, 44, 42, 189])
    t_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EAEAEA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#DDDDDD')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F9F9F9'), colors.white]),
    ]))
    story.append(t_c)
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Comparación empírica y pruebas de rendimiento", estilo_subtitulo))
    story.append(Paragraph(
        "Para comparar el rendimiento real de Bubble Sort (O(n²)) contra Merge Sort (O(n log n)), realizamos un benchmark con la librería "
        "<chrono> de C++, midiendo el tiempo de ejecución en microsegundos (µs). Probamos con arreglos aleatorios de 10, 100, 1 000 y 10 000 "
        "registros con nombres sintéticos y puntajes al azar, promediando 5 repeticiones por cada tamaño para asegurar datos representativos.",
        estilo_cuerpo
    ))

    # Tabla Benchmark
    filas_b = [
        [Paragraph("<b>Tamaño (N)</b>", estilo_tabla_hdr), Paragraph("<b>Bubble Sort (µs)</b>", estilo_tabla_hdr), Paragraph("<b>Bubble Sort (ms)</b>", estilo_tabla_hdr), Paragraph("<b>Merge Sort (µs)</b>", estilo_tabla_hdr), Paragraph("<b>Merge Sort (ms)</b>", estilo_tabla_hdr), Paragraph("<b>Diferencia</b>", estilo_tabla_hdr)],
        [Paragraph("N = 10", estilo_tabla_center), Paragraph("0.90 µs", estilo_tabla_center), Paragraph("0.0009 ms", estilo_tabla_center), Paragraph("1.00 µs", estilo_tabla_center), Paragraph("0.0010 ms", estilo_tabla_center), Paragraph("Empate técnico (0.9x)", estilo_tabla_center)],
        [Paragraph("N = 100", estilo_tabla_center), Paragraph("117.50 µs", estilo_tabla_center), Paragraph("0.1175 ms", estilo_tabla_center), Paragraph("38.50 µs", estilo_tabla_center), Paragraph("0.0385 ms", estilo_tabla_center), Paragraph("Merge 3x más rápido", estilo_tabla_center)],
        [Paragraph("N = 1 000", estilo_tabla_center), Paragraph("12 333.00 µs", estilo_tabla_center), Paragraph("12.33 ms", estilo_tabla_center), Paragraph("650.00 µs", estilo_tabla_center), Paragraph("0.65 ms", estilo_tabla_center), Paragraph("Merge 19x más rápido", estilo_tabla_center)],
        [Paragraph("N = 10 000", estilo_tabla_center), Paragraph("1 309 150.00 µs", estilo_tabla_center), Paragraph("1 309.15 ms", estilo_tabla_center), Paragraph("5 857.00 µs", estilo_tabla_center), Paragraph("5.86 ms", estilo_tabla_center), Paragraph("<b>Merge 223.5x más rápido</b>", estilo_tabla_center)]
    ]
    t_b = Table(filas_b, colWidths=[70, 85, 85, 80, 80, 104])
    t_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EAEAEA')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#BBBBBB')),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#DDDDDD')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#F9F9F9'), colors.white]),
    ]))
    story.append(t_b)
    story.append(Spacer(1, 6))

    if os.path.exists(ruta_grafico):
        story.append(Image(ruta_grafico, width=480, height=480 * (560 / 1000)))
        story.append(Spacer(1, 4))

    story.append(Paragraph(
        "Al analizar los números obtenidos notamos varios puntos importantes:<br/>"
        "• Con N = 10, los dos algoritmos tardan prácticamente lo mismo (0.9 µs vs 1.0 µs). De hecho, Bubble Sort fue una fracción "
        "más rápido porque no tiene que hacer llamadas recursivas ni reservar memoria extra para el arreglo temporal de mezcla.<br/>"
        "• Con N = 100, Merge Sort ya empieza a ganar ventaja y es 3 veces más rápido (38.5 µs frente a 117.5 µs).<br/>"
        "• Con N = 1 000, la diferencia ya es notable: Merge Sort tarda solo 0.65 ms mientras que Bubble Sort tarda 12.33 ms (unas 19 veces más rápido).<br/>"
        "• Con N = 10 000, la diferencia es enorme: Bubble Sort tarda más de 1.3 segundos (1 309.15 ms), lo que en un juego causaría que la pantalla "
        "se congele de forma molesta, mientras que Merge Sort hace todo el trabajo en menos de 6 milisegundos (5.86 ms), siendo más de 223 veces más rápido.<br/>"
        "• Si nos fijamos en cómo crecieron los tiempos de 1 000 a 10 000 (multiplicando los datos por 10), Bubble Sort aumentó su tiempo unas 106 veces "
        "(12.33 ms a 1 309.15 ms), lo cual coincide casi exacto con lo que predice la teoría cuadrática (10² = 100). En cambio, Merge Sort solo aumentó "
        "9 veces (0.65 ms a 5.86 ms), confirmando su comportamiento casi lineal O(n log n).",
        estilo_cuerpo
    ))

    story.append(Paragraph("5. Respuestas a las preguntas obligatorias de la sección 7", estilo_subtitulo))

    # P1
    story.append(Paragraph("<b>Pregunta 1: Compare el tiempo de ordenar la tabla de puntajes con el algoritmo de complejidad O(n²) contra el de O(n log n), para tamaños crecientes de datos de prueba. ¿A partir de qué tamaño se nota la diferencia? ¿Coincide con lo que predice la notación asintótica?</b>", estilo_cuerpo))
    story.append(Paragraph(
        "Con pocos datos (N = 10), los dos algoritmos duran casi lo mismo (0.9 µs y 1.0 µs), porque para arreglos pequeños el costo de las llamadas "
        "recursivas y la memoria dinámica que usa Merge Sort empata el tiempo con las pocas comparaciones directas que hace Bubble Sort. "
        "La diferencia se empieza a notar a partir de N = 100, donde Merge Sort ya es 3 veces más veloz. Ya con N = 1 000 la diferencia es clara (19x), "
        "y en N = 10 000 la diferencia es gigantesca, pues Bubble tarda más de 1.3 segundos y Merge menos de 6 milisegundos (223.5x más rápido).<br/>"
        "Sí coincide totalmente con lo que dice la teoría asintótica: Bubble Sort tiene una complejidad cuadrática O(n²), por lo que al multiplicar "
        "los datos por 10 su tiempo se multiplica por 100 (en nuestras pruebas reales subió 106 veces). Mientras tanto, Merge Sort es O(n log n) y crece "
        "de forma mucho más suave, siendo la opción adecuada para manejar grandes cantidades de datos.",
        estilo_cuerpo
    ))

    # P2
    story.append(Paragraph("<b>Pregunta 2: Explique por qué representar el tablero como una lista enlazada de filas es una forma razonable de modelar la limpieza de líneas, y qué costo (en operaciones) tiene en su implementación insertar una fila vacía y eliminar una fila completa.</b>", estilo_cuerpo))
    story.append(Paragraph(
        "En una matriz común de toda la vida (un arreglo estático de 20x10), cuando una fila se llena en el medio, para hacer que los bloques de arriba "
        "\"caigan\" hay que hacer ciclos que copien fila por fila hacia abajo, moviendo decenas o cientos de números en la memoria. En cambio, al modelar "
        "el tablero como una lista enlazada de filas, las filas de arriba no se tienen que mover de lugar en la memoria. Lo único que se hace es soltar "
        "los punteros de arriba y abajo que estaban conectados a la fila llena, y conectar directamente la fila de arriba con la de abajo. La fila completa "
        "se borra con delete y se inserta una fila vacía nueva en la parte superior conectando sus punteros.<br/>"
        "• <i>Costo de eliminar una fila completa:</i> Como el tablero tiene 10 columnas, se recorren las 10 celdas desconectando sus enlaces verticales y "
        "liberando la memoria. Esto toma exactamente 10 liberaciones y unas 20 reasignaciones de punteros, lo que representa un costo de O(C) operaciones "
        "(tiempo constante O(1) porque las 10 columnas nunca cambian).<br/>"
        "• <i>Costo de insertar una fila vacía:</i> Se crean 10 nodos celda nuevos con new, se enlazan horizontalmente y se conectan sus punteros hacia abajo con "
        "la fila que antes estaba de primera. Esto toma 10 creaciones y unas 30 asignaciones de puntero, teniendo un costo de O(C) operaciones (O(1) constante).",
        estilo_cuerpo
    ))

    # P3
    story.append(Paragraph("<b>Pregunta 3: ¿Por qué el replay requiere una lista doblemente enlazada y no una simplemente enlazada? ¿Qué costo tiene, en su implementación, retroceder o avanzar un paso?</b>", estilo_cuerpo))
    story.append(Paragraph(
        "Para poder hacer un replay o para deshacer y rehacer jugadas, necesitamos movernos hacia adelante y hacia atrás. Si usáramos una lista simplemente "
        "enlazada, cada nodo solo sabe quién es el siguiente. Para avanzar en el tiempo no hay problema (actual = actual->siguiente), pero para retroceder "
        "una sola jugada no se puede regresar directamente porque no hay puntero al anterior. Habría que empezar a buscar desde el puro inicio de la lista "
        "recorriendo nodo por nodo hasta encontrar cuál era el que apuntaba a la jugada actual. Esto costaría O(k) operaciones cada vez que el usuario presione "
        "la tecla de retroceder (donde k es el número de la jugada actual), lo que causaría tirones o bajones de FPS si la partida ya lleva muchos turnos. "
        "La lista doblemente enlazada soluciona esto porque cada nodo tiene un puntero anterior y un puntero siguiente.<br/>"
        "• <i>Costo de avanzar un paso:</i> Solo se hace actual = actual->siguiente. Es una sola asignación de puntero, costo O(1).<br/>"
        "• <i>Costo de retroceder un paso:</i> Solo se hace actual = actual->anterior. Es una sola asignación de puntero, costo O(1).",
        estilo_cuerpo
    ))

    # P4
    story.append(Paragraph("<b>Pregunta 4: ¿Cómo garantiza su implementación que la cola de eventos programados siempre mantenga al frente el evento más próximo a dispararse? ¿Qué complejidad tiene insertar un nuevo evento?</b>", estilo_cuerpo))
    story.append(Paragraph(
        "Nuestra clase ColaPrioridad está implementada con un Montículo Binario Mínimo (Min-Heap) sobre un arreglo dinámico. La propiedad que siempre "
        "se cumple en este montículo es que cualquier nodo padre siempre tiene un tiempo menor o igual al de sus dos nodos hijos. Gracias a esta regla "
        "matemática, el evento que tiene el tiempo más pequeño (el que va a pasar más pronto) siempre queda garantizado en la raíz del árbol, que es la "
        "posición 0 del arreglo. Saber cuál es el siguiente evento con verTiempoFrente() cuesta O(1) porque solo se lee esa primera casilla.<br/>"
        "• <i>Inserción de un nuevo evento (encolar):</i> El nuevo evento se coloca al final del arreglo y luego se compara con su padre (sift-up o flotación). "
        "Si su tiempo es menor que el del padre, se intercambian y se sigue subiendo hasta que quede en su lugar correcto. Como un árbol binario con n elementos "
        "tiene una altura de log₂ n, a lo sumo se hacen log₂ n comparaciones. Por lo tanto, la inserción tiene una complejidad de O(log n), lo cual es muy "
        "eficiente y cumple la regla de no insertar al final y reordenar todo con un ordenamiento general (que costaría O(n log n)).",
        estilo_cuerpo
    ))

    # ------------------ CONCLUSIONES ------------------
    story.append(Paragraph("Conclusiones", estilo_titulo))
    story.append(Paragraph(
        "• Desarrollar este proyecto sin utilizar la STL nos permitió entender a fondo cómo funcionan las estructuras de datos lineales por dentro, "
        "cómo se manejan los punteros y la importancia de liberar siempre la memoria dinámica con delete para evitar fugas.<br/>"
        "• Cada mecánica del juego encaja de forma natural con una estructura específica: la cola para las piezas futuras, la pila para el hold, "
        "la lista de filas para el tablero, la lista doble para el historial y el replay, y el montículo para los eventos por tiempo.<br/>"
        "• Las pruebas de rendimiento demostraron en la práctica lo que se estudia en la teoría: para pocos datos algoritmos simples como Bubble Sort "
        "funcionan bien y son fáciles de programar, pero conforme el volumen de datos crece, algoritmos eficientes como Merge Sort son indispensables "
        "para que una aplicación no se vuelva lenta o se congele.",
        estilo_cuerpo
    ))

    doc.build(story)
    print(f"PDF normal generado en: {ruta_pdf}")

if __name__ == '__main__':
    base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    graf = os.path.join(base, "scratch", "benchmark_chart.png")
    pdf_path = os.path.join(base, "INFORME_PROYECTO1_EIF207.pdf")
    generar_pdf_normal(graf, pdf_path)
