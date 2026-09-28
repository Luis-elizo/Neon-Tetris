#ifndef MANEJADOR_JSON_H
#define MANEJADOR_JSON_H

#include <string>

// guarda el nombre y los puntos
struct RegistroPuntaje {
    std::string nombre; // nombre del jugador
    int puntaje;        // puntaje obtenido
};

// lista con los puntajes guardados
struct ListaPuntajes {
    RegistroPuntaje registros[50]; // maximo 50 records
    int cantidad;                  // cuantos records hay
    
    ListaPuntajes() {
        cantidad = 0;
    }
};

// clase para guardar y cargar el archivo json
class ManejadorJSON {
public:
    static ListaPuntajes cargar(std::string rutaArchivo);          // lee el json
    static void guardar(std::string rutaArchivo, ListaPuntajes& lista); // escribe en el json
};

#endif
