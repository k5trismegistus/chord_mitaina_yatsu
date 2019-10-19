class Network:
    def __init__(self):
        self.nodes = dict()

    def get_node(self, hash_val):
        return self.nodes[hash_val]