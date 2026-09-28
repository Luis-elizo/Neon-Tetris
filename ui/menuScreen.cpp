#include "menuScreen.h"
#include "colors.h"
#include <string>

MenuScreen::MenuScreen() {
	// posiciones de los botones
	botonJugar = { 400, 440, 200, 55 };
	botonRanking = { 400, 520, 200, 55 };
	botonSalir = { 400, 600, 200, 55 };
	botonResaltado = false;
	rankingResaltado = false;
	salirResaltado = false;
}

int MenuScreen::Update() {
	Vector2 mouse = GetMousePosition();
	// revisa si el mouse esta encima
	botonResaltado = CheckCollisionPointRec(mouse, botonJugar);
	rankingResaltado = CheckCollisionPointRec(mouse, botonRanking);
	salirResaltado = CheckCollisionPointRec(mouse, botonSalir);
	
	// clic en los botones: 1 jugar, 2 ranking, 3 salir
	if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
		if (botonResaltado) return 1;
		if (rankingResaltado) return 2;
		if (salirResaltado) return 3;
	}
	return 0;
}

void MenuScreen::Draw() {
	ClearBackground(NeonColors::FONDO);
	DibujarTitulo();
	DibujarBotones();
}

void MenuScreen::DibujarTitulo() {
	std::string titulo = "NEON TETRIS";
	int tamanoFuente = 64;
	int anchoTexto = MeasureText(titulo.c_str(), tamanoFuente);
	int posX = (1000 - anchoTexto) / 2;
	int posY = 280;
	
	// efecto de brillo con texto repetido
	Color glow1 = NeonColors::MORADO;
	glow1.a = 60;
	Color glow2 = NeonColors::ROSA;
	glow2.a = 120;
	
	DrawText(titulo.c_str(), posX - 3, posY - 3, tamanoFuente, glow1);
	DrawText(titulo.c_str(), posX + 3, posY + 3, tamanoFuente, glow1);
	DrawText(titulo.c_str(), posX - 1, posY - 1, tamanoFuente, glow2);
	DrawText(titulo.c_str(), posX, posY, tamanoFuente, NeonColors::ROSA);
}

void MenuScreen::DibujarBotones() {
	// boton jugar
	Color colorBordeJugar = botonResaltado ? NeonColors::ROSA : NeonColors::CYAN;
	DrawRectangleRec(botonJugar, NeonColors::FONDO);
	DrawRectangleLinesEx(botonJugar, 3, colorBordeJugar);
	int anchoJugar = MeasureText("JUGAR", 26);
	DrawText("JUGAR", botonJugar.x + (botonJugar.width - anchoJugar) / 2, botonJugar.y + 14, 26, colorBordeJugar);

	// boton ranking
	Color colorBordeRank = rankingResaltado ? NeonColors::ROSA : NeonColors::CYAN;
	DrawRectangleRec(botonRanking, NeonColors::FONDO);
	DrawRectangleLinesEx(botonRanking, 3, colorBordeRank);
	int anchoRank = MeasureText("RANKING", 26);
	DrawText("RANKING", botonRanking.x + (botonRanking.width - anchoRank) / 2, botonRanking.y + 14, 26, colorBordeRank);

	// boton salir
	Color colorBordeSalir = salirResaltado ? NeonColors::ROSA : NeonColors::CYAN;
	DrawRectangleRec(botonSalir, NeonColors::FONDO);
	DrawRectangleLinesEx(botonSalir, 3, colorBordeSalir);
	int anchoSalir = MeasureText("SALIR", 26);
	DrawText("SALIR", botonSalir.x + (botonSalir.width - anchoSalir) / 2, botonSalir.y + 14, 26, colorBordeSalir);
}
