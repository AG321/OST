from algorithms import ForBothAlgorithms
from network.Chromosome import Chromosome
from network.Net import Net
from typing import List
import random
import copy
from time import time
# import algorithms


class EvolutionaryAlgorithm:
    def __init__(self,
                 problem: str,
                 seed: int,
                 net: Net,
                 number_of_chromosomes: int,
                 max_time: int,
                 max_generations: int,
                 max_mutations: int,
                 max_no_progress_generations: int,
                 percent_of_best_chromosomes: float,
                 crossover_probability: float,
                 mutation_probability: float
                 ):

        random.seed(seed)

        self.problem = problem
        self.net = net
        self.number_of_chromosomes = number_of_chromosomes
        self.generation = 0
        self.without_progress = 0
        self.mutation = 0
        self.max_generations = max_generations
        self.max_mutations = max_mutations
        self.max_generations_without_progress = max_no_progress_generations
        self.max_time = max_time
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

        self.initial_time = None
        self.history = []

        self.percent_of_best_chromosomes = percent_of_best_chromosomes
        self.number_of_best_chromosomes = round(number_of_chromosomes * percent_of_best_chromosomes)
        self.population_padding = number_of_chromosomes - self.number_of_best_chromosomes

    def compute(self) -> Chromosome:
        # choose starting population
        population = self.get_init_population()
        final_solution = Chromosome({})
        self.initial_time = time()

        while not self.ending_cases():
            self.generation += 1
            best_chromosome_in_generation = Chromosome({})

            # calculate cost function for current generation
            for chromosome in population:
                chromosome.calculate_links_for_problem(self.net, self.problem)
                if chromosome.calculate_z(self.net, self.problem) < best_chromosome_in_generation.z:
                    best_chromosome_in_generation = copy.deepcopy(
                        chromosome)

            self.history.append(best_chromosome_in_generation)

            print(f"Generacja: {self.generation} koszt: {best_chromosome_in_generation.z}")

            if best_chromosome_in_generation.z < final_solution.z:
                final_solution = copy.deepcopy(best_chromosome_in_generation)
                self.without_progress = 0
            else:
                self.without_progress += 1

            # eliminate weakest chromosomes
            population = self.fittest_selector(population)

            # crossover
            crossed_population = []
            while len(population) > 1:
                parents = random.sample(population, 2)
                population.remove(parents[0])
                population.remove(parents[1])
                crossed_population += (self.corssover(parents) if self.crossover_happened() else parents)

            population += crossed_population

            # mutation
            for chromosome in population:
                if self.mutation_happened():  # chromosome mutation
                    for i in range(chromosome.number_of_genes):
                        if self.mutation_happened():  # gene mutation
                            chromosome.mutate_gene(i + 1)
                            self.mutation += 1

        print(f"Rozwiazanie znaleziono w czasie: {round(time() - self.initial_time, 2)} s.")

        # calculate link values for both problems to save full information in output files
        for solution in self.history:
            solution.calculate_links(self.net)

        final_solution.calculate_links(self.net)

        return final_solution

    def fittest_selector(self, population: List):
        population.sort(key=lambda x: x.z)
        best_chromosomes = population[:self.number_of_best_chromosomes]
        padding = [copy.deepcopy(best_chromosomes[i]) for i in range(self.population_padding)]
        return best_chromosomes + padding

    def corssover(self, parents):
        father = parents[0]
        mother = parents[1]
        brother = Chromosome({})
        sister = Chromosome({})

        number_of_genes = father.number_of_genes

        for gene_number in range(number_of_genes):
            if random.random() > 0.5:
                brother.add_gene(father.get_gene(gene_number + 1))
                sister.add_gene(mother.get_gene(gene_number + 1))
            else:
                brother.add_gene(mother.get_gene(gene_number + 1))
                sister.add_gene(father.get_gene(gene_number + 1))

        return [brother, sister]

    def get_init_population(self) -> List:
        all_genes_combinations = [ForBothAlgorithms.get_chromosomes_with_one_gene(demand) for demand in
                                  self.net.demands]
        chromosomes = []

        for i in range(self.number_of_chromosomes):
            chromosome = Chromosome({})
            for gene_combination in all_genes_combinations:
                gene = random.choice(gene_combination).allocation_pattern
                chromosome.add_gene(gene)
            chromosome.calculate_links_for_problem(self.net, problem=self.problem)
            chromosomes.append(chromosome)

        random.shuffle(chromosomes)
        return chromosomes

    def ending_cases(self) -> bool:
        time_exceeded = time() - self.initial_time >= self.max_time
        if time_exceeded:
            print("Wstrzymano obliczenie z powodu przekroczenia limitu czasu.")
            return True

        generations_exceeded = self.generation >= self.max_generations
        if generations_exceeded:
            print("Wstrzymano obliczenie z powodu przekroczenia limitu generacji.")
            return True

        mutations_exceeded = self.mutation >= self.max_mutations
        if mutations_exceeded:
            print("Wstrzymano obliczenie z powodu przekroczenia limitu mutacji.")
            return True

        without_progress = self.without_progress >= self.max_generations_without_progress
        if without_progress:
            print("Wstrzymano obliczenie z powodu braku poprawy wyniku.")
            return True

        return False


    def crossover_happened(self) -> bool:
        return random.random() < self.crossover_probability

    def mutation_happened(self) -> bool:
        return random.random() < self.mutation_probability

