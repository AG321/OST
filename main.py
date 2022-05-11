import argparse

from algorithms import BruteForce
from files.InputReader import InputReader
from files.OutputWriter import OutputWriter
from algorithms.Evolutionary import EvolutionaryAlgorithm

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--algorytm",type=str, help="Nazwa algorytmu")
    parser.add_argument("-p", "--plik", help="Nazwa pliku wejsciowego")
    parser.add_argument("-w", "--wynik", help="Nazwa pliku wyjsciowego")
    parser.add_argument("-H", "--historia", help="Nazwa pliku z historia")
    parser.add_argument("-P", "--problem", help="Nazwa problemu")

    args = parser.parse_args()

    solution = None
    net_parser = InputReader()
    net = net_parser.parse_network(args.plik)
    output_writer = OutputWriter(net=net)
    if args.algorytm == "EA":
        EA = EvolutionaryAlgorithm(
            problem=args.problem,
            net=net,
            seed=15,
            number_of_chromosomes=1000,
            max_no_progress_generations=20,
            max_generations=100,
            max_mutations=1000000,
            max_time=300,
            percent_of_best_chromosomes=0.7,
            crossover_probability=0.6,
            mutation_probability=0.03
        )
        solution = EA.compute()
        output_writer.history(EA.history, file_name=args.historia)
    else:
        solution = BruteForce.compute(net, problem=args.problem)

    print(f"\nRozwiazanie koncowe:\n{solution}\n")
    output_writer.solution(solution=solution, file_name=args.wynik)


