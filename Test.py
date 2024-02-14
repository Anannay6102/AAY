class Network:
    def __init__(self):
        self.members = []
        self.relationships = []
    def add_member(self, name, age, location):
        member = Node(name, age, location)
        self.members += member

    def add_relationship(self,first_person, second_person):
        first_person.friends += second_person
        second_person.friends += first_person
        relationship = Graph(first_person, second_person)
        self.relationships += relationship

class Node:
    def __init__(self, name, age, location):
        self.name = name
        self.age = age
        self.location = location
        self.friends = []


class Graph:
    def __init__(self, first_person, second_person):
        self.first_person = first_person
        self.second_location = second_person
