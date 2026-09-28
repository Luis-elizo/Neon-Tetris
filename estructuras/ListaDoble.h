#ifndef LISTA_DOBLE_H
#define LISTA_DOBLE_H

#include "Tablero.h"

// nodo para guardar una foto del tablero y el puntaje
struct NodoHistorial {
    int estado[20][10]; // copia de las celdas en este turno
    int puntaje;        // puntaje en este turno
    
    NodoHistorial* siguiente; // turno siguiente
    NodoHistorial* anterior;  // turno anterior
    
    NodoHistorial(int puntajeInicial = 0) {
        puntaje = puntajeInicial;
        siguiente = nullptr;
        anterior = nullptr;
        
        for (int fila = 0; fila < 20; fila++) {
            for (int columna = 0; columna < 10; columna++) {
                estado[fila][columna] = 0;
            }
        }
    }
};

// lista doble para deshacer, rehacer y replay
class ListaDoble {
private:
    NodoHistorial* inicio; // primer movimiento
    NodoHistorial* final;  // ultimo movimiento
    NodoHistorial* actual; // turno donde estamos parados

public:
    ListaDoble();
    ~ListaDoble();

    void agregarEstado(Tablero& tablero, int puntaje); // guarda un turno nuevo al final
    void vaciar();                                     // borra todo el historial

    void irAlInicio();       // se pone en el primer turno para el replay
    bool avanzar();          // pasa al turno siguiente
    bool retroceder();       // vuelve al turno anterior
    
    bool eliminarUltimo();   // quita el ultimo turno
    NodoHistorial* getFinal();
    
    NodoHistorial* getEstadoActual(); // devuelve el turno actual
    bool estaVacia();                 // revisa si no tiene nada
};

#endif
