import re

text = "wp.txt"
diction = dict()                            # тут будут храниться связки слов
with open(text, "r", encoding="UTF-8") as file:
    for line in file:
        if line != '\n':
            line = line.lower()  # приводим к нижнему регистру
            line = re.sub(r'[^\w\s]', ' ', line)  # избавляемся от пробелов/ знаков препинания
            line = line.split()  # получили простой лист слов
            size = len(line)
            for i in range(size):
                if i != size - 1:
                    word = line[i]
                    next_word = line[i + 1]
                    if word in diction:
                        if next_word in diction[word]:
                            diction[word][next_word] = diction[word][next_word] + 1  # +1 к частоте
                        else:
                            diction[word].setdefault(next_word, 1)
                    else:
                        diction.setdefault(word, {next_word: 1})  # просто добавили слово

with open("model.txt", "w", encoding="UTF-8") as f:
    for i in diction:
        for j in diction[i]:
            f.write(i + " " + j + " " + str(diction[i][j]) + '\n')
