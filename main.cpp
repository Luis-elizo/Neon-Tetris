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
    
    int puntajeTemporal = 1500;
    
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
                    // Por ahora solo apilamos sin destruir ni dar puntos
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
            } else if (accion == 2) {
                estadoActual = EstadoJuego::REPLAY;
            }
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            if (IsKeyPressed(KEY_M)) {
                estadoActual = EstadoJuego::MENU;
            }
        }
        
        BeginDrawing();
        
        if (estadoActual == EstadoJuego::MENU) {
            menu.Draw();
        } 
        else if (estadoActual == EstadoJuego::JUEGO) {
            pantallaJuego.Draw(tablero, piezaActual);
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            pantallaJuego.Draw(tablero, piezaActual);
            pantallaPausa.Draw();
        }
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            ClearBackground(BLACK);
            pantallaGameOver.Draw(puntajeTemporal);
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
