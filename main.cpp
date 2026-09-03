#include "raylib.h"
#include<iostream>
#include "ui/menuScreen.h"

// Estados posibles del juego.
enum class EstadoJuego {
	MENU,
	JUEGO
};

int main() {
	InitWindow(1000, 900, "NeonTetris");
	SetTargetFPS(60);
	
	EstadoJuego estadoActual = EstadoJuego::MENU;
	MenuScreen menu;
	
	while (!WindowShouldClose()) {
		
		// --- Actualizar segun el estado actual ---
		if (estadoActual == EstadoJuego::MENU) {
			if (menu.Update()) {
				estadoActual = EstadoJuego::JUEGO;
			}
		}
		
		BeginDrawing();
		
		if (estadoActual == EstadoJuego::MENU) {
			menu.Draw();
		} else if (estadoActual == EstadoJuego::JUEGO) {
			ClearBackground(BLACK);
			DrawText("Aqui va el juego...", 180, 190, 20, RAYWHITE);
		}
		
		EndDrawing();
	}
	
	CloseWindow();	
	return 0;
}
