import hashlib

MAX_HASH_VAL = 'ffffffffffffffffffffffffffffffffffffffff'
MIN_HASH_VAL = '0000000000000000000000000000000000000000'

class ChordNode:

    # def __init__(self, own_hash_val, network, initial_node_hash_val):
    #     self.own_hash_val = own_hash_val

    #     # Join
    #     first_connect_node = network.get_node(initial_node_hash_val)
    #     successor = first_connect_node.get_successor(own_hash_val)
    #     self.successor_list = [successor]

    #     self.store = dict()

    def __init__(self, own_hash_val, network, successor_hash_val):
        self.own_hash_val = own_hash_val

        self.network = network

        self.successor_list = [successor_hash_val]

        self.store = dict()

    def get_successor(self, hash_val):
        is_next_successor = False

        # ループの0位置を挟まない場合
        if int(self.own_hash_val, 16) < int(self.successor_list[0], 16):
            if int(self.own_hash_val, 16) < int(hash_val, 16) < int(self.successor_list[0], 16):
                is_next_successor = True

        # 挟む場合
        else:
            if int(self.own_hash_val, 16) < int(hash_val, 16) < int(MAX_HASH_VAL, 16) or int(MIN_HASH_VAL, 16) < int(hash_val, 16) < int(self.successor_list[0], 16):
                is_next_successor = True

        if is_next_successor:
            return self.successor_list[0]
        else:
            self.network.get_node(self.successor_list[0]).get_successor(hash_val)

    def receive_value(self, key, value):
        hash_val = hashlib.sha1(key.encode()).hexdigest()

        is_next_successor = self.get_successor(hash_val)

        successor_node = self.network.get_node(self.successor_list[0])

        key_value = dict()
        key_value[key] = value

        successor_node.store_value(hash_val, key_value, is_next_successor)

    def store_value(self, hash_val, key_value, is_successor):
        if is_successor:
            self.store[hash_val] = key_value
        else:
            is_next_successor = self.get_successor(hash_val)

            successor_node = self.network.get_node(self.successor_list[0])
            successor_node.store_value(hash_val, key_value, is_next_successor)
