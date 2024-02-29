class Node:
    def __init__(self, word):
        self.word = word
        self.neighbors = []
        self.status = None


class Graph:
    def __init__(self, first_node, second_node):
        self.first_node = first_node
        self.second_node = second_node


class Network:
    def __init__(self, words_list):
        self.words_list = words_list
        self.nodes_list = []
        self.graphs_list = []

    def add_graph(self, first_node, second_node):
        new_graph = Graph(first_node, second_node)
        self.graphs_list.append(new_graph)
        first_node.neighbors.append(second_node)
        second_node.neighbors.append(first_node)

    def find_node_by_word(self, word):
        for node in self.nodes_list:
            if node.word == word:
                return node

    def find_neighbors(self, word):
        node = self.find_node_by_word(word)
        return node.neighbors()

    def make_neighbors_network(self):
        for word in self.words_list:
            new_node = Node(word)
            self.nodes_list.append(new_node)

        for word in self.words_list:
            for i in range(len(word)):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    if char != word[i]:
                        new_word = word[:i] + char + word[i + 1:]
                        if new_word in self.words_list:
                            first_node = self.find_node_by_word(word)
                            second_node = self.find_node_by_word(new_word)
                            self.add_graph(first_node, second_node)


'''def find_neighbors(word, words_list):
    neighbors = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != word[i]:
                new_word = word[:i] + char + word[i + 1:]
                if new_word in words_list:
                    neighbors.append(new_word)
    return neighbors'''


with open('words_alpha.txt', 'r') as file:
    words_list = [word.strip() for word in file]
network = Network(words_list)
