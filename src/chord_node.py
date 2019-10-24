import hashlib

MAX_HASH_VAL = 'ffffffffffffffffffffffffffffffffffffffff'
MIN_HASH_VAL = '0000000000000000000000000000000000000000'

def hash_i(hash_string):
    return int(hash_string, 16)

class ChordNode:

    def __init__(self, own_hash_val, network, successor_hash_val, predecessor_hash_val=None):
        self.own_hash_val = own_hash_val

        self.network = network

        self.successor_hash_list = [successor_hash_val]
        self.predecessor = predecessor_hash_val

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
        if hash_i(self.own_hash_val) < hash_i(self.successor_hash_list[0]):
            if hash_i(self.own_hash_val) < hash_i(hash_val) < int(self.successor_hash_list[0], 16):
                is_next_successor = True

        # 挟む場合
        else:
            if hash_i(self.own_hash_val) < hash_i(hash_val) < hash_i(MAX_HASH_VAL) or hash_i(MIN_HASH_VAL) < hash_i(hash_val) < int(self.successor_hash_list[0], 16):
                is_next_successor = True

        if not is_next_successor:
            return self.network.get_node(self.successor_hash_list[0]).get_successor(hash_val)

        return self.successor_hash_list[0]

    def stabilize_successor(self):
        successor_node = self.network.get_node(self.successor_hash_list[0])

        if not (successor_node_predecessor := successor_node.predecessor) == self.own_hash_val:
            successor_node.challenge_predecessor(self.own_hash_val)
            self.challenge_successor(successor_node.predecessor)


    def challenge_predecessor(self, predecessor_candidate_hash):
        # predecessorがNoneの場合
        if not self.predecessor:
            self.predecessor = predecessor_candidate_hash
            return

        # リングの0地点を挟まない場合
        if hash_i(self.predecessor) < hash_i(predecessor_candidate_hash) < hash_i(self.own_hash_val):
            self.predecessor = predecessor_candidate_hash
            return

        # old_predecessor < 0 < new_predecessor < own の場合
        if hash_i(self.predecessor) < 0 < hash_i(predecessor_candidate_hash) and hash_i(predecessor_candidate_hash) < hash_i(self.own_hash_val):
            self.predecessor = predecessor_candidate_hash
            return

        # old_predecessor < new_predecessor < 0 < own の場合
        if hash_i(self.predecessor) < hash_i(predecessor_candidate_hash) < 0 and 0 < hash_i(self.own_hash_val):
            self.predecessor = predecessor_candidate_hash
            return

    def challenge_successor(self, successor_candidate_hash):
        # successorのpredecessorがまだ空の場合
        if not successor_candidate_hash:
            return

         # リングの0地点を挟まない場合
        if hash_i(self.own_hash_val) < hash_i(successor_candidate_hash) < hash_i(self.successor_hash_list[0]):
            self.successor_hash_list = [successor_candidate_hash]
            return

        # self < 0 < new_successor < old_successor の場合
        if hash_i(self.own_hash_val) < 0 < hash_i(successor_candidate_hash) and hash_i(successor_candidate_hash) < hash_i(self.successor_hash_list[0]):
            self.successor_hash_list = [successor_candidate_hash]
            return

        # self < new_successor < 0 < old_successor の場合
        if hash_i(self.own_hash_val) < hash_i(successor_candidate_hash) < 0 and 0 < hash_i(self.successor_hash_list[0]):
            self.successor_hash_list = [successor_candidate_hash]
            return

    # データの追加を受け付ける
    def receive_value(self, key, value):
        hash_val = hashlib.sha1(key.encode()).hexdigest()

        is_next_successor = self.get_successor(hash_val)

        successor_node = self.network.get_node(self.successor_hash_list[0])

        key_value = dict()
        key_value[key] = value

        successor_node.store_value(hash_val, key_value, is_next_successor)

    # データの保存、自分が担当だった場合は保存、そうでなかったらsuccessorに依頼
    def store_value(self, hash_val, key_value, is_successor):
        if is_successor:
            self.store[hash_val] = key_value
        else:
            is_next_successor = self.get_successor(hash_val)

            successor_node = self.network.get_node(self.successor_hash_list[0])
            successor_node.store_value(hash_val, key_value, is_next_successor)
