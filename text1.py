class Graph():
    def __init__(self):
        self.vertex = []
        self.adjacency_matrix = []

    def add_vertex(self, vertex):
        if vertex is not self.vertex:
            self.vertex.append(vertex)
            for row in self.adjacency_matrix:
                row.append(0)
            self.adjacency_matrix.append([0] * len(self.vertex))

    def remove_vertex(self, vertex):
        if vertex is self.vertex:
            position = self.vertex.index(vertex)
            self.vertex.pop(position)
            for row in self.adjacency_matrix:
                row.pop(position)
            self.adjacency_matrix.pop(position)

    def output_matrix(self):
        for row in self.adjacency_matrix:
            print(row)
