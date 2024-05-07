import random, sys, math

# Nota: en lugar de matrices se usan listas de listas

def matrizDistancias(nCiud, distanciaMaxima):
    matriz = [[0 for i in range(nCiud)] for j in range(nCiud)]

    for i in range(nCiud):
        for j in range(i):
            matriz[i][j] = distanciaMaxima * random.random()
            matriz[j][i] = matriz[i][j]

    return matriz

# Elige un paso de una hormiga, teniendo en cuenta las distancias
# y las feromonas y descartando las ciudades ya visitadas.
def eligeCiudad(dists, ferom, visitadas):
    # Se calcula la tabla de pesos de cada ciudad
    listaPesos = []
    disponibles = []
    actual = visitadas[-1] # La última ciudad visitada
    alfa = 1.0
    beta = 0.5

    for i in range(len(dists)):
        if i not in visitadas:
            fer = math.pow((1.0 + ferom[actual][i]), alfa)
            peso = math.pow(1.0 / dists[actual][i], beta) * fer
            disponibles.append(i)
            listaPesos.append(peso)

    # Se elige aleatoriamente una de las ciudades disponibles,
    # teniendo en cuenta su peso relativo.
    valor = random.random() * sum(listaPesos)
    acumulado = 0.0
    i = -1

    while valor > acumulado:
        i += 1
        acumulado += listaPesos[i]

    return disponibles[i]

def eligeCamino(distancias, feromonas):
    camino = [0]
    longCamino = 0

    while len(camino) < len(distancias):
        ciudad = eligeCiudad(distancias, feromonas, camino)
        longCamino += distancias[camino[-1]][ciudad]
        camino.append(ciudad)


    longCamino += distancias[camino[-1]][0]
    camino.append(ciudad)

    return (camino, longCamino)

def rastroFeromonas(feromonas, camino, dosis):
    for i in range(len(camino) - 1):
        feromonas[camino[i]][camino[i+1]] += dosis

# Evapora todas las feromonas multiplicándolas por una constante
# = 0.9 (en otras palabras, el coeficiente de evaporación es 0.1)
def evaporaFeromonas(feromonas):
    for lista in feromonas:
        for i in range(len(lista)):
            lista[i] *= 0.9

def hormigas(distancias, iteraciones, distMedia):
    # Primero se crea una matriz de feromonas vacía
    n = len(distancias)
    feromonas = [[0 for i in range(n)] for j in range(n)]

    # El mejor camino y su longitud (inicialmente "infinita")
    mejorCamino = []
    longMejorCamino = sys.maxsize

    # En cada iteración se genera una hormiga, que elige un camino,
    # y si es mejor que el mejor que teníamos, deja su rastro de
    # feromonas (mayor cuanto más corto sea el camino)
    for iter in range(iteraciones):
        (camino, longCamino) = eligeCamino(distancias, feromonas)

        if longCamino <= longMejorCamino:
            mejorCamino = camino
            longMejorCamino = longCamino

        rastroFeromonas(feromonas, camino, distMedia/longCamino)

        # En cualquier caso, las feromonas se van evaporando
        evaporaFeromonas(feromonas)

    # Se devuelve el mejor camino que se haya encontrado
    return (mejorCamino, longMejorCamino)

# Generación de una matriz de prueba
numCiudades = 10

distanciaMaxima = 100
ciudades = matrizDistancias(numCiudades, distanciaMaxima)

iteraciones = 100
distMedia = numCiudades* distanciaMaxima/2
(camino, longCamino) = hormigas(ciudades, iteraciones, distMedia)
print("Camino: ", camino)
print("Longitud del camino: ", longCamino)
