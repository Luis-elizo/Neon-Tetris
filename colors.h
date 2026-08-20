#ifndef NEON_COLORS_H
#define NEON_COLORS_H

#include "raylib.h"

// Paleta de colores con tematica neon para todo el juego.
namespace NeonColors {
	const Color FONDO        = { 10, 10, 20, 255 };   // Casi negro con tinte azulado
	const Color ROSA         = { 255, 20, 147, 255 };  // Rosa neon (titulo, acentos)
	const Color CYAN         = { 0, 255, 255, 255 };   // Cyan neon (botones, bordes)
	const Color MORADO       = { 180, 0, 255, 255 };   // Morado neon (sombras, detalles)
	const Color BLANCO_SUAVE = { 230, 230, 240, 255 }; // Texto secundario
}

#endif
