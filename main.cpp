#include "raylib.h"
#include <iostream>
#include "ui/menuScreen.h"
#include "ui/pauseScreen.h"
#include "ui/gameOverScreen.h"
#include "ui/gameScreen.h"
#include "estructuras/Tablero.h"
#include "logica/Pieza.h"
#include "estructuras/Cola.h"
#include "estructuras/Pila.h"

enum class EstadoJuego {
    MENU,
    JUEGO,
    PAUSA,
    GAME_OVER,
    REPLAY
};

void LlenarBolsa(Cola& cola) {
    TipoPieza bolsa[7] = { 
        TipoPieza::I, TipoPieza::O, TipoPieza::T, TipoPieza::S, 
        TipoPieza::Z, TipoPieza::J, TipoPieza::L 
    };
    
    for (int i = 6; i > 0; --i) {
        int j = GetRandomValue(0, i);
        TipoPieza temp = bolsa[i];
        bolsa[i] = bolsa[j];
        bolsa[j] = temp;
    }
    
    for (int i = 0; i < 7; ++i) {
        cola.encolar(bolsa[i]);
    }
}

int main() {
    InitWindow(1000, 900, "NeonTetris");
    SetTargetFPS(60);
    SetExitKey(0);
    
    EstadoJuego estadoActual = EstadoJuego::MENU;
    
    MenuScreen menu;
    PauseScreen pantallaPausa;
    GameOverScreen pantallaGameOver;
    GameScreen pantallaJuego;
    
    Tablero tablero;
    
    Cola colaSiguientes;
    LlenarBolsa(colaSiguientes);
    Pieza piezaActual(colaSiguientes.desencolar());
    
    Pila pilaHold;
    bool yaIntercambio = false;
    
    int puntaje = 0;
    
    float tiempoCaida = 0.0f;
    float velocidadCaida = 0.5f;
    
    while (!WindowShouldClose()) {
        
        if (estadoActual == EstadoJuego::MENU) {
            if (menu.Update()) {
                estadoActual = EstadoJuego::JUEGO;
            }
        } 
        else if (estadoActual == EstadoJuego::JUEGO) {
            if (IsKeyPressed(KEY_ESCAPE)) {
                estadoActual = EstadoJuego::PAUSA;
            }
            if (IsKeyPressed(KEY_G)) {
                estadoActual = EstadoJuego::GAME_OVER;
            }
            
            // Logica de Caida y Movimiento
            tiempoCaida += GetFrameTime();
            
            if (IsKeyPressed(KEY_LEFT)) {
                piezaActual.mover(0, -1);
                if (tablero.hayColision(piezaActual)) piezaActual.mover(0, 1);
            }
            if (IsKeyPressed(KEY_RIGHT)) {
                piezaActual.mover(0, 1);
                if (tablero.hayColision(piezaActual)) piezaActual.mover(0, -1);
            }
            if (IsKeyPressed(KEY_UP)) {
                piezaActual.rotar();
                if (tablero.hayColision(piezaActual)) piezaActual.deshacerRotacion();
            }
            if (IsKeyDown(KEY_DOWN)) {
                velocidadCaida = 0.05f; // Soft drop
            } else {
                velocidadCaida = 0.5f;  // Velocidad normal
            }
            
            if (IsKeyPressed(KEY_RIGHT_SHIFT) && !yaIntercambio) {
                TipoPieza tipoActual = piezaActual.getTipo();
                if (pilaHold.estaVacia()) {
                    pilaHold.apilar(tipoActual);
                    if (colaSiguientes.estaVacia()) {
                        LlenarBolsa(colaSiguientes);
                    }
                    piezaActual = Pieza(colaSiguientes.desencolar());
                } else {
                    TipoPieza guardada = pilaHold.desapilar();
                    pilaHold.apilar(tipoActual);
                    piezaActual = Pieza(guardada);
                }
                yaIntercambio = true;
                tiempoCaida = 0.0f; 
            }
            
            if (tiempoCaida >= velocidadCaida) {
                piezaActual.mover(1, 0); 
                if (tablero.hayColision(piezaActual)) {
                    piezaActual.mover(-1, 0); 
                    tablero.fijarPieza(piezaActual);
                    yaIntercambio = false; 
                    
                    int lineasLimpiadas = tablero.limpiarLineas();
                    if (lineasLimpiadas == 1) puntaje += 100;
                    else if (lineasLimpiadas == 2) puntaje += 300;
                    else if (lineasLimpiadas == 3) puntaje += 500;
                    else if (lineasLimpiadas >= 4) puntaje += 800;
                    
                    if (colaSiguientes.estaVacia()) {
                        LlenarBolsa(colaSiguientes);
                    }
                    piezaActual = Pieza(colaSiguientes.desencolar());
                    
                    // Si al nacer ya hay colision, es Game Over
                    if (tablero.hayColision(piezaActual)) {
                        estadoActual = EstadoJuego::GAME_OVER;
                    }
                }
                tiempoCaida = 0.0f;
            }
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            int accion = pantallaPausa.Update();
            if (accion == 1) {
                estadoActual = EstadoJuego::JUEGO;
            } else if (accion == 2) {
                estadoActual = EstadoJuego::MENU;
            }
        }
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            int accion = pantallaGameOver.Update();
            if (accion == 1) {
                estadoActual = EstadoJuego::MENU;
                // Reset juego
                tablero = Tablero();
                puntaje = 0;
                while (!colaSiguientes.estaVacia()) colaSiguientes.desencolar();
                LlenarBolsa(colaSiguientes);
                piezaActual = Pieza(colaSiguientes.desencolar());
                while (!pilaHold.estaVacia()) pilaHold.desapilar();
                yaIntercambio = false;
            } else if (accion == 2) {
                estadoActual = EstadoJuego::REPLAY;
            }
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            if (IsKeyPressed(KEY_M)) {
                estadoActual = EstadoJuego::MENU;
                tablero = Tablero();
                puntaje = 0;
                while (!colaSiguientes.estaVacia()) colaSiguientes.desencolar();
                LlenarBolsa(colaSiguientes);
                piezaActual = Pieza(colaSiguientes.desencolar());
                while (!pilaHold.estaVacia()) pilaHold.desapilar();
                yaIntercambio = false;
            }
        }
        
        BeginDrawing();
        
        if (estadoActual == EstadoJuego::MENU) {
            menu.Draw();
        } 
        else if (estadoActual == EstadoJuego::JUEGO) {
            pantallaJuego.Draw(tablero, piezaActual, puntaje, colaSiguientes, pilaHold);
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            pantallaJuego.Draw(tablero, piezaActual, puntaje, colaSiguientes, pilaHold);
            pantallaPausa.Draw();
        }
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            ClearBackground(BLACK);
            pantallaGameOver.Draw(puntaje);
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            ClearBackground(DARKGRAY);
            DrawText("REPLAY...", 180, 190, 30, RAYWHITE);
        }
        
        EndDrawing();
    }
    
    CloseWindow();    
    return 0;
}
