#ifndef COLA_PRIORIDAD_H
#define COLA_PRIORIDAD_H

#include <string>

enum class TipoEvento {
    AUMENTO_VELOCIDAD,
    LINEA_BASURA,
    BONUS_PUNTAJE
};

struct NodoEvento {
    TipoEvento evento;
    float tiempoEjecucion; // Prioridad (menor tiempo = primero en salir)
    std::string mensaje;
    
    NodoEvento* siguiente;
    
    NodoEvento(TipoEvento ev, float tiempo, std::string msg) {
        evento = ev;
        tiempoEjecucion = tiempo;
        mensaje = msg;
        siguiente = nullptr;
    }
};

class ColaPrioridad {
private:
    NodoEvento* frente;

public:
    ColaPrioridad();
    ~ColaPrioridad();

    void encolar(TipoEvento ev, float tiempo, std::string msg);
    NodoEvento desencolar();
    float verTiempoFrente() const;
    bool estaVacia() const;
    void vaciar();
};

#endif
