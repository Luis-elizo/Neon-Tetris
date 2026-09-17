#include "raylib.h"
#include <iostream>
#include "ui/menuScreen.h"
#include "ui/pauseScreen.h"
#include "ui/gameOverScreen.h"
#include "ui/gameScreen.h"
#include "estructuras/Tablero.h"
#include "logica/Pieza.h"

enum class EstadoJuego {
    MENU,
    JUEGO,
    PAUSA,
    GAME_OVER,
    REPLAY
};

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
    Pieza piezaActual(static_cast<TipoPieza>(GetRandomValue(0, 6)));
    
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
            
            if (tiempoCaida >= velocidadCaida) {
                piezaActual.mover(1, 0); 
                if (tablero.hayColision(piezaActual)) {
                    piezaActual.mover(-1, 0); 
                    tablero.fijarPieza(piezaActual);
                    
                    int lineasLimpiadas = tablero.limpiarLineas();
                    if (lineasLimpiadas == 1) puntaje += 100;
                    else if (lineasLimpiadas == 2) puntaje += 300;
                    else if (lineasLimpiadas == 3) puntaje += 500;
                    else if (lineasLimpiadas >= 4) puntaje += 800;
                    
                    piezaActual = Pieza(static_cast<TipoPieza>(GetRandomValue(0, 6)));
                    
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
            } else if (accion == 2) {
                estadoActual = EstadoJuego::REPLAY;
            }
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            if (IsKeyPressed(KEY_M)) {
                estadoActual = EstadoJuego::MENU;
                tablero = Tablero();
                puntaje = 0;
            }
        }
        
        BeginDrawing();
        
        if (estadoActual == EstadoJuego::MENU) {
            menu.Draw();
        } 
        else if (estadoActual == EstadoJuego::JUEGO) {
            pantallaJuego.Draw(tablero, piezaActual, puntaje);
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            pantallaJuego.Draw(tablero, piezaActual, puntaje);
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
