import time
class Node:
    def __init__(self, word): 
        self.word = word #The word represnted by the node
        self.neighbors = [] #Initializing an empty list of neighbors
        self.visited = False #For marking visited nodes during BFS Search
        self.parent = None #Tracking relationships during BFS search
   
class Network:
    def __init__(self, words_list): #List of all words
        self.words_list = words_list
        self.nodes_dict = {word: Node(word) for word in words_list} #Making a dictonary where each object is itself
        self.make_neighbors_network() #Creating the network

    def add_graph(self, first_word, second_word):
        #Creating nodes and adding as neighbors
        first_node = self.nodes_dict[first_word]
        second_node = self.nodes_dict[second_word]
        first_node.neighbors.append(second_node)
        second_node.neighbors.append(first_node)

    def make_neighbors_network(self):
        #Creating a network of all words that differ by only one letter
        for word in self.words_list:
            word_length = len(word)
            for i in range(word_length):
                for char in 'abcdefghijklmnopqrstuvwxyz':
                    if char != word[i]:
                        new_word = word[:i] + char + word[i + 1:]
                        if new_word in self.nodes_dict:
                            self.add_graph(word, new_word)

def word_ladder(start_word, end_word, network):
    if start_word == end_word:
        return [start_word] #Check to see if the two words are different

    #Look for the corresponding object of the node in the dicitionary
    start_node = network.nodes_dict.get(start_word)
    if start_node is None:
        return "No path found" #Cases where no path is available

    #Queueing and visitng the starting node 
    queue = [start_node] 
    start_node.visited = True

    while queue:
    #Taking first word from the queue
        current_node = queue.pop(0)
        #Checking if target word is found
        if current_node.word == end_word:
            path = [] #Initialzing a list to track path
            #Tracing backthe path and adding to list
            while current_node:
                path.append(current_node.word)
                current_node = current_node.parent
            #Reversing path since it was traced backwards
            return path[::-1]

        for neighbor in current_node.neighbors:
            #Checking each neighbors
            if not neighbor.visited:
                neighbor.visited = True  #Marking checked
                neighbor.parent = current_node
                queue.append(neighbor)  #Queueing to check
#YuDong's part
#Creating a list of all words that differ by only one letter from the target word
def find_neighbors(word, words_set):
    neighbors = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != word[i]:
                new_word = word[:i] + char + word[i+1:]
                if new_word in words_set:
                    neighbors.append(new_word)
    return neighbors

#Taking input and converting to lowercase
start_word = input("Enter the start word: ").lower()
end_word = input("Enter the end word: ").lower()

if len(start_word) != len(end_word):
    print("Error: Start and end words must be of the same length.") #Ensuring both words are of the same length
else:
    words_list = []
    with open('words_alpha.txt', 'r') as file:
        for word in file:
            word = word.strip().lower()
            if len(word) == len(start_word):
                words_list.append(word)

    network = Network(words_list)

    #Measuring runtime
    start_time = time.time()
    ladder = word_ladder(start_word, end_word, network)
    end_time = time.time()

    print("Word ladder from '{}' to '{}':".format(start_word, end_word), ladder)
    print("Runtime of the word_ladder function: {:.6f} seconds".format(end_time - start_time))

