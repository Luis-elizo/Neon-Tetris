#ifndef TABLERO_H
#define TABLERO_H

#include "../logica/Pieza.h"

// celda individual del tablero
struct NodoCelda {
    int color; // color del bloque (0 si esta vacio)
    NodoCelda* siguiente; // celda de la derecha
    
    NodoCelda(int colorInicial = 0) {
        color = colorInicial;
        siguiente = nullptr;
    }
};

// fila del tablero
struct NodoFila {
    NodoCelda* primerCelda; // primera celda de la izquierda
    NodoFila* siguiente;    // fila de abajo
    
    NodoFila() {
        primerCelda = nullptr;
        siguiente = nullptr;
    }
};

// tablero del juego
class Tablero {
private:
    NodoFila* cabeza; // primera fila de arriba
    int filas;        // total de filas (20)
    int columnas;     // total de columnas (10)

    NodoCelda* crearFilaVacia(); // crea una fila de 10 celdas vacias

public:
    Tablero(int numFilas = 20, int numColumnas = 10);
    ~Tablero();

    int getCelda(int fila, int columna); // devuelve el color de una celda
    void setCelda(int fila, int columna, int color); // le cambia el color a una celda

    bool hayColision(Pieza& pieza);       // revisa si choca con bordes o bloques
    void fijarPieza(Pieza& pieza);        // pega la pieza en el tablero
    int limpiarLineas();                  // borra las filas llenas y baja las demas
    bool hayLineasCompletas();            // revisa si hay alguna fila llena
    bool esFilaLlena(int filaIndex);      // revisa si una fila especifica esta llena
    
    void agregarLineaBasura();            // mete una fila con hueco abajo
    
    void cargarEstado(int estado[20][10]); // carga las celdas desde una matriz
};

#endif
