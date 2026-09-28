#include "Cola.h"

Cola::Cola() {
    // empieza vacia
    primero = nullptr;
    ultimo = nullptr;
    tamano = 0;
}

Cola::~Cola() {
    // borra todos los nodos que queden
    while (!estaVacia()) {
        desencolar();
    }
}

void Cola::encolar(TipoPieza elemento) {
    NodoCola* nuevo = new NodoCola(elemento);
    // si no habia nada, el nuevo es el primero y el ultimo
    if (estaVacia()) {
        primero = nuevo;
        ultimo = nuevo;
    } else {
        // lo engancha al final
        ultimo->siguiente = nuevo;
        ultimo = nuevo;
    }
    tamano++;
}

TipoPieza Cola::desencolar() {
    if (estaVacia()) {
        return TipoPieza::I; 
    }
    
    // guarda el primero para borrarlo
    NodoCola* nodoAEliminar = primero;
    TipoPieza dato = nodoAEliminar->dato;
    primero = primero->siguiente;
    
    // si ya no queda nada, el ultimo tambien queda nulo
    if (primero == nullptr) {
        ultimo = nullptr;
    }
    
    delete nodoAEliminar; // borra el nodo
    tamano--;
    return dato;
}

TipoPieza Cola::verPrimero() {
    // devuelve el primero sin sacarlo
    if (estaVacia()) return TipoPieza::I;
    return primero->dato;
}

TipoPieza Cola::obtenerEn(int indice) {
    // busca la pieza en esa posicion
    NodoCola* nodoActual = primero;
    int contador = 0;
    while (nodoActual != nullptr && contador < indice) {
        nodoActual = nodoActual->siguiente;
        contador++;
    }
    if (nodoActual != nullptr) {
        return nodoActual->dato;
    }
    return TipoPieza::I; 
}

bool Cola::estaVacia() {
    return primero == nullptr;
}

int Cola::getTamano() {
    return tamano;
}
