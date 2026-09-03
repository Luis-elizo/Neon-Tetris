#include "Pieza.h"

Pieza::Pieza(TipoPieza t) {
    tipo = t;
    rotacionActual = 0;
    
    // Posicion inicial tipica de una pieza en Tetris (centro arriba)
    filaOriginal = 0;
    colOriginal = 3; 

    // Asignamos un ID de color segun el tipo (1 al 7)
    colorId = static_cast<int>(t) + 1;

    inicializarForma();
}

void Pieza::inicializarForma() {
    // Definimos las 4 orientaciones para cada bloque
    // Las coordenadas (fila, col) son relativas a la posicion original.
    
    switch (tipo) {
        case TipoPieza::I:
            orientaciones[0][0] = {1, 0}; orientaciones[0][1] = {1, 1}; orientaciones[0][2] = {1, 2}; orientaciones[0][3] = {1, 3};
            orientaciones[1][0] = {0, 2}; orientaciones[1][1] = {1, 2}; orientaciones[1][2] = {2, 2}; orientaciones[1][3] = {3, 2};
            orientaciones[2][0] = {2, 0}; orientaciones[2][1] = {2, 1}; orientaciones[2][2] = {2, 2}; orientaciones[2][3] = {2, 3};
            orientaciones[3][0] = {0, 1}; orientaciones[3][1] = {1, 1}; orientaciones[3][2] = {2, 1}; orientaciones[3][3] = {3, 1};
            break;
            
        case TipoPieza::O:
            // La pieza O no rota realmente, es igual en las 4 orientaciones
            for (int i = 0; i < 4; ++i) {
                orientaciones[i][0] = {0, 0}; orientaciones[i][1] = {0, 1}; 
                orientaciones[i][2] = {1, 0}; orientaciones[i][3] = {1, 1};
            }
            break;
            
        case TipoPieza::T:
            orientaciones[0][0] = {0, 1}; orientaciones[0][1] = {1, 0}; orientaciones[0][2] = {1, 1}; orientaciones[0][3] = {1, 2};
            orientaciones[1][0] = {0, 1}; orientaciones[1][1] = {1, 1}; orientaciones[1][2] = {2, 1}; orientaciones[1][3] = {1, 2};
            orientaciones[2][0] = {1, 0}; orientaciones[2][1] = {1, 1}; orientaciones[2][2] = {1, 2}; orientaciones[2][3] = {2, 1};
            orientaciones[3][0] = {0, 1}; orientaciones[3][1] = {1, 0}; orientaciones[3][2] = {1, 1}; orientaciones[3][3] = {2, 1};
            break;
            
        case TipoPieza::S:
            orientaciones[0][0] = {0, 1}; orientaciones[0][1] = {0, 2}; orientaciones[0][2] = {1, 0}; orientaciones[0][3] = {1, 1};
            orientaciones[1][0] = {0, 1}; orientaciones[1][1] = {1, 1}; orientaciones[1][2] = {1, 2}; orientaciones[1][3] = {2, 2};
            orientaciones[2][0] = {1, 1}; orientaciones[2][1] = {1, 2}; orientaciones[2][2] = {2, 0}; orientaciones[2][3] = {2, 1};
            orientaciones[3][0] = {0, 0}; orientaciones[3][1] = {1, 0}; orientaciones[3][2] = {1, 1}; orientaciones[3][3] = {2, 1};
            break;
            
        case TipoPieza::Z:
            orientaciones[0][0] = {0, 0}; orientaciones[0][1] = {0, 1}; orientaciones[0][2] = {1, 1}; orientaciones[0][3] = {1, 2};
            orientaciones[1][0] = {0, 2}; orientaciones[1][1] = {1, 1}; orientaciones[1][2] = {1, 2}; orientaciones[1][3] = {2, 1};
            orientaciones[2][0] = {1, 0}; orientaciones[2][1] = {1, 1}; orientaciones[2][2] = {2, 1}; orientaciones[2][3] = {2, 2};
            orientaciones[3][0] = {0, 1}; orientaciones[3][1] = {1, 0}; orientaciones[3][2] = {1, 1}; orientaciones[3][3] = {2, 0};
            break;
            
        case TipoPieza::J:
            orientaciones[0][0] = {0, 0}; orientaciones[0][1] = {1, 0}; orientaciones[0][2] = {1, 1}; orientaciones[0][3] = {1, 2};
            orientaciones[1][0] = {0, 1}; orientaciones[1][1] = {0, 2}; orientaciones[1][2] = {1, 1}; orientaciones[1][3] = {2, 1};
            orientaciones[2][0] = {1, 0}; orientaciones[2][1] = {1, 1}; orientaciones[2][2] = {1, 2}; orientaciones[2][3] = {2, 2};
            orientaciones[3][0] = {0, 1}; orientaciones[3][1] = {1, 1}; orientaciones[3][2] = {2, 0}; orientaciones[3][3] = {2, 1};
            break;
            
        case TipoPieza::L:
            orientaciones[0][0] = {0, 2}; orientaciones[0][1] = {1, 0}; orientaciones[0][2] = {1, 1}; orientaciones[0][3] = {1, 2};
            orientaciones[1][0] = {0, 1}; orientaciones[1][1] = {1, 1}; orientaciones[1][2] = {2, 1}; orientaciones[1][3] = {2, 2};
            orientaciones[2][0] = {1, 0}; orientaciones[2][1] = {1, 1}; orientaciones[2][2] = {1, 2}; orientaciones[2][3] = {2, 0};
            orientaciones[3][0] = {0, 0}; orientaciones[3][1] = {0, 1}; orientaciones[3][2] = {1, 1}; orientaciones[3][3] = {2, 1};
            break;
    }
}

void Pieza::mover(int dFila, int dCol) {
    filaOriginal += dFila;
    colOriginal += dCol;
}

void Pieza::rotar() {
    rotacionActual = (rotacionActual + 1) % 4;
}

void Pieza::deshacerRotacion() {
    rotacionActual = (rotacionActual - 1 + 4) % 4; // +4 para evitar negativos
}

TipoPieza Pieza::getTipo() const { return tipo; }
int Pieza::getFilaOriginal() const { return filaOriginal; }
int Pieza::getColOriginal() const { return colOriginal; }
int Pieza::getColorId() const { return colorId; }

void Pieza::setPosicion(int fila, int col) {
    filaOriginal = fila;
    colOriginal = col;
}

Posicion Pieza::getPosicionBloque(int bloqueIdx) const {
    Posicion rel = orientaciones[rotacionActual][bloqueIdx];
    return { filaOriginal + rel.fila, colOriginal + rel.col };
}
