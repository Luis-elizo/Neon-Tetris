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

TipoPieza Cola::obtenerEn(int indice) const {
    NodoCola* aux = primero;
    int contador = 0;
    while (aux != nullptr && contador < indice) {
        aux = aux->siguiente;
        contador++;
    }
    if (aux != nullptr) {
        return aux->dato;
    }
    return TipoPieza::I; 
}

bool Cola::estaVacia() const {
    return primero == nullptr;
}

int Cola::getTamano() const {
    return tamano;
}
