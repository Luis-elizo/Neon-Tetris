#include "Pila.h"

Pila::Pila() {
    // empieza vacia
    cima = nullptr;
    tamano = 0;
}

Pila::~Pila() {
    // vacia toda la pila
    while (!estaVacia()) {
        desapilar();
    }
}

void Pila::apilar(TipoPieza elemento) {
    // pone el nodo nuevo arriba
    NodoPila* nuevo = new NodoPila(elemento);
    nuevo->siguiente = cima;
    cima = nuevo;
    tamano++;
}

TipoPieza Pila::desapilar() {
    if (estaVacia()) {
        return TipoPieza::I;
    }
    
    // saca el de arriba y lo borra
    NodoPila* nodoAEliminar = cima;
    TipoPieza dato = nodoAEliminar->dato;
    cima = cima->siguiente;
    
    delete nodoAEliminar;
    tamano--;
    return dato;
}

TipoPieza Pila::verCima() {
    // mira la pieza de arriba sin sacarla
    if (estaVacia()) return TipoPieza::I;
    return cima->dato;
}

bool Pila::estaVacia() {
    return cima == nullptr;
}

int Pila::getTamano() {
    return tamano;
}
