#ifndef PILA_H
#define PILA_H

#include "../logica/Pieza.h"

// nodo para la pila
struct NodoPila {
    TipoPieza dato; // tipo de pieza guardada
    NodoPila* siguiente; // puntero al siguiente nodo
    
    NodoPila(TipoPieza valorPieza) {
        dato = valorPieza;
        siguiente = nullptr;
    }
};

// pila para la pieza guardada en hold
class Pila {
private:
    NodoPila* cima; // pieza de arriba
    int tamano;     // cantidad de elementos

public:
    Pila();
    ~Pila();

    void apilar(TipoPieza elemento); // guarda una pieza arriba
    TipoPieza desapilar();          // saca la pieza de arriba
    TipoPieza verCima();            // mira la pieza guardada sin sacarla
    bool estaVacia();               // revisa si no hay nada guardado
    int getTamano();                // tamaño de la pila
};

#endif
