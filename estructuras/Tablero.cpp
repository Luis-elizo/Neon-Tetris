#include "Tablero.h"
#include "raylib.h"

Tablero::Tablero(int numFilas, int numColumnas) {
    filas = numFilas;
    columnas = numColumnas;
    cabeza = nullptr;
    NodoFila* actual = nullptr;
    
    // crea las 20 filas
    for (int indiceFila = 0; indiceFila < filas; indiceFila++) {
        NodoFila* nuevoNodo = new NodoFila();
        nuevoNodo->primerCelda = crearFilaVacia(); // le crea sus 10 celdas
        
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
    // borra todas las celdas y filas
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
    // hace una fila de celdas vacias
    NodoCelda* inicio = nullptr;
    NodoCelda* actual = nullptr;
    
    for (int indiceCol = 0; indiceCol < columnas; indiceCol++) {
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

int Tablero::getCelda(int fila, int columna) {
    // revisa que no se salga del tablero
    if (fila < 0 || fila >= filas || columna < 0 || columna >= columnas) {
        return -1;
    }
    
    // baja hasta la fila
    NodoFila* filaActual = cabeza;
    for (int indiceFila = 0; indiceFila < fila && filaActual != nullptr; indiceFila++) {
        filaActual = filaActual->siguiente;
    }
    if (filaActual == nullptr) return -1;
    
    // avanza hasta la columna
    NodoCelda* celdaActual = filaActual->primerCelda;
    for (int indiceCol = 0; indiceCol < columna && celdaActual != nullptr; indiceCol++) {
        celdaActual = celdaActual->siguiente;
    }
    if (celdaActual == nullptr) return -1;
    
    return celdaActual->color;
}

void Tablero::setCelda(int fila, int columna, int color) {
    // revisa que no se salga
    if (fila < 0 || fila >= filas || columna < 0 || columna >= columnas) return;
    
    NodoFila* filaActual = cabeza;
    for (int indiceFila = 0; indiceFila < fila && filaActual != nullptr; indiceFila++) {
        filaActual = filaActual->siguiente;
    }
    if (filaActual == nullptr) return;
    
    NodoCelda* celdaActual = filaActual->primerCelda;
    for (int indiceCol = 0; indiceCol < columna && celdaActual != nullptr; indiceCol++) {
        celdaActual = celdaActual->siguiente;
    }
    if (celdaActual != nullptr) {
        celdaActual->color = color;
    }
}

bool Tablero::hayColision(Pieza& pieza) {
    // revisa si choca con bordes o con otros bloques
    for (int indiceBloque = 0; indiceBloque < 4; indiceBloque++) {
        Posicion pos = pieza.getPosicionBloque(indiceBloque);
        
        // revisa paredes y piso
        if (pos.col < 0 || pos.col >= columnas || pos.fila >= filas) {
            return true;
        }
        
        // todavia no entra al tablero
        if (pos.fila < 0) continue; 
        
        // la celda ya esta ocupada
        if (getCelda(pos.fila, pos.col) != 0) {
            return true;
        }
    }
    return false;
}

void Tablero::fijarPieza(Pieza& pieza) {
    // copia los bloques al tablero
    for (int indiceBloque = 0; indiceBloque < 4; indiceBloque++) {
        Posicion pos = pieza.getPosicionBloque(indiceBloque);
        if (pos.fila >= 0 && pos.fila < filas && pos.col >= 0 && pos.col < columnas) {
            setCelda(pos.fila, pos.col, pieza.getColorId());
        }
    }
}

int Tablero::limpiarLineas() {
    int lineasLimpiadas = 0;
    
    NodoFila* previoFila = nullptr;
    NodoFila* actualFila = cabeza;
    
    // busca filas llenas
    while (actualFila != nullptr) {
        bool llena = true;
        NodoCelda* celda = actualFila->primerCelda;
        // si ve una celda vacia, no esta llena
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
            
            // borra las celdas de la fila
            NodoCelda* celdaABorrar = actualFila->primerCelda;
            while (celdaABorrar != nullptr) {
                NodoCelda* celdaEliminar = celdaABorrar;
                celdaABorrar = celdaABorrar->siguiente;
                delete celdaEliminar;
            }
            
            // desconecta y borra la fila
            if (previoFila == nullptr) {
                cabeza = siguienteFila;
            } else {
                previoFila->siguiente = siguienteFila;
            }
            delete actualFila;
            
            // pone una fila vacia arriba
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

bool Tablero::esFilaLlena(int filaIndex) {
    // revisa si una fila esta llena
    if (filaIndex < 0 || filaIndex >= filas) return false;
    
    NodoFila* actualFila = cabeza;
    for (int indiceFila = 0; indiceFila < filaIndex && actualFila != nullptr; indiceFila++) {
        actualFila = actualFila->siguiente;
    }
    if (actualFila == nullptr) return false;
    
    NodoCelda* celda = actualFila->primerCelda;
    while (celda != nullptr) {
        if (celda->color == 0) return false;
        celda = celda->siguiente;
    }
    return true;
}

bool Tablero::hayLineasCompletas() {
    // revisa si hay alguna fila llena
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
        if (llena) return true;
        actualFila = actualFila->siguiente;
    }
    return false;
}

void Tablero::agregarLineaBasura() {
    // quita la de arriba y mete una fila gris con hueco abajo
    NodoFila* filaEliminar = cabeza;
    cabeza = cabeza->siguiente;
    
    // borra la fila de arriba
    NodoCelda* celdaRecorrido = filaEliminar->primerCelda;
    while (celdaRecorrido != nullptr) {
        NodoCelda* celdaABorrar = celdaRecorrido;
        celdaRecorrido = celdaRecorrido->siguiente;
        delete celdaABorrar;
    }
    delete filaEliminar;
    
    // crea la fila con un hueco aleatorio
    NodoFila* nuevaFila = new NodoFila();
    int hueco = GetRandomValue(0, columnas - 1);
    
    NodoCelda* actual = nullptr;
    for (int indiceCol = 0; indiceCol < columnas; indiceCol++) {
        NodoCelda* nuevaCelda = new NodoCelda();
        nuevaCelda->color = (indiceCol == hueco) ? 0 : 8; 
        
        if (indiceCol == 0) {
            nuevaFila->primerCelda = nuevaCelda;
            actual = nuevaCelda;
        } else {
            actual->siguiente = nuevaCelda;
            actual = nuevaCelda;
        }
    }
    
    // la conecta al fondo
    NodoFila* ultimaFila = cabeza;
    while (ultimaFila->siguiente != nullptr) {
        ultimaFila = ultimaFila->siguiente;
    }
    ultimaFila->siguiente = nuevaFila;
}

void Tablero::cargarEstado(int estado[20][10]) {
    // copia los colores de la matriz
    NodoFila* filaActual = cabeza;
    for (int indiceFila = 0; indiceFila < filas && filaActual != nullptr; indiceFila++) {
        NodoCelda* celdaActual = filaActual->primerCelda;
        for (int indiceCol = 0; indiceCol < columnas && celdaActual != nullptr; indiceCol++) {
            celdaActual->color = estado[indiceFila][indiceCol];
            celdaActual = celdaActual->siguiente;
        }
        filaActual = filaActual->siguiente;
    }
}
