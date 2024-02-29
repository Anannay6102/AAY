with open('C:/Users/le/PycharmProjects/pythonProject/workshhet16/words_alpha.txt', 'r') as file:
    word_set = [word.strip() for word in file]

def find_neighbors_simple(word, words_set):
    neighbors = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            if char != word[i]:
                new_word = word[:i] + char + word[i+1:]
                if new_word in words_set:
                    neighbors.append(new_word)
    return neighbors

print(find_neighbors_simple('cat', word_set))




