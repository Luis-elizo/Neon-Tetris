#ifndef PILA_H
#define PILA_H

#include "../logica/Pieza.h"

struct NodoPila {
    TipoPieza dato;
    NodoPila* siguiente;
    
    NodoPila(TipoPieza d) {
        dato = d;
        siguiente = nullptr;
    }
};

class Pila {
private:
    NodoPila* cima;
    int tamano;

public:
    Pila();
    ~Pila();

    void apilar(TipoPieza elemento);
    TipoPieza desapilar();
    TipoPieza verCima() const;
    bool estaVacia() const;
    int getTamano() const;
};

#endif
