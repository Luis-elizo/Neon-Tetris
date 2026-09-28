#include "gameScreen.h"
#include "colors.h"
#include <string>

GameScreen::GameScreen() {
    cellSize = 35;       
    boardWidth = 10;     
    boardHeight = 20;    
    
    offsetX = (1000 - (boardWidth * cellSize)) / 2;
    offsetY = (900 - (boardHeight * cellSize)) / 2;
    mensajeAlerta = "";
    tiempoFinAlerta = 0.0f;
    
    botonReplaySalir = { 60, 825, 140, 45 };
    botonReplayAtras = { 240, 825, 150, 45 };
    botonReplayPlay = { 420, 825, 170, 45 };
    botonReplayAdelante = { 620, 825, 150, 45 };
    replayAtrasResaltado = false;
    replayPlayResaltado = false;
    replayAdelanteResaltado = false;
    replaySalirResaltado = false;
}

void GameScreen::setAlerta(std::string mensaje, float tiempoFin) {
    mensajeAlerta = mensaje;
    tiempoFinAlerta = tiempoFin;
}

void GameScreen::Draw(Tablero& tablero, Pieza& piezaActual, int puntaje, Cola& colaSiguientes, Pila& pilaHold, float tiempoPartida, bool animandoLimpieza, float tiempoAnimacion) {
    ClearBackground(NeonColors::FONDO);

    // borde del tablero
    DrawRectangleLinesEx({ (float)offsetX - 5, (float)offsetY - 5, (float)(boardWidth * cellSize) + 10, (float)(boardHeight * cellSize) + 10 }, 5, NeonColors::CYAN);
    
    // cuadricula del tablero
    for (int colGrid = 0; colGrid < boardWidth; colGrid++) {
        for (int filaGrid = 0; filaGrid < boardHeight; filaGrid++) {
            DrawRectangleLines(offsetX + colGrid * cellSize, offsetY + filaGrid * cellSize, cellSize, cellSize, {50, 50, 60, 255});
        }
    }

    // dibuja los bloques fijos
    for (int fila = 0; fila < boardHeight; fila++) {
        // parpadeo si se lleno la fila
        bool filaLlenaAnimada = animandoLimpieza && tablero.esFilaLlena(fila);
        
        for (int columna = 0; columna < boardWidth; columna++) {
            int colorId = tablero.getCelda(fila, columna);
            if (colorId > 0) {
                Color colorBloque = NeonColors::GetPieceColor(colorId);
                if (filaLlenaAnimada) {
                    if (((int)(tiempoAnimacion * 24) % 2) == 0) {
                        colorBloque = RAYWHITE;
                    } else {
                        colorBloque = NeonColors::ROSA;
                    }
                }
                DrawRectangle(offsetX + columna * cellSize, offsetY + fila * cellSize, cellSize, cellSize, colorBloque);
                DrawRectangleLines(offsetX + columna * cellSize, offsetY + fila * cellSize, cellSize, cellSize, {255, 255, 255, 50});
            }
        }
    }

    // dibuja la pieza que va cayendo
    if (!animandoLimpieza) {
        for (int bloque = 0; bloque < 4; bloque++) {
            Posicion pos = piezaActual.getPosicionBloque(bloque);
            if (pos.fila >= 0 && pos.fila < boardHeight && pos.col >= 0 && pos.col < boardWidth) {
                Color colorBloque = NeonColors::GetPieceColor(piezaActual.getColorId());
                DrawRectangle(offsetX + pos.col * cellSize, offsetY + pos.fila * cellSize, cellSize, cellSize, colorBloque);
                DrawRectangleLines(offsetX + pos.col * cellSize, offsetY + pos.fila * cellSize, cellSize, cellSize, {255, 255, 255, 50});
            }
        }
    }

    // cuadro de hold
    int holdX = 80;
    int holdY = offsetY;
    DrawText("HOLD", holdX + 35, holdY - 40, 30, NeonColors::MORADO);
    DrawRectangleLinesEx({ (float)holdX, (float)holdY, 150, 150 }, 3, NeonColors::MORADO);

    // dibuja la pieza guardada
    if (!pilaHold.estaVacia()) {
        Pieza piezaHold(pilaHold.verCima());
        for (int bloque = 0; bloque < 4; bloque++) {
            Posicion pos = piezaHold.getPosicionBloque(bloque);
            Color colorBloque = NeonColors::GetPieceColor(piezaHold.getColorId());
            int pixelX = holdX + 40 + (pos.col - 4) * cellSize;
            int pixelY = holdY + 50 + pos.fila * cellSize;
            DrawRectangle(pixelX, pixelY, cellSize, cellSize, colorBloque);
            DrawRectangleLines(pixelX, pixelY, cellSize, cellSize, {255, 255, 255, 50});
        }
    }

    // texto de controles
    int panelY = holdY + 190;
    DrawText("CONTROLES", holdX + 10, panelY, 20, NeonColors::CYAN);
    DrawText("<- / -> : Mover", holdX, panelY + 30, 16, NeonColors::BLANCO_SUAVE);
    DrawText("Arriba  : Rotar", holdX, panelY + 55, 16, NeonColors::BLANCO_SUAVE);
    DrawText("Abajo   : Caida", holdX, panelY + 80, 16, NeonColors::BLANCO_SUAVE);
    DrawText("RShift  : Hold", holdX, panelY + 105, 16, NeonColors::BLANCO_SUAVE);
    DrawText("Z       : Deshacer", holdX, panelY + 130, 16, NeonColors::AMARILLO);
    DrawText("Y       : Rehacer", holdX, panelY + 155, 16, NeonColors::AMARILLO);
    DrawText("Esc     : Pausa", holdX, panelY + 180, 16, NeonColors::BLANCO_SUAVE);

    // cuadro de siguientes piezas
    int nextX = offsetX + (boardWidth * cellSize) + 50;
    int nextY = offsetY;
    DrawText("SIGUIENTES", nextX + 10, nextY - 40, 30, NeonColors::ROSA);
    DrawRectangleLinesEx({ (float)nextX, (float)nextY, 180, 400 }, 3, NeonColors::ROSA);

    // dibuja las proximas 3 piezas
    if (!colaSiguientes.estaVacia()) {
        int maxSiguientes = colaSiguientes.getTamano() < 3 ? colaSiguientes.getTamano() : 3;
        for (int indicePieza = 0; indicePieza < maxSiguientes; indicePieza++) {
            Pieza sigPieza(colaSiguientes.obtenerEn(indicePieza));
            for (int bloque = 0; bloque < 4; bloque++) {
                Posicion pos = sigPieza.getPosicionBloque(bloque);
                Color colorBloque = NeonColors::GetPieceColor(sigPieza.getColorId());
                int pixelX = nextX + 50 + (pos.col - 4) * cellSize;
                int pixelY = nextY + 60 + pos.fila * cellSize + (indicePieza * 110);
                DrawRectangle(pixelX, pixelY, cellSize, cellSize, colorBloque);
                DrawRectangleLines(pixelX, pixelY, cellSize, cellSize, {255, 255, 255, 50});
            }
        }
    }

    // cuadro de puntaje
    int scoreY = nextY + 450;
    DrawText("PUNTAJE", nextX + 25, scoreY, 30, NeonColors::CYAN);
    DrawRectangleLinesEx({ (float)nextX, (float)scoreY + 40, 180, 60 }, 3, NeonColors::CYAN);
    
    std::string scoreStr = std::to_string(puntaje);
    DrawText(scoreStr.c_str(), nextX + 20, scoreY + 50, 40, NeonColors::BLANCO_SUAVE);
    
    // mensaje del evento sorpresa
    if (tiempoPartida < tiempoFinAlerta) {
        int anchoMensaje = MeasureText(mensajeAlerta.c_str(), 40);
        DrawText(mensajeAlerta.c_str(), 500 - (anchoMensaje / 2), 830, 40, NeonColors::AMARILLO);
    }
}

int GameScreen::UpdateReplay() {
    // revisa si el mouse esta encima
    Vector2 mouse = GetMousePosition();
    replaySalirResaltado = CheckCollisionPointRec(mouse, botonReplaySalir);
    replayAtrasResaltado = CheckCollisionPointRec(mouse, botonReplayAtras);
    replayPlayResaltado = CheckCollisionPointRec(mouse, botonReplayPlay);
    replayAdelanteResaltado = CheckCollisionPointRec(mouse, botonReplayAdelante);

    // clic en los botones
    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
        if (replayAtrasResaltado) return 1;    // atras
        if (replayPlayResaltado) return 2;     // play o pausa
        if (replayAdelanteResaltado) return 3; // adelante
        if (replaySalirResaltado) return 4;    // salir al menu
    }
    return 0;
}

void GameScreen::DrawReplay(NodoHistorial* estadoReplay, bool reproduciendoAuto) {
    ClearBackground(NeonColors::FONDO);

    // borde del tablero
    DrawRectangleLinesEx({ (float)offsetX - 5, (float)offsetY - 5, (float)(boardWidth * cellSize) + 10, (float)(boardHeight * cellSize) + 10 }, 5, NeonColors::CYAN);
    
    // cuadricula
    for (int colGrid = 0; colGrid < boardWidth; colGrid++) {
        for (int filaGrid = 0; filaGrid < boardHeight; filaGrid++) {
            DrawRectangleLines(offsetX + colGrid * cellSize, offsetY + filaGrid * cellSize, cellSize, cellSize, {50, 50, 60, 255});
        }
    }

    // dibuja los bloques del turno
    if (estadoReplay != nullptr) {
        for (int fila = 0; fila < boardHeight; fila++) {
            for (int columna = 0; columna < boardWidth; columna++) {
                int colorId = estadoReplay->estado[fila][columna];
                if (colorId > 0) {
                    Color colorBloque = NeonColors::GetPieceColor(colorId);
                    DrawRectangle(offsetX + columna * cellSize, offsetY + fila * cellSize, cellSize, cellSize, colorBloque);
                    DrawRectangleLines(offsetX + columna * cellSize, offsetY + fila * cellSize, cellSize, cellSize, {255, 255, 255, 50});
                }
            }
        }
        
        // puntaje en ese turno
        int nextX = offsetX + (boardWidth * cellSize) + 50;
        int scoreY = offsetY + 450;
        DrawText("PUNTAJE", nextX + 25, scoreY, 30, NeonColors::CYAN);
        DrawRectangleLinesEx({ (float)nextX, (float)scoreY + 40, 180, 60 }, 3, NeonColors::CYAN);
        
        std::string scoreStr = std::to_string(estadoReplay->puntaje);
        DrawText(scoreStr.c_str(), nextX + 20, scoreY + 50, 40, NeonColors::BLANCO_SUAVE);
    }
    
    // titulo e instrucciones
    DrawText("MODO REPLAY", 30, 30, 36, NeonColors::ROSA);
    DrawText("Puedes usar las flechas o los botones:", 30, 75, 18, NeonColors::BLANCO_SUAVE);
    DrawText("<- / ->  : Navegar paso a paso", 30, 100, 18, NeonColors::BLANCO_SUAVE);
    DrawText("Espacio  : Reproducir / Pausar", 30, 125, 18, NeonColors::BLANCO_SUAVE);
    DrawText("M        : Salir al Menu", 30, 150, 18, NeonColors::BLANCO_SUAVE);

    // boton salir
    Color colorSalir = replaySalirResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonReplaySalir, NeonColors::FONDO);
    DrawRectangleLinesEx(botonReplaySalir, 2, colorSalir);
    int anchoSalir = MeasureText("SALIR", 20);
    DrawText("SALIR", botonReplaySalir.x + (botonReplaySalir.width - anchoSalir) / 2, botonReplaySalir.y + 13, 20, colorSalir);

    // boton atras
    Color colorAtras = replayAtrasResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonReplayAtras, NeonColors::FONDO);
    DrawRectangleLinesEx(botonReplayAtras, 2, colorAtras);
    int anchoAtras = MeasureText("<- ATRAS", 20);
    DrawText("<- ATRAS", botonReplayAtras.x + (botonReplayAtras.width - anchoAtras) / 2, botonReplayAtras.y + 13, 20, colorAtras);

    // boton reproducir o pausar
    Color colorPlay = reproduciendoAuto ? NeonColors::AMARILLO : (replayPlayResaltado ? NeonColors::ROSA : NeonColors::CYAN);
    DrawRectangleRec(botonReplayPlay, NeonColors::FONDO);
    DrawRectangleLinesEx(botonReplayPlay, 2, colorPlay);
    std::string textoPlay = reproduciendoAuto ? "|| PAUSA" : "> REPRODUCIR";
    int anchoPlay = MeasureText(textoPlay.c_str(), 20);
    DrawText(textoPlay.c_str(), botonReplayPlay.x + (botonReplayPlay.width - anchoPlay) / 2, botonReplayPlay.y + 13, 20, colorPlay);

    // boton adelante
    Color colorAdelante = replayAdelanteResaltado ? NeonColors::ROSA : NeonColors::CYAN;
    DrawRectangleRec(botonReplayAdelante, NeonColors::FONDO);
    DrawRectangleLinesEx(botonReplayAdelante, 2, colorAdelante);
    int anchoAdelante = MeasureText("ADELANTE ->", 20);
    DrawText("ADELANTE ->", botonReplayAdelante.x + (botonReplayAdelante.width - anchoAdelante) / 2, botonReplayAdelante.y + 13, 20, colorAdelante);
}
