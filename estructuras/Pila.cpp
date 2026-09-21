#include "Pila.h"

Pila::Pila() {
    cima = nullptr;
    tamano = 0;
}

Pila::~Pila() {
    while (!estaVacia()) {
        desapilar();
    }
}

void Pila::apilar(TipoPieza elemento) {
    NodoPila* nuevo = new NodoPila(elemento);
    nuevo->siguiente = cima;
    cima = nuevo;
    tamano++;
}

TipoPieza Pila::desapilar() {
    if (estaVacia()) {
        return TipoPieza::I;
    }
    
    NodoPila* aux = cima;
    TipoPieza dato = aux->dato;
    cima = cima->siguiente;
    
    delete aux;
    tamano--;
    return dato;
}

TipoPieza Pila::verCima() const {
    if (estaVacia()) return TipoPieza::I;
    return cima->dato;
}

bool Pila::estaVacia() const {
    return cima == nullptr;
}

int Pila::getTamano() const {
    return tamano;
}
