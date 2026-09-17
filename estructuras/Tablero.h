#ifndef TABLERO_H
#define TABLERO_H

#include "../logica/Pieza.h"

struct NodoCelda {
    int color;
    NodoCelda* siguiente;
    
    NodoCelda(int c = 0) {
        color = c;
        siguiente = nullptr;
    }
};

struct NodoFila {
    NodoCelda* primerCelda;
    NodoFila* siguiente;
    
    NodoFila() {
        primerCelda = nullptr;
        siguiente = nullptr;
    }
};

class Tablero {
private:
    NodoFila* cabeza;
    int filas;
    int columnas;

    NodoCelda* crearFilaVacia();

public:
    Tablero(int numFilas = 20, int numCols = 10);
    ~Tablero();

    int getCelda(int fila, int col) const;
    void setCelda(int fila, int col, int color);

    bool hayColision(const Pieza& pieza) const;
    void fijarPieza(const Pieza& pieza);
    int limpiarLineas();
};

#endif
