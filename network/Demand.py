class Demand:

    def __init__(self, data, demand_id):
        self.node1 = data[0]
        self.node2 = data[1]
        self.volume = int(data[2])
        self.id = demand_id
        self.demand_paths = []

    def get_number_of_paths(self):
        return len(self.demand_paths)
