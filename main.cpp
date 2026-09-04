#include "raylib.h"
#include <iostream>
#include "ui/menuScreen.h"
#include "ui/pauseScreen.h"
#include "ui/gameOverScreen.h"

// Estados posibles del juego.
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
	
	EstadoJuego estadoActual = EstadoJuego::MENU;
	
    MenuScreen menu;
    PauseScreen pantallaPausa;
    GameOverScreen pantallaGameOver;
    
    int puntajeTemporal = 1500; // Simular un puntaje por ahora
	
	while (!WindowShouldClose()) {
		
		// --- Actualizar segun el estado actual ---
		if (estadoActual == EstadoJuego::MENU) {
			if (menu.Update()) {
				estadoActual = EstadoJuego::JUEGO;
			}
		} 
        else if (estadoActual == EstadoJuego::JUEGO) {
            // Simulacion de entrar al menu de pausa
            if (IsKeyPressed(KEY_ESCAPE)) {
                estadoActual = EstadoJuego::PAUSA;
            }
            // Simulacion de Game Over manual para pruebas (presionar G)
            if (IsKeyPressed(KEY_G)) {
                estadoActual = EstadoJuego::GAME_OVER;
            }
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            int accion = pantallaPausa.Update();
            if (accion == 1) { // Continuar
                estadoActual = EstadoJuego::JUEGO;
            } else if (accion == 2) { // Menu
                estadoActual = EstadoJuego::MENU;
            }
        }
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            int accion = pantallaGameOver.Update();
            if (accion == 1) { // Menu
                estadoActual = EstadoJuego::MENU;
            } else if (accion == 2) { // Replay
                estadoActual = EstadoJuego::REPLAY;
            }
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            // Logica temporal para salir de replay (presionar M para volver al menu)
            if (IsKeyPressed(KEY_M)) {
                estadoActual = EstadoJuego::MENU;
            }
        }
		
		BeginDrawing();
		
		if (estadoActual == EstadoJuego::MENU) {
			menu.Draw();
		} 
        else if (estadoActual == EstadoJuego::JUEGO) {
			ClearBackground(BLACK);
			DrawText("Aqui va el juego...", 180, 190, 20, RAYWHITE);
            DrawText("Presiona ESC para Pausa", 180, 230, 20, GRAY);
            DrawText("Presiona G para Game Over", 180, 260, 20, GRAY);
		}
        else if (estadoActual == EstadoJuego::PAUSA) {
            // Se dibuja el juego en el fondo para dar efecto de pausa
            ClearBackground(BLACK);
			DrawText("Aqui va el juego...", 180, 190, 20, RAYWHITE);
            // Encima dibujamos la pausa
            pantallaPausa.Draw();
        }
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            // Se dibuja el juego de fondo antes del game over
            ClearBackground(BLACK);
            pantallaGameOver.Draw(puntajeTemporal);
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            ClearBackground(DARKGRAY);
            DrawText("REPRODUCIENDO REPLAY...", 180, 190, 30, RAYWHITE);
            DrawText("Presiona M para volver al Menu", 180, 250, 20, LIGHTGRAY);
        }
		
		EndDrawing();
	}
	
	CloseWindow();	
	return 0;
}
