import random

i = 1
n = 0
step = 0

p = float(input("Ingrese la probabilidad de dar un paso hacia adelante (p): "))
n = int(input("Ingrese el numero de pasos (n): "))

posicion = 0
probabilidad_paso_adelante = p
probabilidad_paso_atras = 1 - p

for i in range(n):
    step = random.randint(0, 1)
    if(step < probabilidad_paso_adelante):
        posicion = posicion + 1
    else:
        posicion = posicion - 1

    print("Paso ", i, ": Posicion actual = ", posicion)