#include "rankingScreen.h"
#include "colors.h"
#include <string>
#include <chrono>
#include <cstdio>

RankingScreen::RankingScreen() {
    // posiciones de los botones
    botonVolver = { 400, 800, 200, 50 };
    botonBubble = { 220, 145, 260, 45 };
    botonMerge = { 520, 145, 260, 45 };
    
    volverResaltado = false;
    bubbleResaltado = false;
    mergeResaltado = false;
    
    algoritmoActivo = 0; // empieza con burbuja
    tiempoNano = 0;
    tiempoMicro = 0.0;
}

void RankingScreen::EjecutarOrdenamiento() {
    // toma el tiempo de inicio
    auto inicio = std::chrono::high_resolution_clock::now();
    if (algoritmoActivo == 0) {
        Ordenamientos::ordenarBurbuja(listaActual);
    } else {
        Ordenamientos::ordenarMergeSort(listaActual);
    }
    auto fin = std::chrono::high_resolution_clock::now();
    
    // calcula cuanto duro
    tiempoNano = std::chrono::duration_cast<std::chrono::nanoseconds>(fin - inicio).count();
    tiempoMicro = tiempoNano / 1000.0;
}

void RankingScreen::CargarPuntajes() {
    // carga los datos y los ordena
    listaActual = ManejadorJSON::cargar("scores.json");
    EjecutarOrdenamiento();
}

bool RankingScreen::Update() {
    Vector2 mouse = GetMousePosition();
    volverResaltado = CheckCollisionPointRec(mouse, botonVolver);
    bubbleResaltado = CheckCollisionPointRec(mouse, botonBubble);
    mergeResaltado = CheckCollisionPointRec(mouse, botonMerge);

    // clic en los botones
    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
        if (volverResaltado) {
            return true; // volver al menu
        }
        if (bubbleResaltado) {
            algoritmoActivo = 0;
            listaActual = ManejadorJSON::cargar("scores.json");
            EjecutarOrdenamiento();
        }
        if (mergeResaltado) {
            algoritmoActivo = 1;
            listaActual = ManejadorJSON::cargar("scores.json");
            EjecutarOrdenamiento();
        }
    }
    return false;
}

void RankingScreen::Draw() {
    ClearBackground(NeonColors::FONDO);

    std::string titulo = "MEJORES PUNTAJES";
    int anchoTitulo = MeasureText(titulo.c_str(), 48);
    DrawText(titulo.c_str(), (1000 - anchoTitulo) / 2, 55, 48, NeonColors::ROSA);

    Color colorBubble = (algoritmoActivo == 0) ? NeonColors::CYAN : (bubbleResaltado ? NeonColors::BLANCO_SUAVE : DARKGRAY);
    DrawRectangleLinesEx(botonBubble, 2, colorBubble);
    DrawText("Bubble Sort O(n^2)", botonBubble.x + 25, botonBubble.y + 12, 20, colorBubble);

    Color colorMerge = (algoritmoActivo == 1) ? NeonColors::CYAN : (mergeResaltado ? NeonColors::BLANCO_SUAVE : DARKGRAY);
    DrawRectangleLinesEx(botonMerge, 2, colorMerge);
    DrawText("Merge Sort O(n log n)", botonMerge.x + 15, botonMerge.y + 12, 20, colorMerge);

    char bufferTiempo[120];
    sprintf(bufferTiempo, "Tiempo de ordenamiento: %lld ns (%.2f us)", tiempoNano, tiempoMicro);
    int anchoTiempo = MeasureText(bufferTiempo, 18);
    DrawText(bufferTiempo, (1000 - anchoTiempo) / 2, 200, 18, NeonColors::AMARILLO);

    DrawRectangleLinesEx({ 200, 228, 600, 532 }, 2, NeonColors::MORADO);

    DrawText("POS", 240, 240, 22, NeonColors::CYAN);
    DrawText("JUGADOR", 420, 240, 22, NeonColors::CYAN);
    DrawText("PUNTAJE", 640, 240, 22, NeonColors::CYAN);
    DrawLine(220, 275, 780, 275, NeonColors::MORADO);

    if (listaActual.cantidad == 0) {
        std::string sinDatos = "Sin puntajes registrados";
        int anchoSin = MeasureText(sinDatos.c_str(), 24);
        DrawText(sinDatos.c_str(), (1000 - anchoSin) / 2, 450, 24, DARKGRAY);
    } else {
        int posY = 295;
        for (int indicePuntaje = 0; indicePuntaje < listaActual.cantidad && indicePuntaje < 10; indicePuntaje++) {
            Color colorFila = NeonColors::BLANCO_SUAVE;
            if (indicePuntaje == 0) colorFila = NeonColors::AMARILLO;
            else if (indicePuntaje == 1) colorFila = NeonColors::CYAN;
            else if (indicePuntaje == 2) colorFila = NeonColors::ROSA;

            std::string textoPosicion = "#" + std::to_string(indicePuntaje + 1);
            DrawText(textoPosicion.c_str(), 245, posY, 22, colorFila);

            std::string textoNombre = listaActual.registros[indicePuntaje].nombre;
            if (textoNombre.empty()) textoNombre = "ANONIMO";
            DrawText(textoNombre.c_str(), 420, posY, 22, colorFila);

            std::string textoPuntaje = std::to_string(listaActual.registros[indicePuntaje].puntaje);
            DrawText(textoPuntaje.c_str(), 640, posY, 22, colorFila);

            posY += 44;
        }
    }

    Color colorVolver = volverResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonVolver, NeonColors::FONDO);
    DrawRectangleLinesEx(botonVolver, 3, colorVolver);
    int anchoVolver = MeasureText("VOLVER", 24);
    DrawText("VOLVER", botonVolver.x + (botonVolver.width - anchoVolver) / 2, botonVolver.y + 13, 24, colorVolver);
}
