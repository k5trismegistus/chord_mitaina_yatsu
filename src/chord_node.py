import hashlib

MAX_HASH_VAL = 'ffffffffffffffffffffffffffffffffffffffff'
MIN_HASH_VAL = '0000000000000000000000000000000000000000'
# ハッシュのビット長
BITS = 160

def hash_i(hash_string):
    return int(hash_string, 16)


class ChordNode:

    def __init__(self, own_hash_val, network, successor_hash_val, predecessor_hash_val=None):
        self.own_hash_val = own_hash_val

        self.network = network

        self.successor_hash_list = [successor_hash_val]
        self.predecessor = predecessor_hash_val
        # 今回は簡易実装なので、Fingerは2^80先のものだけにする
        self.finger_hash = None

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

        if self.clockwise_distance(hash_val) < self.clockwise_distance(self.successor_hash_list[0]):
            is_next_successor = True

        if not is_next_successor:
            return self.network.get_node(self.successor_hash_list[0]).get_successor(hash_val)

        return self.successor_hash_list[0]

    def stabilize_successor(self):
        successor_node = self.network.get_node(self.successor_hash_list[0])

        if not (successor_node_predecessor := successor_node.predecessor) == self.own_hash_val:
            successor_node.challenge_predecessor(self.own_hash_val)
            self.challenge_successor(successor_node.predecessor)

    def stabilize_finger(self):
        target = hex((hash_i(self.own_hash_val) + (2 ** 159) - 1) % 2 ** 160)
        self.finger_hash = self.get_successor(target)

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

        successor_node = self.network.get_node(self.successor_hash_list[0])
        if not self.clockwise_distance(hash_val) < self.clockwise_distance(self.successor_hash_list[0]):
            successor_node.receive_value(key, value)
            return

        successor_node.store_value(hash_val, key, value)

    # データの保存
    def store_value(self, hash_val, key, value):
        dt = dict()
        dt[key] = value
        self.store[hash_val] = dt

    def query_value(self, key):
        print(self.own_hash_val)
        hash_val = hashlib.sha1(key.encode()).hexdigest()
        if rst := self.store.get(hash_val, None):
            return rst

        successor_node = self.network.get_node(self.successor_hash_list[0])
        return successor_node.query_value(key)

    def clockwise_distance(self, target_hash):
        return (hash_i(target_hash) - hash_i(self.own_hash_val)) % 2 ** 160
