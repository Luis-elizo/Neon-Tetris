#include "gameScreen.h"
#include "colors.h"

GameScreen::GameScreen() {
    cellSize = 35;       
    boardWidth = 10;     
    boardHeight = 20;    
    
    offsetX = (1000 - (boardWidth * cellSize)) / 2;
    offsetY = (900 - (boardHeight * cellSize)) / 2;
}

void GameScreen::Draw() {
    ClearBackground(NeonColors::FONDO);

    DrawRectangleLinesEx({ (float)offsetX - 5, (float)offsetY - 5, (float)(boardWidth * cellSize) + 10, (float)(boardHeight * cellSize) + 10 }, 5, NeonColors::CYAN);
    
    for (int i = 0; i < boardWidth; i++) {
        for (int j = 0; j < boardHeight; j++) {
            DrawRectangleLines(offsetX + i * cellSize, offsetY + j * cellSize, cellSize, cellSize, {50, 50, 60, 255});
        }
    }

    int holdX = 80;
    int holdY = offsetY;
    DrawText("HOLD", holdX + 35, holdY - 40, 30, NeonColors::MORADO);
    DrawRectangleLinesEx({ (float)holdX, (float)holdY, 150, 150 }, 3, NeonColors::MORADO);

    int nextX = offsetX + (boardWidth * cellSize) + 50;
    int nextY = offsetY;
    DrawText("SIGUIENTES", nextX + 10, nextY - 40, 30, NeonColors::ROSA);
    DrawRectangleLinesEx({ (float)nextX, (float)nextY, 180, 400 }, 3, NeonColors::ROSA);

    int scoreY = nextY + 450;
    DrawText("PUNTAJE", nextX + 25, scoreY, 30, NeonColors::CYAN);
    DrawRectangleLinesEx({ (float)nextX, (float)scoreY + 40, 180, 60 }, 3, NeonColors::CYAN);
    
    DrawText("0", nextX + 20, scoreY + 50, 40, NeonColors::BLANCO_SUAVE);
}
