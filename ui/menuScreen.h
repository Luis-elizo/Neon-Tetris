#ifndef MENU_SCREEN_H
#define MENU_SCREEN_H

#include "raylib.h"

class MenuScreen {
private:
    Rectangle botonJugar;
    bool botonResaltado;
    
    void DibujarTitulo();
    void DibujarBoton();
    
public:
    MenuScreen();
    
    bool Update();
    void Draw();
};

#endif
