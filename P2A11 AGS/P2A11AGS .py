from random import random, randint, sample
from collections import namedtuple

# Calcula el capital invertido por un individuo
def capitalInvertido(individuo):
    return sum(map(lambda x, y: x*y.precio, individuo, inversiones))

# Calcula el rendimiento obtenido por un individuo
def rendimiento(individuo):
    return sum(map(lambda x, y: x*y.precio*y.rendim, individuo, inversiones))

# Si un individuo gasta más capital del disponible, se eliminan
# aleatoriamente inversiones hasta que se ajusta al capital
def ajustaCapital(individuo):
    ajustado = individuo[:]
    while capitalInvertido(ajustado) > capital:
        pos = randint(0, len(ajustado)-1)
        if ajustado[pos] > 0:
            ajustado[pos] -= 1
    return ajustado

# Crea un individuo al azar, en este caso una selección de
# inversiones que no excedan el capital disponible
def creaIndividuo(inversiones, capital):
    individuo = [0]*len(inversiones)
    while capitalInvertido(individuo) < capital:
        eleccion = randint(0, len(inversiones)-1)
        individuo[eleccion] += 1
    return ajustaCapital(individuo)

# Crea un nuevo individuo cruzando otros dos (cuyas posiciones se
# indican en el segundo parámetro)
def cruza(poblacion, posiciones):
    # Toma los genes del primer progenitor y luego toma al azar
    # un segmento de entre 1 y L genes del segundo progenitor
    L = len(poblacion[0])
    hijo = poblacion[posiciones[0]][:]  # Copia del primer progenitor
    inicio = randint(0, L - 1)  # Inicio aleatorio para el segmento del segundo progenitor
    fin = randint(inicio + 1, L)  # Fin aleatorio para el segmento (debe ser después del inicio)
    hijo[inicio:fin] = poblacion[posiciones[1]][inicio:fin]  # Reemplazo del segmento en el hijo
    return ajustaCapital(hijo)  # Ajusta el capital del hijo y lo retorna

# Aplica mutaciones a un individuo según una tasa dada; garantiza
# que cumple las restricciones de capital e inversiones
def muta(individuo, tasaMutacion):
    mutado = []  # Inicializa una nueva lista para el individuo mutado
    for i in range(len(individuo)):  # Itera sobre cada gen del individuo
        if random() > tasaMutacion:  # Con una probabilidad de (1 - tasaMutacion), mantiene el gen
            mutado.append(individuo[i])
        else:  # Con una probabilidad de tasaMutacion, aplica una mutación
            mutado.append(randint(0, inversiones[
                i].cantidad))  # La mutación es un valor aleatorio dentro de un rango permitido
    return ajustaCapital(mutado)  # Ajusta el capital del individuo mutado y lo retorna

# Evoluciona una población de individuos durante un número dado de generaciones
def evoluciona(poblacion, generaciones):
    # Ordena la población inicial por rendimiento producido
    poblacion.sort(key=lambda x: rendimiento(x))

    # Algunos valores útiles
    N = len(poblacion)
    tasaMutacion = 0.01

    # Genera una lista del tipo [0,1,1,2,2,2,3,3,3,3,...] para
    # representar las probabilidades de reproducirse de cada
    # individuo (el primero 1 posibilidad, el segundo 2, etc.)
    reproduccion = [x for x in range(N) for y in range(x+1)]

    for i in range(generaciones):
        # Se generan N-1 nuevos individuos cruzando los existentes
        # (sin que se repitan los padres)
        padres = sample(reproduccion, 2)
        while padres[0] == padres[1]:
            padres = sample(reproduccion, 2)
        hijos = [cruza(poblacion, padres) for x in range(N-1)]
        # Se aplican mutaciones con una cierta probabilidad
        hijos = [muta(x, tasaMutacion) for x in hijos]

        # Se añade el mejor individuo de la población anterior (elitismo)
        hijos.append(poblacion[-1])
        poblacion = hijos

        # Se ordenan los individuos por rendimiento
        poblacion.sort(key=lambda x: rendimiento(x))

    # Devuelve el mejor individuo encontrado
    return poblacion[-1]

# Declara una tupla con nombres para representar cada inversión
Inversion = namedtuple('Inversion', ['precio', 'cantidad', 'rendim'])

numInver = 100
maxPrecio = 1000
maxCant = 10
maxRend = 0.2

# Genera una lista de tuplas Inversion
inversiones=[Inversion(random()*maxPrecio, randint(1,maxCant), random()*maxRend) for i in range(numInver)]
print(inversiones)

capital = 50000
individuos = 20
generaciones = 1000

poblacion = [creaIndividuo(inversiones, capital) for i in range(individuos)]

mejor = evoluciona(poblacion, generaciones)
print(mejor, capitalInvertido(mejor), rendimiento(mejor))

def imprimir_inversiones(inversiones, individuo):
    for cantidad, inversion in zip(individuo, inversiones):
        if cantidad > 0:
            print(f"Inversión: Precio - {inversion.precio}, Cantidad - {cantidad}, Rendimiento - {inversion.rendim}")

print("------------------------------------------------------")

# Imprime solo las inversiones con cantidad mayor a 0 y agrega salto de línea para legibilidad
print("Mejores Bonos:")
imprimir_inversiones(inversiones, mejor)
print(f"\nCapital Invertido: {capitalInvertido}")
print(f"Rendimiento: {rendimiento(mejor)}")
