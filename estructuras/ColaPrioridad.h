#ifndef COLA_PRIORIDAD_H
#define COLA_PRIORIDAD_H

#include <string>

// tipos de eventos que salen en la partida
enum class TipoEvento {
    AUMENTO_VELOCIDAD, // cae mas rapido por 10 segundos
    LINEA_BASURA,      // mete una fila con un hueco
    BONUS_PUNTAJE      // da 500 puntos extra
};

// nodo para la cola de prioridad
struct NodoEvento {
    TipoEvento evento;     // que evento es
    float tiempoEjecucion; // en que segundo le toca salir
    std::string mensaje;   // texto que sale en pantalla
    
    NodoEvento* siguiente; // puntero al siguiente evento
    
    NodoEvento(TipoEvento tipoEvento, float tiempo, std::string mensajeEvento) {
        evento = tipoEvento;
        tiempoEjecucion = tiempo;
        mensaje = mensajeEvento;
        siguiente = nullptr;
    }
};

// cola de prioridad ordenada por tiempo
class ColaPrioridad {
private:
    NodoEvento* frente; // el evento que va a salir primero

public:
    ColaPrioridad();
    ~ColaPrioridad();

    // mete un evento y lo acomoda segun el tiempo
    void encolar(TipoEvento tipoEvento, float tiempo, std::string mensajeEvento);
    
    // saca el evento que toca primero
    NodoEvento desencolar();
    
    // mira cuando toca el primer evento
    float verTiempoFrente();
    bool estaVacia(); // revisa si no quedan eventos
    void vaciar();    // borra todos los eventos
};

#endif
