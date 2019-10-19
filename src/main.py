from network import Network
from chord_node import ChordNode

if __name__ == '__main__':
    network = Network()

    node1 = ChordNode(
        '0000000000000000000000000000000000000000',
        network,
        '4444444444444444444444444444444444444444',
    )

    node2 = ChordNode(
        '4444444444444444444444444444444444444444',
        network,
        '8888888888888888888888888888888888888888',
    )

    node3 = ChordNode(
        '8888888888888888888888888888888888888888',
        network,
        'cccccccccccccccccccccccccccccccccccccccc',
    )

    node4 = ChordNode(
        'cccccccccccccccccccccccccccccccccccccccc',
        network,
        '0000000000000000000000000000000000000000',
    )

    network.nodes = {
        '0000000000000000000000000000000000000000': node1,
        '4444444444444444444444444444444444444444': node2,
        '8888888888888888888888888888888888888888': node3,
        'cccccccccccccccccccccccccccccccccccccccc': node4,
    }

    node3.receive_value('key1', 'value')
    node2.receive_value('key2', 'value')
    node1.receive_value('key3', 'value')
    node4.receive_value('key4', 'value')
    node1.receive_value('key5', 'value')
    node4.receive_value('key6', 'value')
    node2.receive_value('key7', 'value')
    node1.receive_value('key8', 'value')
    node1.receive_value('key9', 'value')
    node1.receive_value('key10', 'value')

    for hash_val, node in network.nodes.items():
        print(hash_val)
        print(node.store)