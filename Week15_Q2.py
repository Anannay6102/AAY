class Graph():
    def __init__(self):
        self.vertex = []
        self.adjacency_matrix = []

    def add_vertex(self, vertex):
        if vertex is not self.vertex:
            self.vertex.append(vertex)
            # Adding a row and column to the adjacency matrix
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

    def add_edge(self, start, end):
        if start in self.vertex and end in self.vertex:  # Checking if vertices exist in the graph
            # Finding index of the vertices
            start_index = self.vertex.index(start)
            end_index = self.vertex.index(end)
            # Adding to adjacency matrix
            self.adjacency_matrix[start_index][end_index] = 1
            self.adjacency_matrix[end_index][
                start_index] = 1  # Added twice because graph is undirected and so the connections are bi-directional

    def print_matrix(self):
        print("  " + " ".join(self.vertex))  # Allinging header row
        for i, row in enumerate(self.adjacency_matrix):
            val = " ".join(map(str, row))  # Getting value for each element of matrix
            print(val)

    def dfs(self, vertex_index, visited):
        visited[vertex_index] = True  # Marking the current vertex as visited
        # Looping through the adjacency matrix row for the current vertex
        for i, connected in enumerate(self.adjacency_matrix[vertex_index]):
            if connected and not visited[i]:  # Enumerating over adjacency matrix and looking for unvisited connection
                self.dfs(i, visited)

    def is_network_connected(self):
        visited = [False] * len(self.vertex)
        self.dfs(0, visited)
        return all(visited)


def create_ring_network(graph):
    for i in range(6):  # Defining number of vertices
        graph.add_vertex(str(i))  # Adding to graph as string value
    # Adding edge from each vertices
    for i in range(5):
        graph.add_edge(str(i), str(i + 1))
    graph.add_edge(str(5), str(0))  # Closing the ring


def create_star_network(graph):
    graph.add_vertex("Center")  # Adding center vertex
    for i in range(1, 7):
        graph.add_vertex("Node" + str(i))  # Adding the defined number of vertices as string value
        graph.add_edge("Center", "Node" + str(i))  # Adding edge from each vertices


# Worksheet Example Usage
# Create a network graph
network = Graph()

# Add vertices and connect them
network.add_vertex("A")
network.add_vertex("B")
network.add_edge("A", "B")

# Verify is all computers are connected
network.is_network_connected()
# Outputs True

# Add more computers to the network and connect them
network.add_vertex("C")
network.add_vertex("C")
network.add_edge("C", "D")

# Verify is all computers are connected
network.is_network_connected()
# Outputs False

# Ring Network
ring_network = Graph()

create_ring_network(ring_network)
print("Ring Network Adjacency Matrix:")
ring_network.output_matrix()
print("Is Ring Network Connected:", ring_network.is_network_connected())

# Star Network
star_network = Graph()

create_star_network(star_network)
print("\nStar Network Adjacency Matrix:")
star_network.output_matrix()
print("Is Star Network Connected:", star_network.is_network_connected())
