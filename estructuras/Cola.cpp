#include "Cola.h"

Cola::Cola() {
    primero = nullptr;
    ultimo = nullptr;
    tamano = 0;
}

Cola::~Cola() {
    while (!estaVacia()) {
        desencolar();
    }
}

void Cola::encolar(TipoPieza elemento) {
    NodoCola* nuevo = new NodoCola(elemento);
    if (estaVacia()) {
        primero = nuevo;
        ultimo = nuevo;
    } else {
        ultimo->siguiente = nuevo;
        ultimo = nuevo;
    }
    tamano++;
}

TipoPieza Cola::desencolar() {
    if (estaVacia()) {
        return TipoPieza::I; 
    }
    
    NodoCola* aux = primero;
    TipoPieza dato = aux->dato;
    primero = primero->siguiente;
    
    if (primero == nullptr) {
        ultimo = nullptr;
    }
    
    delete aux;
    tamano--;
    return dato;
}

TipoPieza Cola::verPrimero() const {
    if (estaVacia()) return TipoPieza::I;
    return primero->dato;
}

bool Cola::estaVacia() const {
    return primero == nullptr;
}

int Cola::getTamano() const {
    return tamano;
}
