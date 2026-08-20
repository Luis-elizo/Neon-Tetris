#include "MenuScreen.h"
#include "Colors.h"
#include <string>

MenuScreen::MenuScreen() {
	botonJugar = { 400, 500, 200, 60 };
	botonResaltado = false;
}

bool MenuScreen::Update() {
	Vector2 mouse = GetMousePosition();
	botonResaltado = CheckCollisionPointRec(mouse, botonJugar);
	
	if (botonResaltado && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
		return true;
	}
	return false;
}

void MenuScreen::Draw() {
	ClearBackground(NeonColors::FONDO);
	DibujarTitulo();
	DibujarBoton();
}

void MenuScreen::DibujarTitulo() {
	std::string titulo = "NEON TETRIS";
	int tamanoFuente = 64;
	int anchoTexto = MeasureText(titulo.c_str(), tamanoFuente);
	int x = (1000 - anchoTexto) / 2;
	int y = 300;
	
	Color glow1 = NeonColors::MORADO;
	glow1.a = 60;
	Color glow2 = NeonColors::ROSA;
	glow2.a = 120;
	
	DrawText(titulo.c_str(), x - 3, y - 3, tamanoFuente, glow1);
	DrawText(titulo.c_str(), x + 3, y + 3, tamanoFuente, glow1);
	DrawText(titulo.c_str(), x - 1, y - 1, tamanoFuente, glow2);
	DrawText(titulo.c_str(), x, y, tamanoFuente, NeonColors::ROSA);
}

void MenuScreen::DibujarBoton() {
	Color colorBorde = botonResaltado ? NeonColors::ROSA : NeonColors::CYAN;
	Color colorTexto = botonResaltado ? NeonColors::ROSA : NeonColors::CYAN;
	
	DrawRectangleRec(botonJugar, NeonColors::FONDO);
	DrawRectangleLinesEx(botonJugar, 3, colorBorde);
	
	std::string textoBoton = "JUGAR";
	int anchoBoton = MeasureText(textoBoton.c_str(), 28);
	int xBoton = botonJugar.x + (botonJugar.width - anchoBoton) / 2;
	int yBoton = botonJugar.y + (botonJugar.height - 28) / 2;
	DrawText(textoBoton.c_str(), xBoton, yBoton, 28, colorTexto);
}
