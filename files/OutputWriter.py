from network.Chromosome import Chromosome
from network.Net import Net


class OutputWriter:
    def __init__(self, net):
        self.net = net
    
    def solution(self, solution: Chromosome, file_name: str):
        with open(file_name, "w+") as out_file:
            links = len(self.net.links)
            out_file.write(f"{links}\n\n")

            for link_id in range(links):
                out_file.write(f"{link_id + 1} ")
                out_file.write(f"{solution.link_loads[link_id]} ")
                out_file.write(f"{solution.link_sizes[link_id]}\n")

            out_file.write("\n")
            demands = len(self.net.demands)

            out_file.write(f"{demands}\n\n")

            for i in range(demands):
                gene = solution.get_gene(i + 1)
                used_flows = {key: val for key, val in gene.items() if val > 0}
                out_file.write(f"{i + 1} ")
                out_file.write(f"{len(used_flows)}\n")

                for key in used_flows.keys():
                    out_file.write(f"{key[1]} {used_flows[key]}\n")
                out_file.write("\n")

            print(f"Wynik zapisano w pliku:  {file_name}")

    @staticmethod
    def history(history, file_name: str):
        with open(file_name, "w+") as out_file:
            for generation, solution in enumerate(history):
                out_file.write("#" * 20 + f" Generacja: {generation + 1} " + "#" * 20 + "\n\n")
                out_file.write(f"{solution}")
                out_file.write("\n")
                out_file.write("\n")
