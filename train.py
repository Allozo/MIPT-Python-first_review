import pymorphy2
import re

text = "wp.txt"
diction = dict()                                    # тут будут храниться связки слов
with open(text, "r", encoding="UTF-8") as file:
    for line in file:
        if line != '\n':
            line = line.lower()                     # приводим к нижнему регистру
            line = re.sub(r'[^\w\s]', ' ', line)    # избавляемся от пробелов/ знаков препинания
            line = line.split()                     # получили простой лист слов
            size = len(line)
            for i in range(size):
                if i != size - 1:
                    word = line[i]
                    next_word = line[i + 1]
                    diction.setdefault(word, list())     # можно написать if word in diction: -//-?
                    diction[word].append(next_word)
print(diction)