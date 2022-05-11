from network.Demand import Demand
from network.Link import Link
import itertools
from typing import List
from network.Route import Route


class Net:
    def __init__(self):
        self.links = []
        self.demands = []

    def get_link(self, link_id) -> Link:
        return self.links[link_id - 1]

    def get_demand(self, demand_id) -> Demand:
        return self.demands[demand_id - 1]

    def get_all_demand_paths(self) -> List[Route]:
        demand_paths = [demand.demand_paths for demand in self.demands]
        return list(itertools.chain.from_iterable(demand_paths))
