import os
from PIL import Image, ImageDraw, ImageFont

def crear_grafico_custom(ruta_salida):
    ancho, alto = 1000, 540
    # Fondo con estilo tarjeta limpia
    img = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    fuente_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    f_tit = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 20)
    f_sub = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 13)
    f_sec = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 14)
    f_txt = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 12)
    f_bold = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 12)
    f_grande = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 26)
    f_num = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 16)
    f_badge = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 11)

    # Marco exterior suave
    draw.rounded_rectangle([(15, 15), (ancho - 15, alto - 15)], radius=12, fill=(252, 253, 255), outline=(215, 222, 232), width=2)

    # Encabezado
    draw.text((40, 32), "Neon Tetris — Comparación de Rendimiento: Bubble Sort vs. Merge Sort", fill=(20, 30, 50), font=f_tit)
    draw.text((40, 60), "Tiempos reales medidos con <chrono> sobre arreglos aleatorios de registros de jugadores", fill=(100, 115, 130), font=f_sub)

    # Línea separadora
    draw.line([(40, 88), (ancho - 40, 88)], fill=(225, 230, 240), width=1)

    # -------------------------------------------------------------
    # PANEL IZQUIERDO: Escalamiento N = 10, 100, 1000 (Comparativa visual)
    # -------------------------------------------------------------
    x_izq, y_izq, w_izq, h_izq = 40, 105, 440, 400
    draw.rounded_rectangle([(x_izq, y_izq), (x_izq + w_izq, y_izq + h_izq)], radius=8, fill=(255, 255, 255), outline=(225, 230, 240), width=1)

    draw.text((x_izq + 20, y_izq + 15), "Pruebas con N = 10, 100 y 1 000 registros", fill=(30, 45, 65), font=f_sec)

    casos_izq = [
        ("N = 10 registros", "Empate técnico (0.9x)", (110, 120, 135), [
            ("Bubble Sort O(n²)", "0.9 µs", 45, (220, 50, 70)),
            ("Merge Sort O(n log n)", "1.0 µs", 50, (20, 120, 230))
        ]),
        ("N = 100 registros", "Merge es 3.05x más rápido", (20, 140, 90), [
            ("Bubble Sort O(n²)", "117.5 µs", 240, (220, 50, 70)),
            ("Merge Sort O(n log n)", "38.5 µs", 80, (20, 120, 230))
        ]),
        ("N = 1 000 registros", "Merge es 18.97x más rápido", (20, 140, 90), [
            ("Bubble Sort O(n²)", "12.33 ms (12 333 µs)", 340, (220, 50, 70)),
            ("Merge Sort O(n log n)", "0.65 ms (650 µs)", 35, (20, 120, 230))
        ])
    ]

    curr_y = y_izq + 48
    for n_tit, ventaja, col_v, barras in casos_izq:
        draw.text((x_izq + 20, curr_y), n_tit, fill=(25, 35, 50), font=f_bold)
        draw.text((x_izq + 200, curr_y), ventaja, fill=col_v, font=f_badge)
        curr_y += 20

        for nombre_alg, valor_txt, bar_w, col_b in barras:
            # Barra
            draw.rounded_rectangle([(x_izq + 20, curr_y + 3), (x_izq + 20 + bar_w, curr_y + 17)], radius=4, fill=col_b)
            # Texto
            draw.text((x_izq + 30 + bar_w, curr_y + 2), valor_txt, fill=(40, 50, 65), font=f_txt)
            curr_y += 22
        curr_y += 18

    # Leyenda pequeña panel izquierdo
    draw.rounded_rectangle([(x_izq + 20, curr_y + 10), (x_izq + 30, curr_y + 20)], radius=2, fill=(220, 50, 70))
    draw.text((x_izq + 35, curr_y + 9), "Bubble Sort", fill=(70, 80, 95), font=f_badge)

    draw.rounded_rectangle([(x_izq + 130, curr_y + 10), (x_izq + 140, curr_y + 20)], radius=2, fill=(20, 120, 230))
    draw.text((x_izq + 145, curr_y + 9), "Merge Sort", fill=(70, 80, 95), font=f_badge)

    # -------------------------------------------------------------
    # PANEL DERECHO: El salto masivo en N = 10 000
    # -------------------------------------------------------------
    x_der, y_der, w_der, h_der = 500, 105, 460, 400
    draw.rounded_rectangle([(x_der, y_der), (x_der + w_der, y_der + h_der)], radius=8, fill=(255, 255, 255), outline=(225, 230, 240), width=1)

    draw.text((x_der + 20, y_der + 15), "Prueba Límite: N = 10 000 registros", fill=(30, 45, 65), font=f_sec)

    # Tarjeta Bubble Sort N=10 000
    card_by = y_der + 48
    draw.rounded_rectangle([(x_der + 20, card_by), (x_der + w_der - 20, card_by + 80)], radius=6, fill=(255, 245, 246), outline=(245, 200, 205), width=1)
    draw.text((x_der + 35, card_by + 12), "Bubble Sort O(n²)", fill=(180, 30, 50), font=f_sec)
    draw.text((x_der + 35, card_by + 36), "1.31 segundos", fill=(180, 25, 45), font=f_grande)
    draw.text((x_der + 225, card_by + 44), "(1 309 150 µs)", fill=(120, 60, 70), font=f_txt)
    draw.text((x_der + 35, card_by + 64), "⚠ Se congela la pantalla durante el ordenamiento", fill=(170, 40, 60), font=f_badge)

    # Tarjeta Merge Sort N=10 000
    card_my = card_by + 95
    draw.rounded_rectangle([(x_der + 20, card_my), (x_der + w_der - 20, card_my + 80)], radius=6, fill=(245, 250, 255), outline=(195, 220, 245), width=1)
    draw.text((x_der + 35, card_my + 12), "Merge Sort O(n log n)", fill=(20, 100, 200), font=f_sec)
    draw.text((x_der + 35, card_my + 36), "0.0058 segundos", fill=(20, 95, 190), font=f_grande)
    draw.text((x_der + 265, card_my + 44), "(5 857 µs)", fill=(60, 100, 140), font=f_txt)
    draw.text((x_der + 35, card_my + 64), "✓ Ejecución instantánea a 60 FPS estables", fill=(20, 130, 80), font=f_badge)

    # Destacado: FACTOR DE DIFERENCIA
    card_dy = card_my + 95
    draw.rounded_rectangle([(x_der + 20, card_dy), (x_der + w_der - 20, card_dy + 65)], radius=6, fill=(246, 242, 255), outline=(215, 195, 245), width=1)
    draw.text((x_der + 35, card_dy + 12), "DIFERENCIA REAL MEDIDA:", fill=(110, 40, 180), font=f_badge)
    draw.text((x_der + 35, card_dy + 28), "Merge Sort es 223.5x más rápido", fill=(100, 30, 170), font=f_sec)

    # Nota de escalamiento abajo
    card_sy = card_dy + 75
    draw.text((x_der + 20, card_sy), "Escalamiento al multiplicar los datos por 10 (N=1k → N=10k):", fill=(70, 80, 95), font=f_badge)
    draw.text((x_der + 20, card_sy + 16), "• Bubble Sort aumentó su tiempo 106.1 veces (crecimiento cuadrático).", fill=(90, 40, 50), font=f_txt)
    draw.text((x_der + 20, card_sy + 32), "• Merge Sort aumentó su tiempo solo 9.0 veces (crecimiento cuasi-lineal).", fill=(30, 70, 110), font=f_txt)

    img.save(ruta_salida, format='PNG')
    print(f"Nuevo gráfico benchmark personalizado guardado en: {ruta_salida}")

if __name__ == '__main__':
    base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    out = os.path.join(base, "scratch", "benchmark_custom.png")
    crear_grafico_custom(out)
