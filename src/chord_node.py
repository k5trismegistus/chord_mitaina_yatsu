import hashlib

MAX_HASH_VAL = 'ffffffffffffffffffffffffffffffffffffffff'
MIN_HASH_VAL = '0000000000000000000000000000000000000000'

class ChordNode:

    def __init__(self, own_hash_val, network, successor_hash_val):
        self.own_hash_val = own_hash_val

        self.network = network

        self.successor_list = [successor_hash_val]

        self.store = dict()

    @classmethod
    def new(cls, own_hash_val, network, initial_contact_hash):
        initial_contact_node = network.get_node(initial_contact_hash)
        successor_hash = initial_contact_node.get_successor(own_hash_val)

        ins = cls(own_hash_val, network, successor_hash)
        network.nodes[own_hash_val] = ins

        return ins

    # 与えられたハッシュ値に対して、そのハッシュ値の担当ノードのハッシュ値を返す
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

        if not is_next_successor:
            return self.network.get_node(self.successor_list[0]).get_successor(hash_val)

        return self.successor_list[0]

    # データの追加を受け付ける
    def receive_value(self, key, value):
        hash_val = hashlib.sha1(key.encode()).hexdigest()

        is_next_successor = self.get_successor(hash_val)

        successor_node = self.network.get_node(self.successor_list[0])

        key_value = dict()
        key_value[key] = value

        successor_node.store_value(hash_val, key_value, is_next_successor)

    # データの保存、自分が担当だった場合は保存、そうでなかったらsuccessorに依頼
    def store_value(self, hash_val, key_value, is_successor):
        if is_successor:
            self.store[hash_val] = key_value
        else:
            is_next_successor = self.get_successor(hash_val)

            successor_node = self.network.get_node(self.successor_list[0])
            successor_node.store_value(hash_val, key_value, is_next_successor)
