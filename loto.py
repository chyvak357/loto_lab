#!/usr/bin/python3
from random import randint


def generate_unique_numbers(count, minbound, maxbound):
    if count > maxbound - minbound + 1:
        raise ValueError('Incorrect input parameters')
    ret = []
    while len(ret) < count:
        new = randint(minbound, maxbound)
        if new not in ret:
            ret.append(new)
    return ret


class Keg:
    __num = None

    def __init__(self):
        self.__num = randint(1, 90)

    @property
    def num(self):
        return self.__num

    def __str__(self):
        return str(self.__num)


class Card:
    __rows = 3
    __cols = 9
    __nums_in_row = 5
    __data = None
    __emptynum = 0
    __crossednum = -1

    def __init__(self):
        """
        Генерит 15 значений из диапазона.
        На каждую строку берём по 5 чисел и потом рандомно вставляем в неё пробелы
        """
        uniques_count = self.__nums_in_row * self.__rows
        uniques = generate_unique_numbers(uniques_count, 1, 90)
        self.__data = []
        for i in range(0, self.__rows):
            tmp = sorted(uniques[self.__nums_in_row * i: self.__nums_in_row * (i + 1)])
            empty_nums_count = self.__cols - self.__nums_in_row
            for j in range(0, empty_nums_count):
                index = randint(0, len(tmp))
                tmp.insert(index, self.__emptynum)
            self.__data += tmp

    def __contains__(self, item):
        return item in self.__data

    def cross_num(self, num):
        """Зачеркивание числа. Замена его на -1"""
        for index, item in enumerate(self.__data):
            if item == num:
                self.__data[index] = self.__crossednum
                return
        raise ValueError(f'Number not in card: {num}')

    def closed(self) -> bool:
        """
        Проверка на заполненность карточки.
        set оставит только уникальные значения, а так как все числа заменяются на -1, то в конце должны остаться 0 и -1
        """
        return set(self.__data) == {self.__emptynum, self.__crossednum}

    @property
    def data(self):
        return self.__data


class Game:
    __usercard = None
    __compcard = None
    __numkegs = 90
    __kegs = []
    __gameover = False

    def __init__(self):
        self.__usercard = Card()
        self.__compcard = Card()
        self.__kegs = generate_unique_numbers(self.__numkegs, 1, 90)
        self.__current_keg = 1000

    @property
    def usercard(self):
        return self.__usercard

    @property
    def compcard(self):
        return self.__compcard

    def generate_keg(self):
        self.__current_keg = self.__kegs.pop()
        return self.__current_keg

    @property
    def left_kegs(self):
        return len(self.__kegs)

    def check_step(self, user_answer):
        keg = self.__current_keg
        if user_answer == 1 and not keg in self.__usercard or user_answer != 1 and keg in self.__usercard:
            return 2

        if keg in self.__usercard:
            self.__usercard.cross_num(keg)
            if self.__usercard.closed():
                return 1
        if keg in self.__compcard:
            self.__compcard.cross_num(keg)
            if self.__compcard.closed():
                return 2
        return 0
