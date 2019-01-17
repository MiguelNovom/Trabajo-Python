import random


def comprobarFallo(x, y, tablero):
    if tablero[x][y] == "X":
        return True
    else:
        return False


def comprobarJugada(x, y, tamTab, tablero):
    if x.isdigit() is False or y.isdigit() is False:
        return True
    elif int(x) <= 0 or int(y) <= 0:
        return True
    elif int(x) > tamTab or int(y) > tamTab:
        return True
    elif comprobarBarco(int(x) - 1, int(y) - 1, tablero):
        return True
    elif comprobarFallo(int(x) - 1, int(y) - 1, tablero):
        return True
    else:
        return False


def comprobarBarco(x, y, tablero):
    if tablero[x][y] == "B":
        return True
    else:
        return False


def generarBarcos(numeroDeBarcos, tamTab, tab1Serv, tab2Serv):
    cont = 0
    while cont < numeroDeBarcos:
        x1 = random.randint(0, tamTab - 1)
        x2 = random.randint(0, tamTab - 1)
        y1 = random.randint(0, tamTab - 1)
        y2 = random.randint(0, tamTab - 1)
        if comprobarBarco(x1, y1, tab1Serv) is False and comprobarBarco(x2, y2, tab2Serv) is False:
            tab1Serv[x1][y1] = "B"
            tab2Serv[x2][y2] = "B"
            cont += 1


def generarTableros(tamTableros, tab1Jug, tab1Serv, tab2Jug, tab2Serv):
    for i in range(tamTableros):
        tab1Jug.append(["O"] * tamTableros)
        tab1Serv.append(["O"] * tamTableros)
        tab2Jug.append(["O"] * tamTableros)
        tab2Serv.append(["O"] * tamTableros)
    return tab1Serv, tab2Serv, tab1Jug, tab2Jug
