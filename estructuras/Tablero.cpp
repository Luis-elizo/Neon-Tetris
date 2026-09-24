#include "Tablero.h"

Tablero::Tablero(int numFilas, int numCols) : filas(numFilas), columnas(numCols) {
    cabeza = nullptr;
    NodoFila* actual = nullptr;
    
    for (int i = 0; i < filas; ++i) {
        NodoFila* nuevoNodo = new NodoFila();
        nuevoNodo->primerCelda = crearFilaVacia();
        
        if (cabeza == nullptr) {
            cabeza = nuevoNodo;
            actual = cabeza;
        } else {
            actual->siguiente = nuevoNodo;
            actual = nuevoNodo;
        }
    }
}

Tablero::~Tablero() {
    NodoFila* actualFila = cabeza;
    while (actualFila != nullptr) {
        NodoCelda* actualCelda = actualFila->primerCelda;
        while (actualCelda != nullptr) {
            NodoCelda* borrarCelda = actualCelda;
            actualCelda = actualCelda->siguiente;
            delete borrarCelda;
        }
        NodoFila* borrarFila = actualFila;
        actualFila = actualFila->siguiente;
        delete borrarFila;
    }
}

NodoCelda* Tablero::crearFilaVacia() {
    NodoCelda* inicio = nullptr;
    NodoCelda* actual = nullptr;
    
    for (int i = 0; i < columnas; ++i) {
        NodoCelda* nuevo = new NodoCelda(0);
        if (inicio == nullptr) {
            inicio = nuevo;
            actual = inicio;
        } else {
            actual->siguiente = nuevo;
            actual = nuevo;
        }
    }
    return inicio;
}

int Tablero::getCelda(int fila, int col) const {
    if (fila < 0 || fila >= filas || col < 0 || col >= columnas) {
        return -1;
    }
    
    NodoFila* f = cabeza;
    for (int i = 0; i < fila && f != nullptr; ++i) {
        f = f->siguiente;
    }
    if (f == nullptr) return -1;
    
    NodoCelda* c = f->primerCelda;
    for (int j = 0; j < col && c != nullptr; ++j) {
        c = c->siguiente;
    }
    if (c == nullptr) return -1;
    
    return c->color;
}

void Tablero::setCelda(int fila, int col, int color) {
    if (fila < 0 || fila >= filas || col < 0 || col >= columnas) return;
    
    NodoFila* f = cabeza;
    for (int i = 0; i < fila && f != nullptr; ++i) f = f->siguiente;
    if (f == nullptr) return;
    
    NodoCelda* c = f->primerCelda;
    for (int j = 0; j < col && c != nullptr; ++j) c = c->siguiente;
    if (c != nullptr) c->color = color;
}

bool Tablero::hayColision(const Pieza& pieza) const {
    for (int i = 0; i < 4; ++i) {
        Posicion pos = pieza.getPosicionBloque(i);
        
        if (pos.col < 0 || pos.col >= columnas || pos.fila >= filas) {
            return true;
        }
        
        if (pos.fila < 0) continue; 
        
        if (getCelda(pos.fila, pos.col) != 0) {
            return true;
        }
    }
    return false;
}

void Tablero::fijarPieza(const Pieza& pieza) {
    for (int i = 0; i < 4; ++i) {
        Posicion pos = pieza.getPosicionBloque(i);
        if (pos.fila >= 0 && pos.fila < filas && pos.col >= 0 && pos.col < columnas) {
            setCelda(pos.fila, pos.col, pieza.getColorId());
        }
    }
}

int Tablero::limpiarLineas() {
    int lineasLimpiadas = 0;
    
    NodoFila* previoFila = nullptr;
    NodoFila* actualFila = cabeza;
    
    while (actualFila != nullptr) {
        bool llena = true;
        NodoCelda* celda = actualFila->primerCelda;
        while (celda != nullptr) {
            if (celda->color == 0) {
                llena = false;
                break;
            }
            celda = celda->siguiente;
        }
        
        if (llena) {
            lineasLimpiadas++;
            NodoFila* siguienteFila = actualFila->siguiente;
            
            NodoCelda* c = actualFila->primerCelda;
            while (c != nullptr) {
                NodoCelda* borrar = c;
                c = c->siguiente;
                delete borrar;
            }
            
            if (previoFila == nullptr) {
                cabeza = siguienteFila;
            } else {
                previoFila->siguiente = siguienteFila;
            }
            delete actualFila;
            
            NodoFila* nuevaFila = new NodoFila();
            nuevaFila->primerCelda = crearFilaVacia();
            nuevaFila->siguiente = cabeza;
            cabeza = nuevaFila;
            
            actualFila = siguienteFila;
        } else {
            previoFila = actualFila;
            actualFila = actualFila->siguiente;
        }
    }
    
    return lineasLimpiadas;
}

void Tablero::cargarEstado(int estado[20][10]) {
    NodoFila* filaActual = cabeza;
    for (int i = 0; i < filas && filaActual != nullptr; ++i) {
        NodoCelda* celdaActual = filaActual->primerCelda;
        for (int j = 0; j < columnas && celdaActual != nullptr; ++j) {
            celdaActual->color = estado[i][j];
            celdaActual = celdaActual->siguiente;
        }
        filaActual = filaActual->siguiente;
    }
}
