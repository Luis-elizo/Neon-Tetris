#ifndef LISTA_DOBLE_H
#define LISTA_DOBLE_H

#include "Tablero.h"

struct NodoHistorial {
    int estado[20][10];
    int puntaje;
    
    NodoHistorial* siguiente;
    NodoHistorial* anterior;
    
    NodoHistorial(int p = 0) {
        puntaje = p;
        siguiente = nullptr;
        anterior = nullptr;
        
        for(int i = 0; i < 20; i++) {
            for(int j = 0; j < 10; j++) {
                estado[i][j] = 0;
            }
        }
    }
};

class ListaDoble {
private:
    NodoHistorial* inicio;
    NodoHistorial* final;
    NodoHistorial* actual;

public:
    ListaDoble();
    ~ListaDoble();

    void agregarEstado(const Tablero& tablero, int puntaje);
    void vaciar();

    void irAlInicio();
    bool avanzar();
    bool retroceder();
    
    NodoHistorial* getEstadoActual() const;
    bool estaVacia() const;
};

#endif
