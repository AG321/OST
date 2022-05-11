class Link:

    def __init__(self, data):
        self.start_node = data[0]
        self.end_node = data[1]
        self.number_of_modules = int(data[2])
        self.cost = int(data[3])
        self.modul = int(data[4])