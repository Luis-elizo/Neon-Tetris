#ifndef NEON_COLORS_H
#define NEON_COLORS_H

#include "raylib.h"

// colores del juego
namespace NeonColors {
    const Color FONDO        = { 10, 10, 20, 255 };
    const Color ROSA         = { 255, 20, 147, 255 };
    const Color CYAN         = { 0, 255, 255, 255 };
    const Color MORADO       = { 180, 0, 255, 255 };
    const Color BLANCO_SUAVE = { 230, 230, 240, 255 };

    // colores de las piezas
    const Color PIEZA_I = { 0, 255, 255, 255 };
    const Color PIEZA_O = { 255, 255, 0, 255 };
    const Color PIEZA_T = { 180, 0, 255, 255 };
    const Color PIEZA_S = { 0, 255, 0, 255 };
    const Color PIEZA_Z = { 255, 0, 0, 255 };
    const Color PIEZA_J = { 0, 0, 255, 255 };
    const Color PIEZA_L = { 255, 165, 0, 255 };
    const Color PIEZA_BASURA = { 120, 120, 120, 255 };
    const Color AMARILLO = { 255, 255, 0, 255 };

    // devuelve el color segun el id de la pieza
    inline Color GetPieceColor(int id) {
        switch(id) {
            case 1: return PIEZA_I;
            case 2: return PIEZA_O;
            case 3: return PIEZA_T;
            case 4: return PIEZA_S;
            case 5: return PIEZA_Z;
            case 6: return PIEZA_J;
            case 7: return PIEZA_L;
            case 8: return PIEZA_BASURA;
            default: return BLANCO_SUAVE;
        }
    }
}

#endif
