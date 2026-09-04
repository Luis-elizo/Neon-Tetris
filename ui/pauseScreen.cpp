#include "pauseScreen.h"
#include "colors.h"
#include <string>

PauseScreen::PauseScreen() {
    // Botones centrados
    botonContinuar = { 400, 350, 200, 60 };
    botonMenu = { 400, 450, 200, 60 };
    continuarResaltado = false;
    menuResaltado = false;
}

int PauseScreen::Update() {
    Vector2 mouse = GetMousePosition();
    continuarResaltado = CheckCollisionPointRec(mouse, botonContinuar);
    menuResaltado = CheckCollisionPointRec(mouse, botonMenu);

    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
        if (continuarResaltado) return 1;
        if (menuResaltado) return 2;
    }
    
    // Tambien se puede quitar la pausa con ESCAPE
    if (IsKeyPressed(KEY_ESCAPE)) {
        return 1;
    }

    return 0;
}

void PauseScreen::Draw() {
    // Fondo semi transparente
    DrawRectangle(0, 0, 1000, 900, { 0, 0, 0, 200 });

    std::string titulo = "PAUSADO";
    int anchoTexto = MeasureText(titulo.c_str(), 64);
    DrawText(titulo.c_str(), (1000 - anchoTexto) / 2, 200, 64, NeonColors::CYAN);

    // Dibujar boton Continuar
    Color colorBordeCont = continuarResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonContinuar, NeonColors::FONDO);
    DrawRectangleLinesEx(botonContinuar, 3, colorBordeCont);
    DrawText("Continuar", botonContinuar.x + 35, botonContinuar.y + 16, 28, colorBordeCont);

    // Dibujar boton Menu
    Color colorBordeMenu = menuResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonMenu, NeonColors::FONDO);
    DrawRectangleLinesEx(botonMenu, 3, colorBordeMenu);
    DrawText("Menu Principal", botonMenu.x + 10, botonMenu.y + 16, 24, colorBordeMenu);
}
