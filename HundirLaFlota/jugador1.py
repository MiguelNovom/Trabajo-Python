import socket
import json
from hundirlaflota import comprobarJugada

tamTab = 5
terminado = "0"

s = socket.socket()
s.connect(("localhost", 9999))

titulo = s.recv(2000).decode()
print(titulo)

while True:
    datos = s.recv(1000)
    tablero = json.loads(datos)
    if tablero == 1:
        break
    for row in tablero:
        print(' '.join([str(elem) for elem in row]))
    x = (input("Introduce la posicion X: "))
    y = (input("Introduce la posicion Y: "))
    while comprobarJugada(x, y, tamTab, tablero):
        print("Coordenadas equivocadas o repetidas")
        x = input("Introduce la posicion X: ")
        y = input("Introduce la posicion Y: ")
    s.send(x.encode())
    s.send(y.encode())
    respuesta = s.recv(1000).decode()
    print(respuesta)

final = s.recv(1000).decode()
print(final)
s.close()
