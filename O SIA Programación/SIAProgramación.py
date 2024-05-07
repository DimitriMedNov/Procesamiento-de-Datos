from random import random
from typing import List


class Utils:
    @staticmethod
    def bit_array_as_string(bit_array):
        return ''.join(['1' if bit else '0' for bit in bit_array])


class Lymphocyte:
    def __init__(self, antibody):
        self.antibody = antibody
        self.stimulation = 0

    def detects(self, pattern):
        return all(x == y for x, y in zip(self.antibody, pattern))

    def __str__(self):
        return f"Antibody: {Utils.bit_array_as_string(self.antibody)}, Stimulation: {self.stimulation}"


def random_bit_array(num_bits):
    return [random() > 0.5 for _ in range(num_bits)]


def load_self_set():
    return []


def show_self_set(self_set):
    for ba in self_set:
        print(Utils.bit_array_as_string(ba))


def create_lymphocyte_set(self_set, num_antibody_bits, num_lymphocytes):
    return []


def show_lymphocyte_set(lymphocyte_set):
    print("\nLymphocyte set:")
    for lymph in lymphocyte_set:
        print(lymph)


def main():
    print("\nComienzo de la demostración del Sistema Inmune Artificial para la Detección de Intrusos\n")

    num_pattern_bits = 12
    num_antibody_bits = 4
    num_lymphocytes = 3
    stimulation_threshold = 3

    print("Cargando conjunto de autoantígenos ('patrones históricos normales')")
    self_set = load_self_set()
    show_self_set(self_set)

    print("\nCreando conjunto de linfocitos utilizando selección negativa y detección de r-chunks")
    lymphocyte_set = create_lymphocyte_set(self_set, num_antibody_bits, num_lymphocytes)
    show_lymphocyte_set(lymphocyte_set)

    print("\nComienzo de la simulación de detección de intrusiones del AIS\n")
    time = 0
    max_time = 6
    detected_and_removed_patterns = []
    intrusion_count = 0

    while time < max_time:
        print("============================================")
        incoming = random_bit_array(num_pattern_bits)
        print(f"Patrón entrante = {Utils.bit_array_as_string(incoming)}\n")

        is_detected = False
        for lymph in lymphocyte_set:
            if lymph.detects(incoming):
                print("Patrón entrante detectado por un linfocito")
                lymph.stimulation += 1
                if lymph.stimulation >= stimulation_threshold:
                    print("¡Linfocito estimulado! Patrón marcado para eliminación como posible intrusión.")
                    if not is_detected:
                        detected_and_removed_patterns.append(incoming)
                        intrusion_count += 1
                        is_detected = True
                else:
                    print("Linfocito no supera el umbral de estimulación")
            else:
                print("Patrón entrante no detectado por el linfocito")
        time += 1
        print("============================================")

    print("\nIntrusiones detectadas:")
    for intrusion in detected_and_removed_patterns:
        print(Utils.bit_array_as_string(intrusion))
    print(f"Total de intrusiones detectadas: {intrusion_count}")

    print("\nFin de la demo del IDS AIS\n")


if __name__ == '__main__':
    main()

