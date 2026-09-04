#ifndef PAUSE_SCREEN_H
#define PAUSE_SCREEN_H

#include "raylib.h"

class PauseScreen {
private:
    Rectangle botonContinuar;
    Rectangle botonMenu;
    bool continuarResaltado;
    bool menuResaltado;

public:
    PauseScreen();

    // Devuelve 1 si presiona Continuar, 2 si presiona Menu, 0 si no pasa nada
    int Update();
    void Draw();
};

#endif
