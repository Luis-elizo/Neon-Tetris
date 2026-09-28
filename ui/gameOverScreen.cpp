#include "gameOverScreen.h"
#include "colors.h"
#include "../estructuras/ManejadorJSON.h"
#include <cctype>

GameOverScreen::GameOverScreen() {
    cajaTexto = { 350, 350, 300, 50 };
    botonGuardar = { 350, 420, 300, 50 };
    botonReplay = { 350, 500, 300, 50 };
    botonMenu = { 350, 580, 300, 50 };

    guardarResaltado = false;
    replayResaltado = false;
    menuResaltado = false;

    nombreJugador = "";
    yaGuardo = false;
    contadorFrames = 0;
}

void GameOverScreen::Reset() {
    nombreJugador = "";
    yaGuardo = false;
    contadorFrames = 0;
}

int GameOverScreen::Update(int puntajeFinal) {
    contadorFrames++;
    Vector2 mouse = GetMousePosition();

    guardarResaltado = CheckCollisionPointRec(mouse, botonGuardar);
    replayResaltado = CheckCollisionPointRec(mouse, botonReplay);
    menuResaltado = CheckCollisionPointRec(mouse, botonMenu);

    if (!yaGuardo) {
        // captura lo que escribe en el teclado
        int teclaPresionada = GetCharPressed();
        while (teclaPresionada > 0) {
            // no permite caracteres especiales que dañen el json
            if ((teclaPresionada >= 32) && (teclaPresionada <= 126) && (nombreJugador.length() < 10) && 
                (teclaPresionada != '"') && (teclaPresionada != ':') && (teclaPresionada != ',') && (teclaPresionada != '{') && (teclaPresionada != '}')) {
                nombreJugador += (char)toupper(teclaPresionada);
            }
            teclaPresionada = GetCharPressed();
        }

        // borra una letra si presiona backspace
        if (IsKeyPressed(KEY_BACKSPACE)) {
            if (!nombreJugador.empty()) {
                nombreJugador.pop_back();
            }
        }

        // guarda si presiona enter o el boton
        if ((guardarResaltado && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) || IsKeyPressed(KEY_ENTER)) {
            if (!nombreJugador.empty()) {
                ListaPuntajes lista = ManejadorJSON::cargar("scores.json");
                if (lista.cantidad < 50) {
                    lista.registros[lista.cantidad].nombre = nombreJugador;
                    lista.registros[lista.cantidad].puntaje = puntajeFinal;
                    lista.cantidad++;

                    ManejadorJSON::guardar("scores.json", lista);
                    yaGuardo = true;
                }
            }
        }
    }

    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
        if (menuResaltado) return 1;
        if (replayResaltado) return 2;
    }

    return 0;
}

void GameOverScreen::Draw(int puntajeFinal) {
    DrawRectangle(0, 0, 1000, 900, { 0, 0, 0, 235 });

    std::string titulo = "GAME OVER";
    int anchoTexto = MeasureText(titulo.c_str(), 60);
    DrawText(titulo.c_str(), (1000 - anchoTexto) / 2, 130, 60, NeonColors::ROSA);

    std::string puntaje = "Puntaje Final: " + std::to_string(puntajeFinal);
    int anchoPuntaje = MeasureText(puntaje.c_str(), 34);
    DrawText(puntaje.c_str(), (1000 - anchoPuntaje) / 2, 220, 34, RAYWHITE);

    if (!yaGuardo) {
        DrawText("ESCRIBE TU NOMBRE:", 350, 320, 18, NeonColors::CYAN);
    } else {
        DrawText("PUNTAJE REGISTRADO:", 350, 320, 18, NeonColors::AMARILLO);
    }

    DrawRectangleRec(cajaTexto, NeonColors::FONDO);
    DrawRectangleLinesEx(cajaTexto, 2, yaGuardo ? DARKGRAY : NeonColors::CYAN);

    std::string textoMostrar = nombreJugador;
    if (!yaGuardo && (contadorFrames / 30) % 2 == 0) {
        textoMostrar += "_";
    }
    DrawText(textoMostrar.c_str(), cajaTexto.x + 15, cajaTexto.y + 13, 24, NeonColors::BLANCO_SUAVE);

    if (!yaGuardo) {
        Color colorGuardar = guardarResaltado ? NeonColors::ROSA : NeonColors::CYAN;
        DrawRectangleRec(botonGuardar, NeonColors::FONDO);
        DrawRectangleLinesEx(botonGuardar, 2, colorGuardar);
        int anchoG = MeasureText("GUARDAR PUNTAJE", 20);
        DrawText("GUARDAR PUNTAJE", botonGuardar.x + (botonGuardar.width - anchoG) / 2, botonGuardar.y + 15, 20, colorGuardar);
    } else {
        DrawRectangleRec(botonGuardar, NeonColors::FONDO);
        DrawRectangleLinesEx(botonGuardar, 2, DARKGRAY);
        int anchoG = MeasureText("GUARDADO EXITOSO", 20);
        DrawText("GUARDADO EXITOSO", botonGuardar.x + (botonGuardar.width - anchoG) / 2, botonGuardar.y + 15, 20, NeonColors::AMARILLO);
    }

    Color colorBordeRep = replayResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonReplay, NeonColors::FONDO);
    DrawRectangleLinesEx(botonReplay, 2, colorBordeRep);
    int anchoRep = MeasureText("VER REPLAY", 20);
    DrawText("VER REPLAY", botonReplay.x + (botonReplay.width - anchoRep) / 2, botonReplay.y + 15, 20, colorBordeRep);

    Color colorBordeMenu = menuResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonMenu, NeonColors::FONDO);
    DrawRectangleLinesEx(botonMenu, 2, colorBordeMenu);
    int anchoMenu = MeasureText("MENU PRINCIPAL", 20);
    DrawText("MENU PRINCIPAL", botonMenu.x + (botonMenu.width - anchoMenu) / 2, botonMenu.y + 15, 20, colorBordeMenu);
}
