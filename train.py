import re
import os
import argparse
import pickle
import collections


def process_pair_words(lines, dict_dict, is_lowering):
    # приводим к нижнему регистру, если надо
    if is_lowering == 1:
        lines = lines.lower()

    # избавляемся от пробелов и знаков препинания
    lines = re.sub(r'[^\w\s]', ' ', lines)

    # получим список слов
    lines = lines.split()

    for t in range(len(lines) - 1):
        word = lines[t]  # первое слово
        next_word = lines[t + 1]  # второе слово
        dict_dict[word][next_word] += 1

    return dict_dict


def fill_dict_dict_from_file(file, can_lowering, dict_dict):
    for line in file:
        if line != '\n':
            dict_dict = process_pair_words(line,
                                           dict_dict,
                                           can_lowering)


def train(args):
    # нужно ли приводить к нижнему регистру
    can_lowering = args.lc

    # указали путь к документам
    directory = args.input

    # указали путь к модели
    model_file_name = args.model

    assert args.model, 'Ошибка!!! Вы не указали путь, куда сохранить модель.'

    # тут будут храниться связки слов
    dict_dict = collections.defaultdict(collections.Counter)

    if directory != " ":
        # получим все файлы в данной директории
        files = os.listdir(directory)

        # получим все файлы *.txt
        file_txt = list(filter(lambda x: x.endswith('.txt'), files))

        # обходим все файлы в папке
        for file_name in file_txt:
            # путь до папки
            path = os.path.join(directory + "/" + file_name)

            with open(path, "r", encoding="UTF-8") as file:
                fill_dict_dict_from_file(file, can_lowering, dict_dict)

        # сохраним модель
        with open(model_file_name, "wb") as f:
            pickle.dump(dict_dict, f)
    else:
        while True:
            try:
                line = input()
                dict_dict = process_pair_words(line, dict_dict, can_lowering)
            except EOFError:
                with open(model_file_name, "wb") as f:
                    pickle.dump(dict_dict, f)
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--lc", action="store_true", default=False,
                       help="Приводить тексты к lowercase.")
    parser.add_argument("--input", "--input-dir", type=str, default=None,
                        help="Путь до папки с документами.")
    parser.add_argument("--model", type=str,
                        help="Путь до файла, куда сохранится модель.")
    arg = parser.parse_args()
    train(arg)
