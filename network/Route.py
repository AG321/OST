class Route:
    def __init__(self, data: list, demand_id: int):
        self.demand_id = demand_id
        self.path_id = int(data[0])

        self.links = [int(link_id) for link_id in data[1:]]
