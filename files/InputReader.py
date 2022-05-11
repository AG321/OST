from network.Net import Net
from network.Link import Link
from network.Demand import Demand
from network.Route import Route


class InputReader:

    @staticmethod
    def parse_line(raw_line: str):
        return raw_line.strip().split(" ")

    def parse_network(self, file: str):
        net = Net()
        with open(file) as file:

            links = int(file.readline())
            for i in range(links):
                link_data = self.parse_line(file.readline())
                link = Link(data=link_data)
                net.links.append(link)

            file.readline()  # for -1 line
            file.readline()  # for empty line

            demands = int(file.readline())
            file.readline()  # for empty line

            for demand_number in range(demands):
                demand_data = self.parse_line(file.readline())
                demand = Demand(data=demand_data, demand_id=demand_number + 1)
                number_of_demand_paths = int(file.readline())

                for demand_path_number in range(number_of_demand_paths):
                    demand_path_data = self.parse_line(file.readline())
                    demand_path = Route(data=demand_path_data, demand_id=demand_number + 1)
                    demand.demand_paths.append(demand_path)

                net.demands.append(demand)
                file.readline()  # for empty line

        return net
