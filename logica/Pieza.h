#ifndef PIEZA_H
#define PIEZA_H

// las 7 piezas del tetris
enum class TipoPieza {
    I = 0, O, T, S, Z, J, L
};

// coordenadas de una celda
struct Posicion {
    int fila;   // posicion en fila
    int col;    // posicion en columna
};
	
// pieza que esta cayendo
class Pieza {
private:
    TipoPieza tipo;         // que pieza es
    int rotacionActual;     // rotacion de 0 a 3
    int filaOriginal;       // fila donde esta
    int colOriginal;        // columna donde esta
    int colorId;            // id del color

    Posicion orientaciones[4][4]; // los 4 bloques en sus 4 rotaciones

    void inicializarForma(); // arma las coordenadas de los bloques

public:
    Pieza(TipoPieza tipoPieza = TipoPieza::I);

    void mover(int deltaFila, int deltaColumna); // mueve la pieza
    void rotar();                               // gira la pieza
    void deshacerRotacion();                    // regresa al giro anterior si choca

    TipoPieza getTipo();                        // tipo de pieza
    int getFilaOriginal();                      // fila actual
    int getColOriginal();                       // columna actual
    int getColorId();                           // color de la pieza
    
    Posicion getPosicionBloque(int bloqueIdx);  // posicion de uno de sus 4 bloques
    
    void setPosicion(int nuevaFila, int nuevaColumna); // cambia la posicion
};

#endif
