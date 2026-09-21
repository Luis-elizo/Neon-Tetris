#include "gameScreen.h"
#include "colors.h"
#include <string>

GameScreen::GameScreen() {
    cellSize = 35;       
    boardWidth = 10;     
    boardHeight = 20;    
    
    offsetX = (1000 - (boardWidth * cellSize)) / 2;
    offsetY = (900 - (boardHeight * cellSize)) / 2;
}

void GameScreen::Draw(const Tablero& tablero, const Pieza& piezaActual, int puntaje, const Cola& colaSiguientes, const Pila& pilaHold) {
    ClearBackground(NeonColors::FONDO);

    DrawRectangleLinesEx({ (float)offsetX - 5, (float)offsetY - 5, (float)(boardWidth * cellSize) + 10, (float)(boardHeight * cellSize) + 10 }, 5, NeonColors::CYAN);
    
    for (int i = 0; i < boardWidth; i++) {
        for (int j = 0; j < boardHeight; j++) {
            DrawRectangleLines(offsetX + i * cellSize, offsetY + j * cellSize, cellSize, cellSize, {50, 50, 60, 255});
        }
    }

    for (int fila = 0; fila < boardHeight; ++fila) {
        for (int col = 0; col < boardWidth; ++col) {
            int colorId = tablero.getCelda(fila, col);
            if (colorId > 0) {
                Color c = NeonColors::GetPieceColor(colorId);
                DrawRectangle(offsetX + col * cellSize, offsetY + fila * cellSize, cellSize, cellSize, c);
                DrawRectangleLines(offsetX + col * cellSize, offsetY + fila * cellSize, cellSize, cellSize, {255, 255, 255, 50});
            }
        }
    }

    for (int i = 0; i < 4; ++i) {
        Posicion pos = piezaActual.getPosicionBloque(i);
        if (pos.fila >= 0 && pos.fila < boardHeight && pos.col >= 0 && pos.col < boardWidth) {
            Color c = NeonColors::GetPieceColor(piezaActual.getColorId());
            DrawRectangle(offsetX + pos.col * cellSize, offsetY + pos.fila * cellSize, cellSize, cellSize, c);
            DrawRectangleLines(offsetX + pos.col * cellSize, offsetY + pos.fila * cellSize, cellSize, cellSize, {255, 255, 255, 50});
        }
    }

    int holdX = 80;
    int holdY = offsetY;
    DrawText("HOLD", holdX + 35, holdY - 40, 30, NeonColors::MORADO);
    DrawRectangleLinesEx({ (float)holdX, (float)holdY, 150, 150 }, 3, NeonColors::MORADO);

    if (!pilaHold.estaVacia()) {
        Pieza piezaHold(pilaHold.verCima());
        for (int i = 0; i < 4; ++i) {
            Posicion pos = piezaHold.getPosicionBloque(i);
            Color c = NeonColors::GetPieceColor(piezaHold.getColorId());
            int px = holdX + 40 + (pos.col - 4) * cellSize;
            int py = holdY + 50 + pos.fila * cellSize;
            DrawRectangle(px, py, cellSize, cellSize, c);
            DrawRectangleLines(px, py, cellSize, cellSize, {255, 255, 255, 50});
        }
    }

    int nextX = offsetX + (boardWidth * cellSize) + 50;
    int nextY = offsetY;
    DrawText("SIGUIENTES", nextX + 10, nextY - 40, 30, NeonColors::ROSA);
    DrawRectangleLinesEx({ (float)nextX, (float)nextY, 180, 400 }, 3, NeonColors::ROSA);

    if (!colaSiguientes.estaVacia()) {
        int maxSiguientes = colaSiguientes.getTamano() < 3 ? colaSiguientes.getTamano() : 3;
        for (int k = 0; k < maxSiguientes; ++k) {
            Pieza sigPieza(colaSiguientes.obtenerEn(k));
            for (int i = 0; i < 4; ++i) {
                Posicion pos = sigPieza.getPosicionBloque(i);
                Color c = NeonColors::GetPieceColor(sigPieza.getColorId());
                int px = nextX + 50 + (pos.col - 4) * cellSize;
                int py = nextY + 60 + pos.fila * cellSize + (k * 110);
                DrawRectangle(px, py, cellSize, cellSize, c);
                DrawRectangleLines(px, py, cellSize, cellSize, {255, 255, 255, 50});
            }
        }
    }

    int scoreY = nextY + 450;
    DrawText("PUNTAJE", nextX + 25, scoreY, 30, NeonColors::CYAN);
    DrawRectangleLinesEx({ (float)nextX, (float)scoreY + 40, 180, 60 }, 3, NeonColors::CYAN);
    
    std::string scoreStr = std::to_string(puntaje);
    DrawText(scoreStr.c_str(), nextX + 20, scoreY + 50, 40, NeonColors::BLANCO_SUAVE);
}
