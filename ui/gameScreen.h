#ifndef GAME_SCREEN_H
#define GAME_SCREEN_H

#include <string>
#include "raylib.h"
#include "../estructuras/Tablero.h"
#include "../logica/Pieza.h"
#include "../estructuras/Cola.h"
#include "../estructuras/Pila.h"
#include "../estructuras/ListaDoble.h"

// pantalla de juego y del replay
class GameScreen {
private:
    int cellSize;    // tamaño de cada celda
    int boardWidth;  // columnas (10)
    int boardHeight; // filas (20)
    int offsetX;     // posicion horizontal del tablero
    int offsetY;     // posicion vertical del tablero
    
    std::string mensajeAlerta; // texto del evento sorpresa
    float tiempoFinAlerta;     // segundo en que se quita el texto
    
    // botones del replay
    Rectangle botonReplayAtras;
    Rectangle botonReplayPlay;
    Rectangle botonReplayAdelante;
    Rectangle botonReplaySalir;
    bool replayAtrasResaltado;
    bool replayPlayResaltado;
    bool replayAdelanteResaltado;
    bool replaySalirResaltado;

public:
    GameScreen();
    
    // dibuja el tablero y las piezas
    void Draw(Tablero& tablero, Pieza& piezaActual, int puntaje, Cola& colaSiguientes, Pila& pilaHold, float tiempoPartida, bool animandoLimpieza = false, float tiempoAnimacion = 0.0f);
    
    // revisa clics en los botones del replay
    int UpdateReplay();
    
    // dibuja la repeticion del replay
    void DrawReplay(NodoHistorial* estadoReplay, bool reproduciendoAuto = false);
    
    // muestra el mensaje sorpresa abajo
    void setAlerta(std::string mensaje, float tiempoFin);
};

#endif
