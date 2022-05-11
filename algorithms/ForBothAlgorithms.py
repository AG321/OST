from network.Demand import Demand
from network.Chromosome import Chromosome
from itertools import product
from typing import List

# funcion get one demand and return list of chromosomes
# volume it take range of demand ex. rang(0,4)
# volume_for_path makes array in size of get number_of_paths, each elements is volume eg. [range(0, 4), range(0, 4), range(0, 4)]
# volume_split  is result of function product, which allows to iterate by tuple
# volume_split eg. [(0, 0, 3), (0, 1, 2), (0, 2, 1), (0, 3, 0), (1, 0, 2), (1, 1, 1), (1, 2, 0), (2, 0, 1), (2, 1, 0), (3, 0, 0)]
# next uses build_gene
# build Chromosome for each combination, uses allocation_pattern
def get_chromosomes_with_one_gene(demand: Demand) -> List[Chromosome]:
    volume = range(demand.volume + 1)
    volume_for_path = [volume for _ in range(demand.get_number_of_paths())]
    volume_split = [combination for combination in product(*volume_for_path) if
                    sum(combination) == demand.volume]
    solutions = [Chromosome(build_gene(combination, demand)) for combination in volume_split]
    return solutions

# takes combinations store in array volume_split, one combination eg (0, 1, 2)
# takes demanad, from demand takes path_id and build flow { demand.id, path_id}
# makes dict form flow and combination
# one row, eg. {(1, 1): 0, (1, 2): 0, (1, 3): 3}
def build_gene(combination: tuple, demand: Demand):
    allocation = {}
    for demand_path in demand.demand_paths:
        path_id = demand_path.path_id
        flow = (demand.id, path_id)
        allocation[flow] = combination[path_id - 1]
    return allocation
