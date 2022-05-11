import algorithms
from algorithms import ForBothAlgorithms
from network.Chromosome import Chromosome
from network.Demand import Demand
from network.Net import Net
from typing import List
from itertools import product
from time import time


def compute(net: Net, problem: str) -> Chromosome:
    start_time = time()
    solutions = get_all_possible_chromosomes(net.demands)
    for solution in solutions:
        solution.calculate_links_for_problem(net, problem=problem)

    print("Current best cost is: ", end="")

    best_cost = float("inf")
    best_solution = None
    for solution in solutions:
        cost = solution.calculate_z(net, problem)
        if cost < best_cost:
            best_cost = cost
            best_solution = solution
            print(f" {best_cost}", end="")
    print(f"\nRozwiazanie znaleziono w:  {round(time() - start_time, 2)} s.")
    best_solution.calculate_links(net)
    return best_solution

# function .get_chromosomes_with_one_gene(demand) returns list of possible chromoseomes for one demand
# all_combinations return list of all possible chromosomes for all demands
def get_all_possible_chromosomes(demands: List[Demand]) -> List[Chromosome]:
    all_combinations_all_demands = [ForBothAlgorithms.get_chromosomes_with_one_gene(demand) for demand in demands]
    indexes = [range(len(combination)) for combination in all_combinations_all_demands]
    solution_indexes = list(product(*indexes))
    print("Generating all possible solutions... ", end="")
    solutions = [get_complete_chromosome(all_combinations_all_demands, current_solution_index) for
                 current_solution_index
                 in solution_indexes]
    print(f"{len(solutions)} found.")
    return solutions


def get_complete_chromosome(demand_combination_matrix: List[List[Chromosome]], current_solution: tuple) -> Chromosome:
    complete_solution = Chromosome({})
    for demand_index, combination_index in enumerate(current_solution):
        solution = demand_combination_matrix[demand_index][combination_index]
        complete_solution.add_flow_values(solution.allocation_pattern)
    return complete_solution
