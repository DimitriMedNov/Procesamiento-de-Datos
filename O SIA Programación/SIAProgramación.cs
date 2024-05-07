using System;
using System.Collections;
using System.Collections.Generic;

namespace SistemaInmuneArtificial
{
    public static class Utils
    {
        // Convierte un BitArray en una cadena de caracteres representando 1s y 0s
        public static string BitArrayAsString(BitArray ba)
        {
            string result = "";
            foreach (bool bit in ba)
            {
                result += bit ? "1" : "0";
            }
            return result;
        }
    }

    class ProgramaSistemaInmuneArtificial
    {
        static Random random = new Random();

        static void Main(string[] args)
        {
            Console.WriteLine("\nComienzo de la demostración del Sistema Inmune Artificial para la Detección de Intrusos\n");

            int numPatternBits = 12;
            int numAntibodyBits = 4;
            int numLymphocytes = 3;
            int stimulationThreshold = 3;

            Console.WriteLine("Cargando conjunto de autoantígenos ('patrones históricos normales)");
            List<BitArray> selfSet = LoadSelfSet();
            ShowSelfSet(selfSet);

            Console.WriteLine("\nCreando conjunto de linfocitos utilizando selección negativa y detección de r-chunks");
            List<Lymphocyte> lymphocyteSet = CreateLymphocyteSet(selfSet, numAntibodyBits, numLymphocytes);
            ShowLymphocyteSet(lymphocyteSet);

            Console.WriteLine("\nComienzo de la simulación de detección de intrusiones del AIS\n");
            int time = 0;
            int maxTime = 6;
            List<BitArray> detectedAndRemovedPatterns = new List<BitArray>();
            int intrusionCount = 0;

            while (time < maxTime)
            {
                Console.WriteLine("============================================");
                BitArray incoming = RandomBitArray(numPatternBits);
                Console.WriteLine("Patrón entrante = " + Utils.BitArrayAsString(incoming) + "\n");

				bool isDetected = false;
                foreach (var lymph in lymphocyteSet)
                {
                    if (lymph.Detects(incoming))
                    {
                        Console.WriteLine("Patrón entrante detectado por un linfocito");
                        lymph.Stimulation++;
                        if (lymph.Stimulation >= stimulationThreshold)
                        {
                            Console.WriteLine("¡Linfocito estimulado! Patrón marcado para eliminación como posible intrusión.");
                            if (!isDetected)
                            {
                                detectedAndRemovedPatterns.Add(incoming);
                                intrusionCount++;
                                isDetected = true;
                            }
                        }
                        else
                        {
                            Console.WriteLine("Linfocito no supera el umbral de estimulación");
                        }
                    }
                    else
                    {
                        Console.WriteLine("Patrón entrante no detectado por el linfocito");
                    }
                }
                ++time;
                Console.WriteLine("============================================");
            }

            Console.WriteLine("\nIntrusiones detectadas:");
            foreach (var intrusion in detectedAndRemovedPatterns)
            {
                Console.WriteLine(Utils.BitArrayAsString(intrusion));
            }
            Console.WriteLine($"Total de intrusiones detectadas: {intrusionCount}");

            Console.WriteLine("\nFin de la demo del IDS AIS\n");
            Console.ReadLine();
        }

        static List<BitArray> LoadSelfSet()
        {
            // Cargar set de auto-antígenos, representando patrones normales
            return new List<BitArray>();
        }

        static void ShowSelfSet(List<BitArray> selfSet)
        {
            // Mostrar el set de auto-antígenos
            foreach (var ba in selfSet)
            {
                Console.WriteLine(Utils.BitArrayAsString(ba));
            }
        }

        static List<Lymphocyte> CreateLymphocyteSet(List<BitArray> selfSet, int numAntibodyBits, int numLymphocytes)
        {
            // Crear un set de linfocitos usando selección negativa y detección r-chunks
            return new List<Lymphocyte>();
        }

        static void ShowLymphocyteSet(List<Lymphocyte> lymphocyteSet)
        {
            // Mostrar el set de linfocitos
            Console.WriteLine("\nLymphocyte set:");
            foreach (Lymphocyte lymph in lymphocyteSet)
            {
                Console.WriteLine(lymph.ToString());
            }
        }

        static BitArray RandomBitArray(int numBits)
        {
            // Generar un BitArray aleatorio para simular patrones entrantes
            BitArray ba = new BitArray(numBits);
            for (int i = 0; i < numBits; ++i)
            {
                ba[i] = random.NextDouble() > 0.5;
            }
            return ba;
        }
    }

    class Lymphocyte
    {
        public BitArray Antibody;
        public int Stimulation;

        public Lymphocyte(BitArray antibody)
        {
            Antibody = antibody;
            Stimulation = 0;
        }

        // Detectar si un patrón coincide con el anticuerpo del linfocito
        public bool Detects(BitArray pattern)
        {
            for (int i = 0; i < pattern.Count; ++i)
            {
                if (pattern[i] != Antibody[i])
                    return false;
            }
            return true;
        }

        public override string ToString()
        {
            // Representación en cadena de un linfocito
            return $"Antibody: {Utils.BitArrayAsString(Antibody)}, Stimulation: {Stimulation}";
        }
    }
}