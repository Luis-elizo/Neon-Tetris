import os
import math
from PIL import Image, ImageDraw, ImageFont

def generar_curva_benchmark_pro(ruta_salida):
    ancho, alto = 1000, 560
    img = Image.new('RGB', (ancho, alto), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    fuente_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')
    f_tit = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 19)
    f_sub = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 12)
    f_ejes = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 13)
    f_ticks = ImageFont.truetype(os.path.join(fuente_dir, 'arial.ttf'), 11)
    f_leyenda = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 12)
    f_anot = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 11)
    f_callout = ImageFont.truetype(os.path.join(fuente_dir, 'arialbd.ttf'), 12)

    # Marco exterior suave
    draw.rounded_rectangle([(12, 12), (ancho - 12, alto - 12)], radius=12, fill=(255, 255, 255), outline=(215, 222, 235), width=2)

    # Encabezado
    draw.text((45, 28), "Curvas de Crecimiento: Bubble Sort O(n²) vs. Merge Sort O(n log n)", fill=(22, 32, 50), font=f_tit)
    draw.text((45, 54), "Escala logarítmica en microsegundos (µs) para evaluar la tendencia teórica con N = 10, 100, 1 000 y 10 000", fill=(95, 105, 125), font=f_sub)

    # Coordenadas del gráfico
    margen_l = 100
    margen_r = 930
    margen_t = 95
    margen_b = 485
    plot_w = margen_r - margen_l
    plot_h = margen_b - margen_t

    # Fondo del plot con rejilla suave
    draw.rounded_rectangle([(margen_l, margen_t), (margen_r, margen_b)], radius=6, fill=(250, 251, 254), outline=(215, 225, 238), width=1)

    # Escala logarítmica: de 0.1 µs (10^-1) a 10 000 000 µs (10^7)
    min_log = -0.5
    max_log = 6.5
    rango_log = max_log - min_log

    def y_a_px(val):
        log_v = math.log10(max(val, 0.1))
        frac = (log_v - min_log) / rango_log
        return margen_b - (frac * plot_h)

    # Rejilla horizontal
    grid_y = [
        (0.1, "0.1 µs"),
        (1.0, "1 µs"),
        (10.0, "10 µs"),
        (100.0, "100 µs"),
        (1000.0, "1 ms (1k µs)"),
        (10000.0, "10 ms"),
        (100000.0, "100 ms"),
        (1000000.0, "1 s (1M µs)")
    ]

    for val, eti in grid_y:
        py = y_a_px(val)
        # Línea de rejilla
        draw.line([(margen_l, py), (margen_r, py)], fill=(232, 237, 246), width=1)
        draw.text((margen_l - 85, py - 7), eti, fill=(115, 125, 140), font=f_ticks)

    # Coordenadas en X
    x_pos = [
        margen_l + plot_w * 0.12,
        margen_l + plot_w * 0.38,
        margen_l + plot_w * 0.64,
        margen_l + plot_w * 0.90
    ]
    etiquetas_x = ["N = 10", "N = 100", "N = 1 000", "N = 10 000"]

    for xp, eti in zip(x_pos, etiquetas_x):
        draw.line([(xp, margen_t), (xp, margen_b)], fill=(232, 237, 246), width=1)
        # Etiqueta X con fondo suave
        draw.text((xp - 30, margen_b + 14), eti, fill=(30, 45, 65), font=f_ejes)

    # Datos medidos
    datos_bubble = [0.9, 117.5, 12333.0, 1309150.0]
    datos_merge = [1.0, 38.5, 650.0, 5857.0]

    pts_bubble = [(xp, y_a_px(v)) for xp, v in zip(x_pos, datos_bubble)]
    pts_merge = [(xp, y_a_px(v)) for xp, v in zip(x_pos, datos_merge)]

    # 1. Relleno bajo la curva de Bubble (Sombreado tenue para dar profundidad)
    poly_bubble = [(x_pos[0], margen_b)] + pts_bubble + [(x_pos[-1], margen_b)]
    overlay = Image.new('RGBA', (ancho, alto), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    d_ov.polygon(poly_bubble, fill=(235, 45, 80, 25))
    # Relleno bajo la curva de Merge
    poly_merge = [(x_pos[0], margen_b)] + pts_merge + [(x_pos[-1], margen_b)]
    d_ov.polygon(poly_merge, fill=(20, 130, 240, 35))
    img.paste(overlay, (0, 0), overlay)

    # 2. Dibujar líneas principales con grosor elegante y antialiasing
    col_bubble = (215, 30, 65)     # Carmín / Magenta Neon
    col_merge = (15, 115, 235)     # Azul Eléctrico

    draw.line(pts_bubble, fill=col_bubble, width=4)
    draw.line(pts_merge, fill=col_merge, width=4)

    # 3. Marcadores y etiquetas para Bubble Sort
    for i, (xp, yp) in enumerate(pts_bubble):
        r = 6
        # Resplandor exterior
        draw.ellipse([(xp - r - 2, yp - r - 2), (xp + r + 2, yp + r + 2)], fill=(255, 200, 215))
        draw.ellipse([(xp - r, yp - r), (xp + r, yp + r)], fill=col_bubble, outline=(255, 255, 255), width=2)

        if i == 0:
            txt = "0.9 µs"
            draw.text((xp - 20, yp - 24), txt, fill=col_bubble, font=f_anot)
        elif i == 1:
            txt = "117.5 µs"
            draw.text((xp - 26, yp - 24), txt, fill=col_bubble, font=f_anot)
        elif i == 2:
            txt = "12.33 ms"
            draw.text((xp - 28, yp - 24), txt, fill=col_bubble, font=f_anot)
        elif i == 3:
            txt = "1.31 s (1 309 ms)"
            draw.rounded_rectangle([(xp - 120, yp - 32), (xp - 10, yp - 8)], radius=4, fill=(255, 240, 244), outline=col_bubble, width=1)
            draw.text((xp - 114, yp - 28), txt, fill=col_bubble, font=f_anot)

    # 4. Marcadores y etiquetas para Merge Sort
    for i, (xp, yp) in enumerate(pts_merge):
        r = 6
        draw.rectangle([(xp - r - 2, yp - r - 2), (xp + r + 2, yp + r + 2)], fill=(200, 225, 255))
        draw.rectangle([(xp - r, yp - r), (xp + r, yp + r)], fill=col_merge, outline=(255, 255, 255), width=2)

        if i == 0:
            txt = "1.0 µs"
            draw.text((xp - 18, yp + 10), txt, fill=col_merge, font=f_anot)
        elif i == 1:
            txt = "38.5 µs"
            draw.text((xp - 22, yp + 10), txt, fill=col_merge, font=f_anot)
        elif i == 2:
            txt = "0.65 ms"
            draw.text((xp - 24, yp + 10), txt, fill=col_merge, font=f_anot)
        elif i == 3:
            txt = "5.86 ms (0.0058 s)"
            draw.rounded_rectangle([(xp - 130, yp + 10), (xp - 10, yp + 32)], radius=4, fill=(240, 248, 255), outline=col_merge, width=1)
            draw.text((xp - 124, yp + 14), txt, fill=col_merge, font=f_anot)

    # 5. Brecha visual y Callout de aceleración en N = 10 000
    y_b_final = pts_bubble[3][1]
    y_m_final = pts_merge[3][1]
    x_final = x_pos[3]

    # Línea vertical punteada indicando la brecha
    for seg_y in range(int(y_b_final), int(y_m_final), 8):
        draw.line([(x_final, seg_y), (x_final, min(seg_y + 4, y_m_final))], fill=(140, 50, 190), width=2)

    # Tarjeta de Callout central en la brecha
    box_w, box_h = 165, 46
    box_x = x_final - 190
    box_y = (y_b_final + y_m_final) // 2 - 23
    draw.rounded_rectangle([(box_x, box_y), (box_x + box_w, box_y + box_h)], radius=6, fill=(248, 240, 255), outline=(150, 40, 200), width=1)
    draw.text((box_x + 12, box_y + 6), "BRECHA DE TIEMPO:", fill=(130, 30, 180), font=f_ticks)
    draw.text((box_x + 12, box_y + 23), "Merge es 223.5x más rápido", fill=(110, 20, 160), font=f_callout)

    # Flecha pequeña apuntando a la línea de brecha
    draw.polygon([(box_x + box_w, box_y + 23), (box_x + box_w + 8, box_y + 23), (box_x + box_w, box_y + 19)], fill=(150, 40, 200))

    # 6. Leyenda ubicada en la zona superior izquierda (despejada de datos)
    leg_x, leg_y = margen_l + 25, margen_t + 20
    draw.rounded_rectangle([(leg_x, leg_y), (leg_x + 235, leg_y + 68)], radius=6, fill=(255, 255, 255), outline=(210, 218, 230), width=1)

    # Bubble item
    draw.line([(leg_x + 15, leg_y + 22), (leg_x + 45, leg_y + 22)], fill=col_bubble, width=3)
    draw.ellipse([(leg_x + 26, leg_y + 18), (leg_x + 34, leg_y + 26)], fill=col_bubble)
    draw.text((leg_x + 55, leg_y + 14), "Bubble Sort O(n²)", fill=(30, 35, 45), font=f_leyenda)

    # Merge item
    draw.line([(leg_x + 15, leg_y + 48), (leg_x + 45, leg_y + 48)], fill=col_merge, width=3)
    draw.rectangle([(leg_x + 26, leg_y + 44), (leg_x + 34, leg_y + 52)], fill=col_merge)
    draw.text((leg_x + 55, leg_y + 40), "Merge Sort O(n log n)", fill=(30, 35, 45), font=f_leyenda)

    img.save(ruta_salida, format='PNG')
    print(f"Nuevo gráfico de curva benchmark guardado en: {ruta_salida}")

if __name__ == '__main__':
    base = r"c:\Users\luisa\Universidad\ll ciclo 2026\Estructura de Datos\Neon-Tetris"
    out = os.path.join(base, "scratch", "benchmark_curva_pro.png")
    generar_curva_benchmark_pro(out)
