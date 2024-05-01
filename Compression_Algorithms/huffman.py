class Node:
    def _init_(self, frequency, value):
        self.frequency = frequency
        self.value = value
        self.left = None
        self.right = None

def huffman(c):
    n = len(c)
    Q = [Node(frequency, value) for value, frequency in c.items()]

    print("Initial Queue:")
    print_queue(Q)

    for i in range(1, n):
        temp = Node(0, None)

        # Get two nodes with minimum frequencies
        left = get_min(Q)
        right = get_min(Q)

        # Assign left and right children
        temp.left = left
        temp.right = right

        # Calculate frequency of parent node
        temp.frequency = left.frequency + right.frequency

        # Insert new node back to the queue
        insert(Q, temp)

        print(f"Iteration {i}:")
        print("Merged nodes:", left.value, right.value)
        print("New node frequency:", temp.frequency)
        print("Queue:")
        print_queue(Q)

    return get_min(Q)

def get_min(Q):
    min_node = Q[0]
    min_index = 0
    for i in range(1, len(Q)):
        if Q[i].frequency < min_node.frequency:
            min_node = Q[i]
            min_index = i
    return Q.pop(min_index)

def insert(Q, node):
    Q.append(node)
    Q.sort(key=lambda x: x.frequency)

def print_queue(Q):
    for node in Q:
        print(f"({node.value}: {node.frequency})", end=", ")
    print()

# Example usage
character_freq = {'a': 5, 'b': 9, 'c': 12, 'd': 13, 'e': 16, 'f': 45}
root_node = huffman(character_freq)
print("Root node frequency:", root_node.frequency)