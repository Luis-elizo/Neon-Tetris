#ifndef GAME_SCREEN_H
#define GAME_SCREEN_H

#include "raylib.h"

class GameScreen {
private:
    int cellSize;
    int boardWidth;
    int boardHeight;
    int offsetX;
    int offsetY;

public:
    GameScreen();
    void Draw();
};

#endif
