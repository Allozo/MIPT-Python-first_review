import re
import os


def processing(lines, dictions, lowers):
    if lowers == 1:
        lines = lines.lower()  # приводим к нижнему регистру
    lines = re.sub(r'[^\w\s]', ' ', lines)  # избавляемся от пробелов/ знаков препинания
    lines = lines.split()  # получили простой лист слов
    sizes = len(lines)
    for i in range(sizes):  # простой счетчик
        if i != sizes - 1:  # если не последние слово в предложении
            words = lines[i]  # первое слово
            next_words = lines[i + 1]  # второе слово
            if words in dictions:
                if next_words in dictions[words]:
                    diction[words][next_words] += 1  # +1 к частоте
                else:
                    diction[words].setdefault(next_words, 1)
            else:
                diction.setdefault(words, {next_words: 1})  # просто добавили слово
    return dictions


print()
print("Введите --help для получения списка команд")
command = input()
if command == "--help":
    print("--lc - необязательный аргумент. Приводить тексты к lowercase. "
          "Для использования введите раньше, чем другие команды.")
    print("--input-dir - путь к директории, в которой лежит коллекция документов. "
          "Если не задан, то вводится текст из потока. Чтобы его остановить введите '~stop' ")
    print("--model - путь к файлу, в который сохраняется модель.")
    command = input()

lower = 0
if command == "--lc":
    lower = 1
    command = input()

flag = 0
if "--input-dir" in command:
    flag = 1
    if command[12] == '.':
        directory = os.getcwd()
        files = os.listdir(directory)
        txt = list(filter(lambda x: x.endswith('.txt'), files))
        model = command[23:]  # путь куда сохранять модель
    else:
        i = 12
        while command[i] != " ":
            i += 1
        directory = command[12:i]
        files = os.listdir(directory)
        txt = list(filter(lambda x: x.endswith('.txt'), files))
        model = command[i + 9:]
else:
    model = command[8:]


diction = dict()  # тут будут храниться связки слов
if flag == 1:
    for m in range(len(txt)):  # обходим все файлы в папке
        path = directory + "/" + txt[m]  # путь до папки
        with open(path, "r", encoding="UTF-8") as file:
            for line in file:
                if line != '\n':
                    diction = processing(line, diction, lower)
else:
    while True:
        line = input()
        if line == "~stop":
            break
        elif line != '\n':
            diction = processing(line, diction, lower)

with open("model.txt", "w", encoding="UTF-8") as f:
    for i in diction:
        for j in diction[i]:
            if diction[i][j] > 1:  # ограничение
                f.write(i + " " + j + " " + str(diction[i][j]) + '\n')
