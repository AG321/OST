from network import Net
import math
import random
from pprint import pformat

# allocation pattern 

class Chromosome(object):
    def __init__(self, allocation_pattern: dict):
        self.allocation_pattern = allocation_pattern
        self.link_sizes = []
        self.link_loads = []
        self.number_of_genes = 0
        self.z = float('inf')

    def add_flow_values(self, new_mappings: dict):
        self.allocation_pattern = {**self.allocation_pattern, **new_mappings}

    def get_gene(self, demand_id):
        return {key: value for key, value in self.allocation_pattern.items() if key[0] == demand_id}

    def add_gene(self, gene: dict):
        self.add_flow_values(gene)
        self.number_of_genes += 1

    def mutate_gene(self, gene_number):
        gene = self.get_gene(gene_number)
        if len(gene) > 1:  # we cant mutate gene with only one value
            flows = random.sample(list(gene), 2)
            if self.allocation_pattern[flows[0]] > 0:
                self.allocation_pattern[flows[0]] -= 1
                self.allocation_pattern[flows[1]] += 1

    def calculate_links_for_problem(self, net: Net, problem: str):
        links = net.links
        link_values = [0] * len(net.links)
        paths = net.get_all_demand_paths()
        for link_id, link in enumerate(links):
            volume_sum = 0
            for path in paths:
                if link_id + 1 in path.links:
                    volume = self.allocation_pattern.get((path.demand_id, path.path_id))
                    volume_sum += volume
            link_values[link_id] = math.ceil(volume_sum / link.modul) if problem == "DDAP" else volume_sum
        if problem == "DDAP":
            self.link_sizes = link_values
        else:
            self.link_loads = link_values

    def calculate_links(self, net: Net):
        self.calculate_links_for_problem(net, "DDAP")
        self.calculate_links_for_problem(net, "DAP")

    def calculate_z(self, net: Net, problem: str):
        if problem =="DDAP":
            z = 0
            for link_id, link_size in enumerate(self.link_sizes):
                z += net.links[link_id].cost * link_size
            self.z = z
            return z
        else:
            z = float('-inf')
            for i, link_load in enumerate(self.link_loads):
                _z = link_load - net.links[i].number_of_modules * net.links[i].modul
                if _z > z:
                    z = _z
            self.z = z
            return z

    def __str__(self):
        text = "Flows dla (demand, path):\n" + pformat(self.allocation_pattern)

        if self.link_loads:
            text += f"\nLink loads: {self.link_loads}"
        if self.link_sizes:
            text += f"\nLink sizes: {self.link_sizes}"

        text += f"\nz = {self.z}"

        return text
