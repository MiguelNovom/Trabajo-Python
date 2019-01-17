import socket
import json
import threading
from hundirlaflota import *

# Variables

terminado = 0
turno = 1

tamTableros = 5
numeroDeBarcos = 5

tab1Serv = []
tab1Jug = []
tab2Serv = []
tab2Jug = []

puntosJug1 = 0
puntosJug2 = 0


class Jugador(threading.Thread):
    def __init__(self, socket_jugador, datos_jugador, codigo_jugador):
        threading.Thread.__init__(self)
        self.socket = socket_jugador
        self.datos = datos_jugador
        self.codigo = codigo_jugador

    def run(self):
        global turno, puntosJug1, puntosJug2, numeroDeBarcos, terminado
        self.socket.send(("--Bienvenido a HUNDIR LA FLOTA jugador " + str(self.codigo) + "-- "
        "\n Encuentra " + str(numeroDeBarcos) + " barcos para ganar.").encode())
        while True:
            if turno / self.codigo == 1:
                if puntosJug1 == numeroDeBarcos or puntosJug2 == numeroDeBarcos:
                    terminado = 1
                    fin = json.dumps(terminado)
                    self.socket.send(fin.encode())
                    break
                if self.codigo == 1:
                    lista = json.dumps(tab1Jug)
                    self.socket.send(lista.encode())
                    coordenadaX = self.socket.recv(1000).decode()
                    coordenadaY = self.socket.recv(1000).decode()
                    jugada = comprobarBarco(int(coordenadaX) - 1, int(coordenadaY) - 1, tab1Serv)
                    if jugada is True:
                        tab1Jug[int(coordenadaX) - 1][int(coordenadaY) - 1] = "B"
                        self.socket.send("HUNDIDO".encode())
                        puntosJug1 += 1
                    elif jugada is False:
                        tab1Jug[int(coordenadaX) - 1][int(coordenadaY) - 1] = "X"
                        self.socket.send("FALLASTE".encode())
                    turno = 2
                elif self.codigo == 2:
                    lista = json.dumps(tab2Jug)
                    self.socket.send(lista.encode())
                    coordenadaX = self.socket.recv(1000).decode()
                    coordenadaY = self.socket.recv(1000).decode()
                    jugada = comprobarBarco(int(coordenadaX) - 1, int(coordenadaY) - 1, tab2Serv)
                    if jugada is True:
                        tab2Jug[int(coordenadaX) - 1][int(coordenadaY) - 1] = "B"
                        self.socket.send("HUNDIDO".encode())
                        puntosJug2 += 1
                    elif jugada is False:
                        tab2Jug[int(coordenadaX) - 1][int(coordenadaY) - 1] = "X"
                        self.socket.send("FALLASTE".encode())
                    turno = 1
                if puntosJug1 == numeroDeBarcos or puntosJug2 == numeroDeBarcos:
                    terminado = 1
                    fin = json.dumps(terminado)
                    self.socket.send(fin.encode())
                    break
            else:
                pass
        if puntosJug2 > puntosJug1:
            self.socket.send("¡Fin de la partida! Ha ganado el jugador 2.".encode())
        else:
            self.socket.send("¡Fin de la partida! Ha ganado el jugador 1.".encode())
        self.socket.close()


# Generar tableros

tab1Serv, tab2Serv, tab1Jug, tab2Jug = generarTableros(tamTableros, tab1Serv, tab2Serv, tab1Jug, tab2Jug)
generarBarcos(numeroDeBarcos, tamTableros, tab1Serv, tab2Serv)

# Creacion de sockets

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("", 9999))
server.listen(1)
cod_jugador = 1

while cod_jugador < 3:
    sc, add = server.accept()
    print("Jugador " + str(cod_jugador) + " conectado.")
    hilo = Jugador(sc, add, cod_jugador)
    hilo.start()
    cod_jugador += 1
