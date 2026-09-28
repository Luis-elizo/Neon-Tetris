#include "ordenamientos.h"

// ordenamiento burbuja
void Ordenamientos::ordenarBurbuja(ListaPuntajes& lista) {
    for (int paso = 0; paso < lista.cantidad - 1; paso++) {
        for (int indice = 0; indice < lista.cantidad - paso - 1; indice++) {
            // compara si el siguiente es mayor para dejarlo de primero
            if (lista.registros[indice].puntaje < lista.registros[indice + 1].puntaje) {
                RegistroPuntaje registroTemporal = lista.registros[indice];
                lista.registros[indice] = lista.registros[indice + 1];
                lista.registros[indice + 1] = registroTemporal;
            }
        }
    }
}

// junta las dos mitades ordenadas
static void mezclar(RegistroPuntaje arregloRegistros[], int izquierda, int medio, int derecha) {
    int tamanoIzquierda = medio - izquierda + 1;
    int tamanoDerecha = derecha - medio;

    // arreglos temporales para cada mitad
    RegistroPuntaje mitadIzquierda[50];
    RegistroPuntaje mitadDerecha[50];

    for (int indiceIzq = 0; indiceIzq < tamanoIzquierda; indiceIzq++) {
        mitadIzquierda[indiceIzq] = arregloRegistros[izquierda + indiceIzq];
    }
    for (int indiceDer = 0; indiceDer < tamanoDerecha; indiceDer++) {
        mitadDerecha[indiceDer] = arregloRegistros[medio + 1 + indiceDer];
    }

    int indiceIzquierda = 0;
    int indiceDerecha = 0;
    int indiceMezcla = izquierda;

    // compara los dos y mete el mayor
    while (indiceIzquierda < tamanoIzquierda && indiceDerecha < tamanoDerecha) {
        if (mitadIzquierda[indiceIzquierda].puntaje >= mitadDerecha[indiceDerecha].puntaje) {
            arregloRegistros[indiceMezcla] = mitadIzquierda[indiceIzquierda];
            indiceIzquierda++;
        } else {
            arregloRegistros[indiceMezcla] = mitadDerecha[indiceDerecha];
            indiceDerecha++;
        }
        indiceMezcla++;
    }

    // copia lo que falte de la izquierda
    while (indiceIzquierda < tamanoIzquierda) {
        arregloRegistros[indiceMezcla] = mitadIzquierda[indiceIzquierda];
        indiceIzquierda++;
        indiceMezcla++;
    }

    // copia lo que falte de la derecha
    while (indiceDerecha < tamanoDerecha) {
        arregloRegistros[indiceMezcla] = mitadDerecha[indiceDerecha];
        indiceDerecha++;
        indiceMezcla++;
    }
}

// parte el arreglo a la mitad recursivamente
static void mergeSortRecursivo(RegistroPuntaje arregloRegistros[], int izquierda, int derecha) {
    if (izquierda < derecha) {
        int medio = izquierda + (derecha - izquierda) / 2;
        mergeSortRecursivo(arregloRegistros, izquierda, medio);     // mitad izquierda
        mergeSortRecursivo(arregloRegistros, medio + 1, derecha); // mitad derecha
        mezclar(arregloRegistros, izquierda, medio, derecha);     // junta las dos partes
    }
}

// ordenamiento merge sort
void Ordenamientos::ordenarMergeSort(ListaPuntajes& lista) {
    if (lista.cantidad <= 1) return;
    mergeSortRecursivo(lista.registros, 0, lista.cantidad - 1);
}
