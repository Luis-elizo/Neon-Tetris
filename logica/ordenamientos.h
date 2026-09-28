#ifndef ORDENAMIENTOS_H
#define ORDENAMIENTOS_H

#include "../estructuras/ManejadorJSON.h"

// metodos para ordenar la lista de puntajes
class Ordenamientos {
public:
    static void ordenarBurbuja(ListaPuntajes& lista);   // metodo burbuja
    static void ordenarMergeSort(ListaPuntajes& lista); // metodo merge sort
};

#endif
