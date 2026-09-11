#ifndef PIEZA_H
#define PIEZA_H

enum class TipoPieza {
    I = 0, O, T, S, Z, J, L
};

struct Posicion {
    int fila;
    int col;
};

class Pieza {
private:
    TipoPieza tipo;
    int rotacionActual;
    int filaOriginal;
    int colOriginal;
    int colorId;

    Posicion orientaciones[4][4]; 

    void inicializarForma();

public:
    Pieza(TipoPieza t = TipoPieza::I);

    void mover(int dFila, int dCol);
    void rotar();
    void deshacerRotacion();

    TipoPieza getTipo() const;
    int getFilaOriginal() const;
    int getColOriginal() const;
    int getColorId() const;
    
    Posicion getPosicionBloque(int bloqueIdx) const;
    
    void setPosicion(int fila, int col);
};

#endif
