import numpy as np

class NeuronaArtificial:
    def __init__(self, num_entradas, tasa_aprendizaje=0.1, num_iteraciones=1000):
        self.pesos = np.random.rand(num_entradas)
        self.sesgo = np.random.rand()
        self.tasa_aprendizaje = tasa_aprendizaje
        self.num_iteraciones = num_iteraciones

    def funcion_activacion(self, suma_ponderada):
        return 1 / (1 + np.exp(-suma_ponderada))

    def entrenar(self, entradas, salida_deseada):
        for _ in range(self.num_iteraciones):
            for entrada, salida_esperada in zip(entradas, salida_deseada):
                suma_ponderada = np.dot(entrada, self.pesos) + self.sesgo
                salida_calculada = self.funcion_activacion(suma_ponderada)

                error = salida_esperada - salida_calculada
                ajuste = error * salida_calculada * (1 - salida_calculada)

                self.pesos += self.tasa_aprendizaje * ajuste * entrada
                self.sesgo += self.tasa_aprendizaje * ajuste

    def predecir(self, entrada):
        suma_ponderada = np.dot(entrada, self.pesos) + self.sesgo
        return self.funcion_activacion(suma_ponderada)


# Ejemplo de uso
num_entradas = 2
entradas = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
salida_deseada = np.array([0, 1, 1, 1])

neurona = NeuronaArtificial(num_entradas)
neurona.entrenar(entradas, salida_deseada)

# Prueba con un nuevo dato
entrada_prueba = np.array([1, 0])
print("Predicción:", neurona.predecir(entrada_prueba))
