#include "ManejadorJSON.h"
#include <fstream>

void ManejadorJSON::guardar(std::string rutaArchivo, ListaPuntajes& lista) {
    // abre el archivo para escribir
    std::ofstream archivo(rutaArchivo);
    if (!archivo.is_open()) return;

    archivo << "[\n";
    for (int indice = 0; indice < lista.cantidad; indice++) {
        archivo << "  { \"nombre\" : \"" << lista.registros[indice].nombre 
                << "\" , \"puntaje\" : " << lista.registros[indice].puntaje << " }";
                
        // coma para separar elementos menos en el ultimo
        if (indice < lista.cantidad - 1) {
            archivo << " ,\n";
        } else {
            archivo << "\n";
        }
    }
    archivo << "]\n";
    archivo.close();
}

ListaPuntajes ManejadorJSON::cargar(std::string rutaArchivo) {
    // lee el archivo buscando nombre y puntaje
    ListaPuntajes lista;
    std::ifstream archivo(rutaArchivo);
    if (!archivo.is_open()) return lista;

    std::string palabra;
    std::string tempNombre = "";
    
    while (archivo >> palabra) {
        if (palabra == "\"nombre\"") {
            // salta los dos puntos y lee el nombre
            archivo >> palabra;
            archivo >> palabra;
            
            // le quita las comillas al texto
            tempNombre = "";
            for (char letra : palabra) {
                if (letra != '"' && letra != ',') {
                    tempNombre += letra;
                }
            }
        }
        else if (palabra == "\"puntaje\"") {
            // salta los dos puntos y lee el numero
            archivo >> palabra;
            archivo >> palabra;
            
            int tempPuntos = std::stoi(palabra);
            
            // guarda el registro en la lista
            lista.registros[lista.cantidad].nombre = tempNombre;
            lista.registros[lista.cantidad].puntaje = tempPuntos;
            lista.cantidad++;
            
            if (lista.cantidad == 50) break; // maximo 50
        }
    }
    
    archivo.close();
    return lista;
}
