#include "raylib.h"
#include <iostream>
#include "ui/menuScreen.h"
#include "ui/pauseScreen.h"
#include "ui/gameOverScreen.h"
#include "ui/gameScreen.h"
#include "ui/rankingScreen.h"
#include "estructuras/Tablero.h"
#include "logica/Pieza.h"
#include "estructuras/Cola.h"
#include "estructuras/Pila.h"
#include "estructuras/ListaDoble.h"
#include "estructuras/ColaPrioridad.h"

// estados de las pantallas
enum class EstadoJuego {
    MENU,
    JUEGO,
    PAUSA,
    GAME_OVER,
    REPLAY,
    RANKING
};

// llena la bolsa con las 7 piezas barajadas
void LlenarBolsa(Cola& cola) {
    TipoPieza bolsa[7] = { 
        TipoPieza::I, TipoPieza::O, TipoPieza::T, TipoPieza::S, 
        TipoPieza::Z, TipoPieza::J, TipoPieza::L 
    };
    
    // las revuelve al azar
    for (int indice = 6; indice > 0; indice--) {
        int indiceAleatorio = GetRandomValue(0, indice);
        TipoPieza piezaTemporal = bolsa[indice];
        bolsa[indice] = bolsa[indiceAleatorio];
        bolsa[indiceAleatorio] = piezaTemporal;
    }
    
    // mete las 7 piezas a la cola
    for (int indice = 0; indice < 7; indice++) {
        cola.encolar(bolsa[indice]);
    }
}

// programa los siguientes 3 eventos sorpresa
void ProgramarEventos(ColaPrioridad& eventos, float tiempoActual) {
    for (int indiceEvento = 0; indiceEvento < 3; indiceEvento++) {
        // tiempo en que va a salir
        float tiempo = tiempoActual + GetRandomValue(10, 15) + (indiceEvento * 15.0f);
        int tipoAleatorio = GetRandomValue(0, 2);
        
        if (tipoAleatorio == 0) {
            eventos.encolar(TipoEvento::AUMENTO_VELOCIDAD, tiempo, "¡FIEBRE DE VELOCIDAD!");
        } else if (tipoAleatorio == 1) {
            eventos.encolar(TipoEvento::LINEA_BASURA, tiempo, "¡TERREMOTO!");
        } else {
            eventos.encolar(TipoEvento::BONUS_PUNTAJE, tiempo, "¡+500 PUNTOS EXTRA!");
        }
    }
}

int main() {
    // ventana del juego
    InitWindow(1000, 900, "NeonTetris");
    SetTargetFPS(60);
    SetExitKey(0); // para que el ESC no cierre la ventana si no que pause
    
    EstadoJuego estadoActual = EstadoJuego::MENU; // pantalla actual
    
    // pantallas
    MenuScreen menu;
    PauseScreen pantallaPausa;
    GameOverScreen pantallaGameOver;
    GameScreen pantallaJuego;
    RankingScreen pantallaRanking;
    
    // estructuras
    Tablero tablero;                        // tablero del juego
    Cola colaSiguientes;                     // cola para las piezas que siguen
    LlenarBolsa(colaSiguientes);
    Pieza piezaActual(colaSiguientes.desencolar()); // saca la primera pieza
    
    Pila pilaHold;                          // pila para guardar una pieza
    bool yaIntercambio = false;             // para que solo guarde una vez por turno
    
    ListaDoble historial;                   // lista doble para el historial y replay
    ColaPrioridad eventos;                  // cola de prioridad para los eventos
    
    int puntaje = 0;
    
    // tiempo de caida
    float tiempoCaida = 0.0f;
    float velocidadCaida = 0.5f;            // velocidad normal
    
    // datos del evento de velocidad
    float tiempoPartida = 0.0f;
    bool fiebreVelocidad = false;
    float finFiebre = 0.0f;
    
    // animacion cuando se llena una linea
    bool animandoLimpieza = false;
    float tiempoAnimacionLimpieza = 0.0f;
    
    // reproduccion del replay
    bool reproduciendoAuto = false;
    float tiempoPasoReplay = 0.0f;
    
    // bucle principal
    while (!WindowShouldClose()) {
        
        // menu principal
        if (estadoActual == EstadoJuego::MENU) {
            int accion = menu.Update();
            if (accion == 1) { // jugar
                estadoActual = EstadoJuego::JUEGO;
                historial.vaciar();
                historial.agregarEstado(tablero, puntaje); // guarda el inicio en el historial
                
                eventos.vaciar();
                tiempoPartida = 0.0f;
                fiebreVelocidad = false;
                animandoLimpieza = false;
                tiempoAnimacionLimpieza = 0.0f;
                ProgramarEventos(eventos, tiempoPartida); // pone los primeros 3 eventos
            } else if (accion == 2) { // ranking
                pantallaRanking.CargarPuntajes();
                estadoActual = EstadoJuego::RANKING;
            } else if (accion == 3) { // salir
                break;
            }
        } 
        // partida en juego
        else if (estadoActual == EstadoJuego::JUEGO) {
            // pausa
            if (IsKeyPressed(KEY_ESCAPE)) {
                estadoActual = EstadoJuego::PAUSA;
            }
            // tecla rapida para perder de una vez
            if (IsKeyPressed(KEY_G)) {
                estadoActual = EstadoJuego::GAME_OVER;
                historial.irAlInicio();
                pantallaGameOver.Reset();
            }
            
            tiempoPartida += GetFrameTime();
            
            // animacion de parpadeo si lleno filas
            if (animandoLimpieza) {
                tiempoAnimacionLimpieza += GetFrameTime();
                if (tiempoAnimacionLimpieza >= 0.25f) {
                    // borra las lineas del tablero
                    int lineasLimpiadas = tablero.limpiarLineas();
                    // suma puntos segun cuantas lineas hizo
                    if (lineasLimpiadas == 1) puntaje += 100;
                    else if (lineasLimpiadas == 2) puntaje += 300;
                    else if (lineasLimpiadas == 3) puntaje += 500;
                    else if (lineasLimpiadas >= 4) puntaje += 800;
                    
                    // guarda el estado en el historial
                    historial.agregarEstado(tablero, puntaje);
                    
                    // saca la siguiente pieza de la cola
                    if (colaSiguientes.estaVacia()) {
                        LlenarBolsa(colaSiguientes);
                    }
                    piezaActual = Pieza(colaSiguientes.desencolar());
                    
                    // si no cabe la nueva pieza, se pierde
                    if (tablero.hayColision(piezaActual)) {
                        estadoActual = EstadoJuego::GAME_OVER;
                        historial.irAlInicio();
                        pantallaGameOver.Reset();
                    }
                    
                    animandoLimpieza = false;
                    tiempoAnimacionLimpieza = 0.0f;
                    tiempoCaida = 0.0f;
                }
            } else {
                // juego normal
                tiempoCaida += GetFrameTime();
                
                // revisa si ya toca un evento
                if (!eventos.estaVacia() && tiempoPartida >= eventos.verTiempoFrente()) {
                    // saca el evento de la cola
                    NodoEvento eventoExtraido = eventos.desencolar();
                    pantallaJuego.setAlerta(eventoExtraido.mensaje, tiempoPartida + 3.0f);
                    
                    if (eventoExtraido.evento == TipoEvento::BONUS_PUNTAJE) {
                        puntaje += 500;
                    } 
                    else if (eventoExtraido.evento == TipoEvento::AUMENTO_VELOCIDAD) {
                        fiebreVelocidad = true;
                        finFiebre = tiempoPartida + 10.0f; 
                    }
                    else if (eventoExtraido.evento == TipoEvento::LINEA_BASURA) {
                        tablero.agregarLineaBasura(); // mete una linea gris con hueco abajo
                    }
                }
                
                // programa otros 3 eventos
                if (eventos.estaVacia()) {
                    ProgramarEventos(eventos, tiempoPartida);
                }
                
                // termina la velocidad rapida
                if (fiebreVelocidad && tiempoPartida > finFiebre) {
                    fiebreVelocidad = false;
                }
                
                // moverse a los lados
                if (IsKeyPressed(KEY_LEFT)) {
                    piezaActual.mover(0, -1);
                    if (tablero.hayColision(piezaActual)) piezaActual.mover(0, 1);
                }
                if (IsKeyPressed(KEY_RIGHT)) {
                    piezaActual.mover(0, 1);
                    if (tablero.hayColision(piezaActual)) piezaActual.mover(0, -1);
                }
                // girar la pieza
                if (IsKeyPressed(KEY_UP)) {
                    piezaActual.rotar();
                    if (tablero.hayColision(piezaActual)) piezaActual.deshacerRotacion();
                }
                
                // baja rapido si presiona abajo
                if (IsKeyDown(KEY_DOWN)) {
                    velocidadCaida = 0.05f; 
                } else {
                    if (fiebreVelocidad) velocidadCaida = 0.25f;
                    else velocidadCaida = 0.5f;
                }
                
                // retroceder jugada con Z
                if (IsKeyPressed(KEY_Z)) {
                    if (historial.retroceder()) {
                        NodoHistorial* estadoHistorico = historial.getEstadoActual();
                        if (estadoHistorico != nullptr) {
                            tablero.cargarEstado(estadoHistorico->estado);
                            puntaje = estadoHistorico->puntaje;
                            piezaActual.setPosicion(0, 4); 
                        }
                    }
                }
                
                // rehacer jugada con Y
                if (IsKeyPressed(KEY_Y)) {
                    if (historial.avanzar()) {
                        NodoHistorial* estadoHistorico = historial.getEstadoActual();
                        if (estadoHistorico != nullptr) {
                            tablero.cargarEstado(estadoHistorico->estado);
                            puntaje = estadoHistorico->puntaje;
                            piezaActual.setPosicion(0, 4); 
                        }
                    }
                }
                
                // guardar pieza en hold con shift derecho
                if (IsKeyPressed(KEY_RIGHT_SHIFT) && !yaIntercambio) {
                    TipoPieza tipoActual = piezaActual.getTipo();
                    if (pilaHold.estaVacia()) {
                        // guarda y saca la siguiente de la cola
                        pilaHold.apilar(tipoActual);
                        if (colaSiguientes.estaVacia()) {
                            LlenarBolsa(colaSiguientes);
                        }
                        piezaActual = Pieza(colaSiguientes.desencolar());
                    } else {
                        // cambia la que tiene por la guardada
                        TipoPieza guardada = pilaHold.desapilar();
                        pilaHold.apilar(tipoActual);
                        piezaActual = Pieza(guardada);
                    }
                    yaIntercambio = true;
                    tiempoCaida = 0.0f; 
                }
                
                // caida de la pieza por gravedad
                if (tiempoCaida >= velocidadCaida) {
                    piezaActual.mover(1, 0); 
                    // si ya toco fondo o un bloque
                    if (tablero.hayColision(piezaActual)) {
                        piezaActual.mover(-1, 0); // la sube a donde si cabia
                        tablero.fijarPieza(piezaActual); // pega la pieza
                        yaIntercambio = false; // permite volver a usar hold
                        
                        // parpadeo si lleno lineas
                        if (tablero.hayLineasCompletas()) {
                            animandoLimpieza = true;
                            tiempoAnimacionLimpieza = 0.0f;
                        } else {
                            // guarda en el historial
                            historial.agregarEstado(tablero, puntaje);
                            
                            // saca la siguiente pieza
                            if (colaSiguientes.estaVacia()) {
                                LlenarBolsa(colaSiguientes);
                            }
                            piezaActual = Pieza(colaSiguientes.desencolar());
                            
                            // si no cabe, pierde
                            if (tablero.hayColision(piezaActual)) {
                                estadoActual = EstadoJuego::GAME_OVER;
                                historial.irAlInicio();
                                pantallaGameOver.Reset();
                            }
                        }
                    }
                    tiempoCaida = 0.0f;
                }
            }
        }
        // pausa
        else if (estadoActual == EstadoJuego::PAUSA) {
            int accion = pantallaPausa.Update();
            if (accion == 1) { // seguir jugando
                estadoActual = EstadoJuego::JUEGO;
            } else if (accion == 2) { // volver al menu
                estadoActual = EstadoJuego::MENU;
            }
        }
        // fin del juego
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            // pantalla para escribir nombre y guardar
            int accion = pantallaGameOver.Update(puntaje);
            if (accion == 1) { // vuelve al menu y reinicia todo
                estadoActual = EstadoJuego::MENU;
                tablero = Tablero();
                puntaje = 0;
                while (!colaSiguientes.estaVacia()) colaSiguientes.desencolar();
                LlenarBolsa(colaSiguientes);
                piezaActual = Pieza(colaSiguientes.desencolar());
                while (!pilaHold.estaVacia()) pilaHold.desapilar();
                yaIntercambio = false;
            } else if (accion == 2) { // ver repeticion
                estadoActual = EstadoJuego::REPLAY;
                historial.irAlInicio(); // empieza desde el turno 0
                reproduciendoAuto = false;
                tiempoPasoReplay = 0.0f;
            }
        }
        // repeticion de la partida
        else if (estadoActual == EstadoJuego::REPLAY) {
            // botones del replay
            int accion = pantallaJuego.UpdateReplay();

            // salir al menu
            if (IsKeyPressed(KEY_M) || accion == 4) {
                estadoActual = EstadoJuego::MENU;
                reproduciendoAuto = false;
                tiempoPasoReplay = 0.0f;
                // reinicia el tablero
                tablero = Tablero();
                puntaje = 0;
                while (!colaSiguientes.estaVacia()) colaSiguientes.desencolar();
                LlenarBolsa(colaSiguientes);
                piezaActual = Pieza(colaSiguientes.desencolar());
                while (!pilaHold.estaVacia()) pilaHold.desapilar();
                yaIntercambio = false;
            }
            // turno anterior
            if (IsKeyPressed(KEY_LEFT) || accion == 1) {
                historial.retroceder();
                reproduciendoAuto = false;
            }
            // turno siguiente
            if (IsKeyPressed(KEY_RIGHT) || accion == 3) {
                historial.avanzar();
                reproduciendoAuto = false;
            }
            // reproducir o pausar
            if (IsKeyPressed(KEY_SPACE) || accion == 2) {
                reproduciendoAuto = !reproduciendoAuto;
                tiempoPasoReplay = 0.0f;
            }

            // avanza solo cada medio segundo
            if (reproduciendoAuto) {
                tiempoPasoReplay += GetFrameTime();
                if (tiempoPasoReplay >= 0.5f) {
                    tiempoPasoReplay = 0.0f;
                    // si llego al final, se pausa
                    if (!historial.avanzar()) {
                        reproduciendoAuto = false;
                    }
                }
            }
        }
        // pantalla de ranking
        else if (estadoActual == EstadoJuego::RANKING) {
            // muestra la tabla de puntajes
            if (pantallaRanking.Update()) {
                estadoActual = EstadoJuego::MENU;
            }
        }
        
        // dibujo en pantalla
        BeginDrawing();
        
        if (estadoActual == EstadoJuego::MENU) {
            menu.Draw();
        } 
        else if (estadoActual == EstadoJuego::JUEGO) {
            // dibuja el tablero y paneles
            pantallaJuego.Draw(tablero, piezaActual, puntaje, colaSiguientes, pilaHold, tiempoPartida, animandoLimpieza, tiempoAnimacionLimpieza);
        }
        else if (estadoActual == EstadoJuego::PAUSA) {
            // dibuja la pausa encima del juego
            pantallaJuego.Draw(tablero, piezaActual, puntaje, colaSiguientes, pilaHold, tiempoPartida);
            pantallaPausa.Draw();
        }
        else if (estadoActual == EstadoJuego::GAME_OVER) {
            ClearBackground(BLACK);
            pantallaGameOver.Draw(puntaje);
        }
        else if (estadoActual == EstadoJuego::REPLAY) {
            // dibuja el turno actual del replay
            pantallaJuego.DrawReplay(historial.getEstadoActual(), reproduciendoAuto);
        }
        else if (estadoActual == EstadoJuego::RANKING) {
            pantallaRanking.Draw();
        }
        
        EndDrawing();
    }
    
    // cierra la ventana
    CloseWindow();    
    return 0;
}
