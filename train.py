import re
import os

print()
print("Введите --help для получения списка команд")
command = input()
lower = 0
if command == "--help":
    print("--lc - необязательный аргумент. Приводить тексты к lowercase. "
          "Для использования введите раньше, чем другие команды.")
    print("--input-dir - путь к директории, в которой лежит коллекция документов.")
    print("--model - путь к файлу, в который сохраняется модель.")
    command = input()
if command == "--lc":
    lower = 1
    command = input()
if command[12] == '.':
    directory = os.getcwd()
    files = os.listdir(directory)
    txt = list(filter(lambda x: x.endswith('.txt'), files))
    model = command[23:]                                      # путь куда сохранять модель
else:
    i = 12
    while command[i] != " ":
        i += 1
    directory = command[12:i]
    files = os.listdir(directory)
    txt = list(filter(lambda x: x.endswith('.txt'), files))
    model = command[i+9:]

diction = dict()                                        # тут будут храниться связки слов
for m in range(len(txt)):                               # обходим все файлы в папке
    path = directory + "/" + txt[m]                     # путь до папки
    with open(path, "r", encoding="UTF-8") as file:
        for line in file:
            if line != '\n':
                if lower == 1:
                    line = line.lower()                 # приводим к нижнему регистру
                line = re.sub(r'[^\w\s]', ' ', line)    # избавляемся от пробелов/ знаков препинания
                line = line.split()                     # получили простой лист слов
                size = len(line)
                for i in range(size):                   # простой счетчик
                    if i != size - 1:                   # если не последние слово в предложении
                        word = line[i]                  # первое слово
                        next_word = line[i + 1]         # второе слово
                        if word in diction:
                            if next_word in diction[word]:
                                diction[word][next_word] += 1  # +1 к частоте
                            else:
                                diction[word].setdefault(next_word, 1)
                        else:
                            diction.setdefault(word, {next_word: 1})  # просто добавили слово

with open("model.txt", "w", encoding="UTF-8") as f:
    for i in diction:
        for j in diction[i]:
            if diction[i][j] > 1:                         # ограничение
                f.write(i + " " + j + " " + str(diction[i][j]) + '\n')
