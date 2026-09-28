#ifndef GAME_OVER_SCREEN_H
#define GAME_OVER_SCREEN_H

#include "raylib.h"
#include <string>

// pantalla cuando el jugador pierde
class GameOverScreen {
private:
    Rectangle cajaTexto;    // cuadro para escribir el nombre
    Rectangle botonGuardar; // boton para guardar
    Rectangle botonReplay;  // boton para ver replay
    Rectangle botonMenu;    // boton para volver al menu

    bool guardarResaltado; // mouse sobre guardar
    bool replayResaltado;  // mouse sobre replay
    bool menuResaltado;    // mouse sobre menu

    std::string nombreJugador; // nombre que escribe el jugador
    bool yaGuardo;             // si ya guardo el puntaje
    int contadorFrames;        // contador para el cursor parpadeante

public:
    GameOverScreen();

    void Reset();                 // limpia el texto y banderas
    int Update(int puntajeFinal); // maneja teclado y clics
    void Draw(int puntajeFinal);  // dibuja la pantalla
};

#endif
