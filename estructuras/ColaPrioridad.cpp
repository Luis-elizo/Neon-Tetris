#include "ColaPrioridad.h"

ColaPrioridad::ColaPrioridad() {
    frente = nullptr;
}

ColaPrioridad::~ColaPrioridad() {
    vaciar();
}

void ColaPrioridad::vaciar() {
    // borra todos los eventos que queden
    while (!estaVacia()) {
        NodoEvento* nodoAEliminar = frente;
        frente = frente->siguiente;
        delete nodoAEliminar;
    }
}

void ColaPrioridad::encolar(TipoEvento tipoEvento, float tiempo, std::string mensajeEvento) {
    NodoEvento* nuevo = new NodoEvento(tipoEvento, tiempo, mensajeEvento);
    
    // si no hay nada o toca antes que el primero, lo pone al frente
    if (estaVacia() || tiempo < frente->tiempoEjecucion) {
        nuevo->siguiente = frente;
        frente = nuevo;
    } else {
        // busca donde meterlo en orden de tiempo
        NodoEvento* actual = frente;
        while (actual->siguiente != nullptr && actual->siguiente->tiempoEjecucion <= tiempo) {
            actual = actual->siguiente;
        }
        // lo conecta en el medio
        nuevo->siguiente = actual->siguiente;
        actual->siguiente = nuevo;
    }
}

NodoEvento ColaPrioridad::desencolar() {
    if (estaVacia()) {
        return NodoEvento(TipoEvento::BONUS_PUNTAJE, -1.0f, "");
    }
    
    // saca el evento que estaba de primero
    NodoEvento* nodoAEliminar = frente;
    NodoEvento copia = *nodoAEliminar;
    frente = frente->siguiente;
    delete nodoAEliminar;
    
    return copia;
}

float ColaPrioridad::verTiempoFrente() {
    if (estaVacia()) return -1.0f;
    return frente->tiempoEjecucion;
}

bool ColaPrioridad::estaVacia() {
    return frente == nullptr;
}
