#ifndef PIEZA_H
#define PIEZA_H

enum class TipoPieza {
    I = 0, O, T, S, Z, J, L
};

// Estructura simple para manejar coordenadas
struct Posicion {
    int fila;
    int col;
};

class Pieza {
private:
    TipoPieza tipo;
    int rotacionActual; // Valores del 0 al 3 (4 orientaciones)
    int filaOriginal;   // Posicion Y actual de la pieza en el tablero
    int colOriginal;    // Posicion X actual de la pieza en el tablero
    int colorId;        // ID del color (para dibujar luego)

    // Almacenamos las 4 orientaciones precalculadas. 
    // Cada orientacion tiene 4 bloques (Posiciones relativas).
    Posicion orientaciones[4][4]; 

    // Metodo privado para inicializar la forma segun el TipoPieza
    void inicializarForma();

public:
    Pieza(TipoPieza t = TipoPieza::I); // Constructor por defecto

    // Movimiento basico
    void mover(int dFila, int dCol);
    void rotar();
    void deshacerRotacion(); // Util si al rotar hay colision

    // Getters y Setters
    TipoPieza getTipo() const;
    int getFilaOriginal() const;
    int getColOriginal() const;
    int getColorId() const;
    
    // Obtener la posicion ABSOLUTA (fila/col en tablero) del bloque i (0 a 3)
    Posicion getPosicionBloque(int bloqueIdx) const;
    
    void setPosicion(int fila, int col);
};

#endif
