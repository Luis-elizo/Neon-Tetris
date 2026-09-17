#ifndef COLA_H
#define COLA_H

#include "../logica/Pieza.h"

struct NodoCola {
    TipoPieza dato;
    NodoCola* siguiente;
    
    NodoCola(TipoPieza d) {
        dato = d;
        siguiente = nullptr;
    }
};

class Cola {
private:
    NodoCola* primero;
    NodoCola* ultimo;
    int tamano;

public:
    Cola();
    ~Cola();

    void encolar(TipoPieza elemento);
    TipoPieza desencolar();
    TipoPieza verPrimero() const;
    bool estaVacia() const;
    int getTamano() const;
};

#endif
