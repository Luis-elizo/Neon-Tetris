#ifndef GAME_SCREEN_H
#define GAME_SCREEN_H

#include "raylib.h"
#include "../estructuras/Tablero.h"
#include "../logica/Pieza.h"

class GameScreen {
private:
    int cellSize;
    int boardWidth;
    int boardHeight;
    int offsetX;
    int offsetY;

public:
    GameScreen();
    void Draw(const Tablero& tablero, const Pieza& piezaActual, int puntaje);
};

#endif
