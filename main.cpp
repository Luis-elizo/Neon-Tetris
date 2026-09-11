#include "raylib.h"
#include <iostream>
#include "ui/menuScreen.h"
#include "ui/pauseScreen.h"
#include "ui/gameOverScreen.h"
#include "ui/gameScreen.h"

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
    
    int puntajeTemporal = 1500;
    
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
            pantallaJuego.Draw();
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            pantallaJuego.Draw();
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
