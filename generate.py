import numpy as np
import random

print()
print("Введите --help для получения списка команд")

command = input()

if command == "--help":
    print("--model - путь к файлу, из которого загружается модель.")
    print("--seed - Начальное слово. Если не указано, выбирается"
          "случайное слово из всех слов.")
    print("--length - длина генерируемой последовательности.")
    print("Порядок ввода аргументов: --model <path> --length <number> --seed <word>")
    print("Пример:")
    print("--model /home/.../model.txt --length 10 --seed exemple")
    command = input()

# обработка команды
i = 8                       # обходим с его помощью строку с командой
# путь до модели
while command[i] != " ":
    i += 1
model = command[8:i]
i += 10
k = i
# получаем длину
while command[i] != " ":
    i += 1
length = int(command[k:i])
# получаем начальное слово
seed = ""
if "--seed" in command:
    i += 8
    seed = command[i:].split()
    seed = seed[0]
# команду обработали

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
