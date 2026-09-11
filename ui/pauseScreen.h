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

    int Update();
    void Draw();
};

#endif
