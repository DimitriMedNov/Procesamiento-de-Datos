import random
alpha = 0.0
beta = 0.0
pi_A = 0.0
pi_B = 0.0

def randomProb(dias):
    for i in range(dias):
        alpha = random.randint(1, 100)
        beta = random.randint(1, 100)
        pi_A = beta/ (alpha+beta)
        pi_B = alpha / (alpha + beta)
        print("-------------------EN EL DIA "+ str(i + 1) + "------------------------------------------------")
        print("La probabilidad de que una persona que pide cafe A lo pida tambien n dias mas tarde es ", pi_A)
        print("La proporcion de cafe A que deberia encargar el bar a largo plazo es ", pi_A)
        print("La proporcion de cafe B que deberia encargar el bar a largo plazo es ", pi_B)


randomProb(5)