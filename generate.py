import numpy as np

text = "model.txt"
diction = dict()
with open(text, "r", encoding="UTF-8") as file:
    for line in file:
        line = line.split()
        word = line[0]
        next_word = line[1]
        frequency = int(line[2])
        if word in diction:
                diction[word].setdefault(next_word, frequency)
        else:
            diction.setdefault(word, {next_word: frequency})
# загрузили наш словарь


print("Введите начальное слово")
word = input()
print("Введите длину последовательности")
size = int(input())
new_text = [word]
for i in range(size - 1):
    list_next_words = []
    frequency = []
    number = 0
    for two_word in diction[new_text[i]]:      # пробегаемся по всем вторым словам
        number += diction[new_text[i]][two_word]
        list_next_words.append(two_word)
    for j in range(len(list_next_words)):
        frequency.append(diction[new_text[i]][list_next_words[j]] / number)
    np.random.choice(list_next_words, len(list_next_words), frequency)
    selected_word = list_next_words[0]
    new_text.append(selected_word)
for words in new_text:
    print(words, end=" ")
