#ifndef COLA_H
#define COLA_H

#include "../logica/Pieza.h"

// nodo para la cola
struct NodoCola {
    TipoPieza dato; // tipo de pieza
    NodoCola* siguiente; // puntero al siguiente nodo
    
    NodoCola(TipoPieza valorPieza) {
        dato = valorPieza;
        siguiente = nullptr;
    }
};

// cola para las piezas que van a salir
class Cola {
private:
    NodoCola* primero; // el primer nodo
    NodoCola* ultimo;  // el ultimo nodo
    int tamano;        // cuantas piezas hay

public:
    Cola();
    ~Cola();

    void encolar(TipoPieza elemento);    // mete una pieza al final
    TipoPieza desencolar();             // saca la que sigue
    TipoPieza verPrimero();             // mira la que sigue sin sacarla
    TipoPieza obtenerEn(int indice);     // busca la pieza por posicion
    bool estaVacia();                    // revisa si no tiene nada
    int getTamano();                     // tamaño de la cola
};

#endif
