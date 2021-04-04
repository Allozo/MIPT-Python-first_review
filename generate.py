import numpy as np
import random
import argparse
import pickle


def building_chain_words(text, length, possible_first_words, diction):
    for i in range(length - 1):
        # тут будут слова, которые могут идти после
        list_next_words = []

        if text[i] not in diction:
            rand = random.randint(0, len(possible_first_words))
            text.append(possible_first_words[rand])
            continue

        # частота соответствующая слову в list_next_words
        frequency = []

        # сумма частот в list_next_words
        number = 0

        # пробегаемся по всем вторым словам
        for second_word in diction[text[i]]:
            # считаем общую частоту
            number += diction[text[i]][second_word]
            list_next_words.append(second_word)

        for j in list_next_words:  # расставим частоту
            frequency.append(diction[text[i]][j] / number)

        # получаем следующее слово
        selected_word = np.random.choice(list_next_words, p=frequency)
        text.append(selected_word)


def print_chain_words(text_path, text, is_file):
    if is_file:
        with open(text_path, "w", encoding="UTF-8") as file:
            for word_in_text in text:
                file.write(word_in_text + " ")
    else:
        for word_in_text in text:
            print(word_in_text, end=" ")
        print()


def generate(args):
    # указали путь к модели
    model_file_name = args.model

    # указали первое слово цепочки
    seed = args.seed

    # указали длину цепочки
    length = args.length

    # загрузка словаря
    with open(model_file_name, "rb") as file:
        diction = pickle.load(file)

    # создаем список первых слов
    possible_first_words = []
    for key in diction:
        possible_first_words.append(key)

    # если слова нет, то получаем случайное из всех первых
    if seed == "":
        rand = random.randint(0, len(possible_first_words))
        seed = possible_first_words[rand]

    # флаг, который укажет, будем ли мы сохранять цепочку слов
    if args.output == "":
        is_file = False
        text_path = ""
    else:
        is_file = True
        text_path = args.output

    # тут будут слова для последовательности
    text = [seed]
    building_chain_words(text, length, possible_first_words, diction)

    # вывод/ сохранение цепочки
    print_chain_words(text_path, text, is_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="создание цепочки")
    parser.add_argument("--model", type=str, help="путь до модели")
    parser.add_argument("--seed", type=str, default="",
                        help="Начальное слово. Опционально")
    parser.add_argument("--length", type=int, help="Длина модели")
    parser.add_argument("--output", type=str, default="",
                        help="Путь, куда сохранить цепочку слов")
    arg = parser.parse_args()
    generate(arg)
