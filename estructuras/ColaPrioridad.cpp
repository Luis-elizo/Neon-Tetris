#include "ColaPrioridad.h"

ColaPrioridad::ColaPrioridad() {
    frente = nullptr;
}

ColaPrioridad::~ColaPrioridad() {
    vaciar();
}

void ColaPrioridad::vaciar() {
    while (!estaVacia()) {
        NodoEvento* aux = frente;
        frente = frente->siguiente;
        delete aux;
    }
}

void ColaPrioridad::encolar(TipoEvento ev, float tiempo, std::string msg) {
    NodoEvento* nuevo = new NodoEvento(ev, tiempo, msg);
    
    // Si esta vacia o el nuevo tiene mas prioridad (menor tiempo) que el frente
    if (estaVacia() || tiempo < frente->tiempoEjecucion) {
        nuevo->siguiente = frente;
        frente = nuevo;
    } else {
        // Buscar su posicion correcta para mantenerla ordenada
        NodoEvento* actual = frente;
        while (actual->siguiente != nullptr && actual->siguiente->tiempoEjecucion <= tiempo) {
            actual = actual->siguiente;
        }
        nuevo->siguiente = actual->siguiente;
        actual->siguiente = nuevo;
    }
}

NodoEvento ColaPrioridad::desencolar() {
    if (estaVacia()) {
        return NodoEvento(TipoEvento::BONUS_PUNTAJE, -1.0f, "");
    }
    
    NodoEvento* aux = frente;
    NodoEvento copia = *aux; // Hacemos copia de los datos
    frente = frente->siguiente;
    delete aux;
    
    return copia; // Retornamos por valor
}

float ColaPrioridad::verTiempoFrente() const {
    if (estaVacia()) return -1.0f;
    return frente->tiempoEjecucion;
}

bool ColaPrioridad::estaVacia() const {
    return frente == nullptr;
}
