#ifndef MENU_SCREEN_H
#define MENU_SCREEN_H

#include "raylib.h"

// pantalla de inicio del juego
class MenuScreen {
private:
    Rectangle botonJugar;   // boton para jugar
    Rectangle botonRanking; // boton para ver ranking
    Rectangle botonSalir;   // boton para salir
    bool botonResaltado;    // mouse sobre jugar
    bool rankingResaltado;  // mouse sobre ranking
    bool salirResaltado;    // mouse sobre salir
    
    void DibujarTitulo();   // dibuja el titulo
    void DibujarBotones();  // dibuja los botones
    
public:
    MenuScreen();
    
    int Update(); // revisa clics
    void Draw();  // dibuja el menu
};

#endif
