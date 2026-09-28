#include "Pieza.h"

Pieza::Pieza(TipoPieza tipoPieza) {
    tipo = tipoPieza;
    rotacionActual = 0;
    filaOriginal = 0;
    colOriginal = 3; 
    colorId = static_cast<int>(tipoPieza) + 1;

    inicializarForma();
}

void Pieza::inicializarForma() {
    switch (tipo) {
        case TipoPieza::I:
            orientaciones[0][0] = {1, 0}; orientaciones[0][1] = {1, 1}; orientaciones[0][2] = {1, 2}; orientaciones[0][3] = {1, 3};
            orientaciones[1][0] = {0, 2}; orientaciones[1][1] = {1, 2}; orientaciones[1][2] = {2, 2}; orientaciones[1][3] = {3, 2};
            orientaciones[2][0] = {2, 0}; orientaciones[2][1] = {2, 1}; orientaciones[2][2] = {2, 2}; orientaciones[2][3] = {2, 3};
            orientaciones[3][0] = {0, 1}; orientaciones[3][1] = {1, 1}; orientaciones[3][2] = {2, 1}; orientaciones[3][3] = {3, 1};
            break;
            
        case TipoPieza::O:
            for (int orientacion = 0; orientacion < 4; orientacion++) {
                orientaciones[orientacion][0] = {0, 0}; orientaciones[orientacion][1] = {0, 1}; 
                orientaciones[orientacion][2] = {1, 0}; orientaciones[orientacion][3] = {1, 1};
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

void Pieza::mover(int deltaFila, int deltaColumna) {
    // mueve la posicion de la pieza
    filaOriginal += deltaFila;
    colOriginal += deltaColumna;
}

void Pieza::rotar() {
    // cambia al siguiente giro
    rotacionActual = (rotacionActual + 1) % 4;
}

void Pieza::deshacerRotacion() {
    // si choco, vuelve al giro de antes
    rotacionActual = (rotacionActual - 1 + 4) % 4;
}

TipoPieza Pieza::getTipo() { return tipo; }
int Pieza::getFilaOriginal() { return filaOriginal; }
int Pieza::getColOriginal() { return colOriginal; }
int Pieza::getColorId() { return colorId; }

void Pieza::setPosicion(int nuevaFila, int nuevaColumna) {
    // cambia las coordenadas
    filaOriginal = nuevaFila;
    colOriginal = nuevaColumna;
}

Posicion Pieza::getPosicionBloque(int bloqueIdx) {
    // calcula donde queda el bloque en el tablero
    Posicion relativa = orientaciones[rotacionActual][bloqueIdx];
    return { filaOriginal + relativa.fila, colOriginal + relativa.col };
}
