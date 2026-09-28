#ifndef PAUSE_SCREEN_H
#define PAUSE_SCREEN_H

#include "raylib.h"

// pantalla de pausa
class PauseScreen {
private:
    Rectangle botonContinuar; // boton para seguir jugando
    Rectangle botonMenu;      // boton para volver al menu
    bool continuarResaltado;  // mouse sobre continuar
    bool menuResaltado;       // mouse sobre menu

public:
    PauseScreen();

    int Update(); // revisa clics o tecla esc
    void Draw();  // dibuja el menu de pausa
};

#endif
