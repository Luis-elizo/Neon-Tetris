#ifndef RANKING_SCREEN_H
#define RANKING_SCREEN_H

#include "raylib.h"
#include "../estructuras/ManejadorJSON.h"
#include "../logica/ordenamientos.h"

// pantalla de records
class RankingScreen {
private:
    Rectangle botonVolver; // boton para volver
    Rectangle botonBubble; // boton para ordenar con burbuja
    Rectangle botonMerge;  // boton para ordenar con merge sort

    bool volverResaltado; // mouse sobre volver
    bool bubbleResaltado; // mouse sobre burbuja
    bool mergeResaltado;  // mouse sobre merge sort

    int algoritmoActivo;       // 0 burbuja, 1 merge sort
    ListaPuntajes listaActual; // lista de puntajes cargada

    long long tiempoNano; // tiempo en nanosegundos
    double tiempoMicro;   // tiempo en microsegundos

    void EjecutarOrdenamiento(); // mide el tiempo que tarda en ordenar

public:
    RankingScreen();

    void CargarPuntajes(); // lee el archivo json y ordena
    bool Update();         // revisa clics
    void Draw();           // dibuja la tabla
};

#endif
