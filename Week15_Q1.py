class Network:
    # Initialize an empty Networks
    def __init__(self):
        self.members = []
        self.relationships = []

    # Create a new member
    def add_member(self, name, age, location):
        member = Node(name, age, location)
        self.members.append(member)

    # Search for a member by name
    def find_member_by_name(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None

    # Add a bidirectional relationship
    def add_relationship(self, first_name, second_name):
        first_member = self.find_member_by_name(first_name)
        second_member = self.find_member_by_name(second_name)
        if first_member and second_member:  # check if members exist
            first_member.friends.append(second_member)  # if it is, 1. add friends
            second_member.friends.append(first_member)
            relationship = Graph(first_member, second_member)  # 2.make relationship (graph between nodes)
            self.relationships.append(relationship)  # 3. add relationship
        else:  # if it is not, at least one account does not exist
            pass

    # Printing network information
    def print_information(self):
        member_names = [member.name for member in self.members]
        relationship_names = [f"{relationship.first_member.name} - {relationship.second_member.name}" for relationship
                              in self.relationships]
        print(f'Members:{member_names} \nRelationships:{relationship_names}')

    # Find and return the names of all friends of given user
    def find_friends(self, name):
        member = self.find_member_by_name(name)
        if member:
            return [friend.name for friend in member.friends]
        return []

    # Find the least number of edges between two users using BFS
    def shortest_path(self, start_name, end_name):
        start_member = self.find_member_by_name(start_name)
        end_member = self.find_member_by_name(end_name)
        if not start_member or not end_member:
            return None  # Member or members do not exist

        visited = set()
        queue = [(start_member, 0)]  # Initialize queue with the starting node

        while queue:
            current_member, distance = queue.pop(0)  # Dequeue the next member
            if current_member == end_member:
                return distance

            if current_member not in visited:
                visited.add(current_member)  # Mark the current node visited
                for friend in current_member.friends:
                    if friend not in visited:
                        queue.append((friend, distance + 1))

        return None


# Initialize nodes
class Node:
    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.location = location
        self.friends = []


# Creating Graph relationships
class Graph:
    def __init__(self, first_member, second_member):
        self.first_member = first_member
        self.second_member = second_member


# Create a new social network
network = Network()

# Add some members to the network
network.add_member("Alice", age=25, location="New York")
network.add_member("Bob", age=30, location="Los Angeles")
network.add_member("Charlie", age=35, location="Chicago")
network.add_member("David", age=40, location="Seattle")

# Add some relationships between members
network.add_relationship("Alice", "Bob")
network.add_relationship("Bob", "Charlie")
network.add_relationship("Charlie", "David")

# Find all the friends of Alice
alice_friends = network.find_friends("Alice")
print(alice_friends)  # Output: ["Bob"]

# Find the shortest path between Alice and David
shortest_path = network.shortest_path("Alice", "David")
print(shortest_path)  # Output: 3

# Printing all information about network
network.print_information()
