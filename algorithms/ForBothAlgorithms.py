from network.Demand import Demand
from network.Chromosome import Chromosome
from itertools import product
from typing import List


def get_chromosomes_with_one_gene(demand: Demand) -> List[Chromosome]:
    volume = range(demand.volume + 1)
    volume_for_path = [volume for _ in range(demand.get_number_of_paths())]

    volume_split = [combination for combination in product(*volume_for_path) if
                    sum(combination) == demand.volume]

    solutions = [Chromosome(build_gene(combination, demand)) for combination in volume_split]
    return solutions


def build_gene(combination: tuple, demand: Demand):
    allocation = {}
    for demand_path in demand.demand_paths:
        path_id = demand_path.path_id
        flow = (demand.id, path_id)
        allocation[flow] = combination[path_id - 1]
    return allocation
