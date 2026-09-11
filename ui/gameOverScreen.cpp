#include "gameOverScreen.h"
#include "colors.h"
#include <string>

GameOverScreen::GameOverScreen() {
    botonReplay = { 400, 450, 200, 60 };
    botonMenu = { 400, 550, 200, 60 };
    menuResaltado = false;
    replayResaltado = false;
}

int GameOverScreen::Update() {
    Vector2 mouse = GetMousePosition();
    replayResaltado = CheckCollisionPointRec(mouse, botonReplay);
    menuResaltado = CheckCollisionPointRec(mouse, botonMenu);

    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
        if (menuResaltado) return 1;
        if (replayResaltado) return 2;
    }
    return 0;
}

void GameOverScreen::Draw(int puntajeFinal) {
    DrawRectangle(0, 0, 1000, 900, { 0, 0, 0, 230 });

    std::string titulo = "GAME OVER";
    int anchoTexto = MeasureText(titulo.c_str(), 64);
    DrawText(titulo.c_str(), (1000 - anchoTexto) / 2, 200, 64, NeonColors::ROSA);

    std::string puntaje = "Puntaje: " + std::to_string(puntajeFinal);
    int anchoPuntaje = MeasureText(puntaje.c_str(), 40);
    DrawText(puntaje.c_str(), (1000 - anchoPuntaje) / 2, 300, 40, RAYWHITE);

    Color colorBordeRep = replayResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonReplay, NeonColors::FONDO);
    DrawRectangleLinesEx(botonReplay, 3, colorBordeRep);
    DrawText("Ver Replay", botonReplay.x + 35, botonReplay.y + 16, 24, colorBordeRep);

    Color colorBordeMenu = menuResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonMenu, NeonColors::FONDO);
    DrawRectangleLinesEx(botonMenu, 3, colorBordeMenu);
    DrawText("Menu Principal", botonMenu.x + 10, botonMenu.y + 16, 24, colorBordeMenu);
}
