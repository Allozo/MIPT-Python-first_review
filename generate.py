import numpy as np
import random
import argparse

parser = argparse.ArgumentParser(description="создание цепочки")
parser.add_argument("--model", type=str, help="путь до модели")
parser.add_argument("--seed", type=str, default="", help="Начальное слово. Опционально")
parser.add_argument("--length", type=int, help="Длина модели")
args = parser.parse_args()

model = args.model                                  # указали путь к модели
seed = args.seed
length = args.length

# загрузка словаря
diction = dict()
first_word = []
with open(model, "r", encoding="UTF-8") as file:
    for line in file:
        line = line.split()
        word = line[0]
        next_word = line[1]
        frequency = int(line[2])
        if word not in first_word:
            first_word.append(word)
        if word in diction:
            diction[word].setdefault(next_word, frequency)
        else:
            diction.setdefault(word, {next_word: frequency})

size_first_word = len(first_word)
if seed == "":
    rand = random.randint(0, size_first_word)
    seed = first_word[rand]

# построение цепочки
new_text = [seed]                                       # тут будут слова для последовательности
for i in range(length - 1):
    list_next_words = []                                # тут будут слова, которые могут идти после
    if new_text[i] not in diction:                      # если последнего слова нет в словаре, то берем случайное
        rand = random.randint(0, size_first_word)
        new_text.append(first_word[rand])
        continue
    frequency = []                                      # частота соответствующая слову в list_next_words
    number = 0                                          # сумма частот в list_next_words
    for two_word in diction[new_text[i]]:               # пробегаемся по всем вторым словам
        number += diction[new_text[i]][two_word]        # считаем общую частоту
        list_next_words.append(two_word)                # добавили из словаря возможное следующее слово
    for j in range(len(list_next_words)):               # расставим частоту
        frequency.append(diction[new_text[i]][list_next_words[j]] / number)     # расставили частоту
    np.random.choice(list_next_words, len(list_next_words), frequency)          # рандом. перемешивание
    selected_word = list_next_words[0]                                          # выбрали слово
    new_text.append(selected_word)                                              # добавили его
for words in new_text:
    print(words, end=" ")
print()
