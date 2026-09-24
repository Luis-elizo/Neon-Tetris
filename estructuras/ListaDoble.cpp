#include "ListaDoble.h"

ListaDoble::ListaDoble() {
    inicio = nullptr;
    final = nullptr;
    actual = nullptr;
}

ListaDoble::~ListaDoble() {
    vaciar();
}

void ListaDoble::vaciar() {
    NodoHistorial* temp = inicio;
    while (temp != nullptr) {
        NodoHistorial* borrar = temp;
        temp = temp->siguiente;
        delete borrar;
    }
    inicio = nullptr;
    final = nullptr;
    actual = nullptr;
}

void ListaDoble::agregarEstado(const Tablero& tablero, int puntaje) {
    NodoHistorial* nuevo = new NodoHistorial(puntaje);
    
    for (int i = 0; i < 20; ++i) {
        for (int j = 0; j < 10; ++j) {
            nuevo->estado[i][j] = tablero.getCelda(i, j);
        }
    }
    
    if (inicio == nullptr) {
        inicio = nuevo;
        final = nuevo;
    } else {
        final->siguiente = nuevo;
        nuevo->anterior = final;
        final = nuevo;
    }
    actual = final;
}

void ListaDoble::irAlInicio() {
    actual = inicio;
}

bool ListaDoble::avanzar() {
    if (actual != nullptr && actual->siguiente != nullptr) {
        actual = actual->siguiente;
        return true;
    }
    return false;
}

bool ListaDoble::retroceder() {
    if (actual != nullptr && actual->anterior != nullptr) {
        actual = actual->anterior;
        return true;
    }
    return false;
}

bool ListaDoble::eliminarUltimo() {
    if (inicio == nullptr || inicio == final) {
        return false; 
    }
    
    NodoHistorial* borrar = final;
    final = final->anterior;
    final->siguiente = nullptr;
    
    if (actual == borrar) {
        actual = final;
    }
    
    delete borrar;
    return true;
}

NodoHistorial* ListaDoble::getFinal() const {
    return final;
}

NodoHistorial* ListaDoble::getEstadoActual() const {
    return actual;
}

bool ListaDoble::estaVacia() const {
    return inicio == nullptr;
}
