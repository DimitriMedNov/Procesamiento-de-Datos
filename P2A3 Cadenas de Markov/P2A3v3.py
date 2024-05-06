alpha = 0.0
beta = 0.0
pi_A = 0.0
pi_B = 0.0

alpha = int(input("Ingrese la probabilidad de cambio de cafe A a B (alpha): "))
beta = int(input("Ingrese la porbabilidad de cambio de cafe B a A (beta): "))

pi_A = beta/ (alpha+beta)
pi_B = alpha / (alpha + beta)

print("La probabilidad de que una persona que pide cafe A lo pida tambien n dias mas tarde es ", pi_A)
print("La proporcion de cafe A que deberia encargar el bar a largo plazo es ", pi_A)
print("La proporcion de cafe B que deberia encargar el bar a largo plazo es ", pi_B)