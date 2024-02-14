class Network:
    def __init__(self):
        self.members = []
        self.relationships = []

    def add_member(self, name, age, location):
        member = Node(name, age, location)
        self.members.append(member)

    def find_member_by_name(self, name):
        m = False
        for member in self.members:
            if member.name == name:
                m = member
                break
        return m

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

    def print_information(self):
        member_names = [member.name for member in self.members]
        relationship_names = [f"{relationship.first_member.name} - {relationship.second_member.name}" for relationship in self.relationships]
        print(f'Members:{member_names} \nRelationships:{relationship_names}')


class Node:
    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.location = location
        self.friends = []

class Graph:
    def __init__(self, first_member, second_member):
        self.first_member = first_member
        self.second_member = second_member


network = Network()
network.add_member('Arkadii', 18, 'Russia')
network.add_member('Joe', 30, 'UK')
network.add_relationship('Joe', 'Arkadii')
network.print_information()
