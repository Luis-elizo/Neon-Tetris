#ifndef MENU_SCREEN_H
#define MENU_SCREEN_H

#include "raylib.h"

// Representa la pantalla principal (titulo + boton "Jugar").
class MenuScreen {
private:
	//Variables
	Rectangle botonJugar;
	bool botonResaltado;
	
	//Metodos
	void DibujarTitulo();
	void DibujarBoton();
	
public:
	MenuScreen();
	
	// Actualiza el estado del boton (hover, click).
	bool Update();
	
	void Draw();
};

#endif
