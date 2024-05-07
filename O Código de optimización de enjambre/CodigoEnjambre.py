from random import random


def funcion(x, y):
    sum1 = x ** 2 * (4 - 2.1 * x ** 2 + x ** 4 / 3.0)
    sum2 = x * y
    sum3 = y ** 2 * (-4 + 4 * y ** 2)
    return sum1 + sum2 + sum3


def aleatorio(inf, sup):
    return random() * (sup - inf) + inf


class Particula:
    # Parámetros para actualizar la velocidad
    inercia = 1.4
    cognitiva = 2.0
    social = 2.0

    # Límites del espacio de soluciones
    infx = -2.0
    supx = 2.0
    infy = -1.0
    supy = 1.0
    # Factor de ajuste de la velocidad inicial
    ajusteV = 100.0

    def __init__(self):
        self.x = aleatorio(Particula.infx, Particula.supx)
        self.y = aleatorio(Particula.infy, Particula.supy)
        self.vx = aleatorio(Particula.infx / Particula.ajusteV, Particula.supx / Particula.ajusteV)
        self.vy = aleatorio(Particula.infy / Particula.ajusteV, Particula.supy / Particula.ajusteV)
        self.xLoc = self.x
        self.yLoc = self.y
        self.valorLoc = funcion(self.x, self.y)

    # Actualiza la velocidad de la particula
    def actualizaVelocidad(self, xGlob, yGlob):
        cogX = Particula.cognitiva * random() * (self.xLoc - self.x)
        socX = Particula.social * random() * (xGlob - self.x)
        self.vx = Particula.inercia * self.vx + cogX + socX
        cogY = Particula.cognitiva * random() * (self.yLoc - self.y)
        socY = Particula.social * random() * (yGlob - self.y)
        self.vy = Particula.inercia * self.vy + cogY + socY

    def actualizaPosicion(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        # Debe mantenerse dentro del espacio de soluciones
        self.x = max(self.x, Particula.infx)
        self.x = min(self.x, Particula.supx)
        self.y = max(self.y, Particula.infy)
        self.y = min(self.y, Particula.supy)

        # Si es inferior a la mejor, la adopta como mejor
        valor = funcion(self.x, self.y)
        if valor < self.valorLoc:
            self.xLoc = self.x
            self.yLoc = self.y
            self.valorLoc = valor


def enjambreParticulas(particulas, iteraciones, reduccionInercia):
    # Registra la mejor posicion global y su valor
    mejorParticula = min(particulas, key=lambda p: p.valorLoc)
    xGlob = mejorParticula.xLoc
    yGlob = mejorParticula.yLoc
    valorGlob = mejorParticula.valorLoc

    # Bucle principal de simulacion
    for itera in range(iteraciones):
        # Actualiza la velocidad y posicion de cada particula
        for p in particulas:
            p.actualizaVelocidad(xGlob, yGlob)
            p.actualizaPosicion()

        # Hasta que no se han movido todas las particulas no se
        # actualiza el minimo global, para simular que todas se
        # mueven a la vez
        mejorParticula = min(particulas, key=lambda p: p.valorLoc)
        if mejorParticula.valorLoc < valorGlob:
            xGlob = mejorParticula.xLoc
            yGlob = mejorParticula.yLoc
            valorGlob = mejorParticula.valorLoc

            # Finalmente se reduce la inercia de las particulas
            Particula.inercia *= reduccionInercia

    return xGlob, yGlob, valorGlob

#Parametros del problema
nParticulas  = 10
iteraciones = 100
redInercia = 0.9

#Genera un conjunto inicial de particulas
particulas = [Particula() for i in range(nParticulas)]

# Ejecuta el algoritmo del enjambre de particuas
print(enjambreParticulas(particulas,iteraciones, redInercia))