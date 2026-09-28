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
    // borra todos los turnos guardados
    NodoHistorial* nodoActual = inicio;
    while (nodoActual != nullptr) {
        NodoHistorial* nodoABorrar = nodoActual;
        nodoActual = nodoActual->siguiente;
        delete nodoABorrar;
    }
    inicio = nullptr;
    final = nullptr;
    actual = nullptr;
}

void ListaDoble::agregarEstado(Tablero& tablero, int puntaje) {
    // si habiamos deshecho jugadas y hacemos una nueva, borramos las que quedaron adelante
    if (actual != nullptr && actual != final) {
        NodoHistorial* nodoSiguiente = actual->siguiente;
        while (nodoSiguiente != nullptr) {
            NodoHistorial* nodoABorrar = nodoSiguiente;
            nodoSiguiente = nodoSiguiente->siguiente;
            delete nodoABorrar;
        }
        actual->siguiente = nullptr;
        final = actual;
    }

    NodoHistorial* nuevo = new NodoHistorial(puntaje);
    
    // copia las celdas del tablero al nuevo turno
    for (int fila = 0; fila < 20; fila++) {
        for (int columna = 0; columna < 10; columna++) {
            nuevo->estado[fila][columna] = tablero.getCelda(fila, columna);
        }
    }
    
    // lo engancha al final de la lista
    if (inicio == nullptr) {
        inicio = nuevo;
        final = nuevo;
    } else {
        final->siguiente = nuevo;
        nuevo->anterior = final;
        final = nuevo;
    }
    actual = final; // se para en el turno nuevo
}

void ListaDoble::irAlInicio() {
    // se va al primer turno
    actual = inicio;
}

bool ListaDoble::avanzar() {
    // pasa al turno siguiente
    if (actual != nullptr && actual->siguiente != nullptr) {
        actual = actual->siguiente;
        return true;
    }
    return false;
}

bool ListaDoble::retroceder() {
    // vuelve al turno anterior
    if (actual != nullptr && actual->anterior != nullptr) {
        actual = actual->anterior;
        return true;
    }
    return false;
}

bool ListaDoble::eliminarUltimo() {
    // borra el ultimo turno si hay mas de uno
    if (inicio == nullptr || inicio == final) {
        return false; 
    }
    
    NodoHistorial* nodoABorrar = final;
    final = final->anterior;
    final->siguiente = nullptr;
    
    if (actual == nodoABorrar) {
        actual = final;
    }
    
    delete nodoABorrar;
    return true;
}

NodoHistorial* ListaDoble::getFinal() {
    return final;
}

NodoHistorial* ListaDoble::getEstadoActual() {
    return actual;
}

bool ListaDoble::estaVacia() {
    return inicio == nullptr;
}
