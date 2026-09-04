#ifndef GAME_OVER_SCREEN_H
#define GAME_OVER_SCREEN_H

#include "raylib.h"

class GameOverScreen {
private:
    Rectangle botonMenu;
    Rectangle botonReplay;
    bool menuResaltado;
    bool replayResaltado;

public:
    GameOverScreen();

    // Devuelve 1 si presiona Menu, 2 si presiona Replay, 0 si nada
    int Update();
    void Draw(int puntajeFinal);
};

#endif
