import re
import os
import argparse


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


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--lc", action="store_true", help="Приводить тексты к lowercase.")
parser.add_argument("--input", "--input-dir", type=str, default="", help="путь до папки с документами")
parser.add_argument("--model", type=str, help="путь до файла, куда сохранится модель")
args = parser.parse_args()
lower = 0
if args.lc:                                         # если нужно приводить к нижнему регистру
    lower = 1
directory = args.input                              # указали путь к документам
if directory == ".":                                # если пользователь написал "--input-dir ."
    directory = os.getcwd()
flag = 1                                            # пометка, что данные будут считываться из потока
txt = []                                            # тут будут лежать названия документов
if directory == "":
    flag = 0
else:
    files = os.listdir(directory)
    txt = list(filter(lambda x: x.endswith('.txt'), files))
model = args.model                                  # указали путь к модели

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
