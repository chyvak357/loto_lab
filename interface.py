#!/usr/bin/python3
"""
Графическое представление для игры Лото
"""
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox as mb
from card_grid import user_card_draw
from loto import *

"""Цвета для основных элементов"""
TOP_BG = '#8c8c8c'
TOP_BG_TEXT_bg = '#8c8c8c'  # фон текстовых полей
TOP_BG_TEXT_fg = '#292929'  # свет текста

TOP_BG_NUM_bg = '#333'
TOP_BG_NUM_fg = '#c2c2c2'

MID_BG = '#6b6b6b'  # цвет средней части
FOOTER_BG = '#8c8c8c'  # цвет нижней части

BTN_BG_bg = '#8fbaba'  # цвет кнопки
BTN_BG_active = '#b4e0e0'  # цвет нажатой кнопки

class MainWindow(Frame):
    """  Главное окно """

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.game = Game()
        self.player_card_dict = None
        self.machine_card_dict = None


        self.keg_Text = StringVar()
        self.keg_left_Text = StringVar()
        self.keg_Text.set('--')
        self.keg_left_Text.set('90')
        self.parent = parent
        self.initUI()

    def initUI(self):
        """Отрисовка интерфейса"""

        self.parent.title('Лото')
        self.pack(fill=BOTH, expand=1)

        topFrame = Frame(self)
        topFrame.pack(fill=BOTH, expand=1)

        '''Блок с информацией про бочонок'''
        # topKegFrame = LabelFrame(topFrame, text='бочонок')
        topKegFrame = Frame(topFrame)
        topKegFrame.pack(fill=X, expand=0)

        '''Левая и правая сторона в верхнем блоке про бочонок'''
        kegFrame_left = Frame(topKegFrame, bg=TOP_BG)
        kegFrame_right = Frame(topKegFrame, bg=TOP_BG)
        kegFrame_left.pack(fill=BOTH, expand=1, side=LEFT)
        kegFrame_right.pack(fill=BOTH, expand=1, side=LEFT)

        '''Текстовые блоки в блоке про бочонок'''
        # TODO разобраться с размерами и цветом фона
        keg_text1Frame = Label(kegFrame_left, text='Новый бочонок:', justify=LEFT, font="Arial 14", width=5, height=2, bg=TOP_BG_TEXT_bg, fg=TOP_BG_TEXT_fg)
        keg_valFrame = Label(kegFrame_left, textvariable=self.keg_Text, fg=TOP_BG_NUM_fg, bg=TOP_BG_NUM_bg, font="Arial 14", height=2)
        keg_text2Frame = Label(kegFrame_right, text='Осталось:', justify=RIGHT, font="Arial 14", width=5, height=2, bg=TOP_BG_TEXT_bg, fg=TOP_BG_TEXT_fg)
        keg_lost_valFrame = Label(kegFrame_right, textvariable=self.keg_left_Text, fg=TOP_BG_NUM_fg, bg=TOP_BG_NUM_bg, font="Arial 14", height=2)

        keg_text1Frame.pack(expand=1, fill=BOTH, side=LEFT, padx=10, pady=2.5)
        keg_valFrame.pack(expand=1, fill=BOTH, side=LEFT, padx=10, pady=2.5)
        keg_text2Frame.pack(expand=1, fill=BOTH, side=LEFT, padx=10, pady=2.5)
        keg_lost_valFrame.pack(expand=1, fill=BOTH, side=LEFT, padx=10, pady=2.5)

        '''Блок с игровыми карточками'''
        topCardsFrame = Frame(topFrame, bg=MID_BG)
        playerFrame = LabelFrame(topCardsFrame, text='Карта игрока', bg=MID_BG)
        machineFrame = LabelFrame(topCardsFrame, text='Карта компьютера', bg=MID_BG)

        topCardsFrame.pack(fill=BOTH, expand=1)
        playerFrame.pack(fill=NONE, expand=1, side=LEFT)
        machineFrame.pack(fill=NONE, expand=1, side=LEFT)

        # Отрисовка карточек из сгенерируемого кода. Потом через эти словари можно обращаться к полям карточек
        self.player_card_dict = user_card_draw(playerFrame)
        self.machine_card_dict = user_card_draw(machineFrame)
        self.update_cards()
        
        '''Блок с кнопками управления. Сначала будет "начать игру", затем появятся две кнопки'''
        topBtnsFrame = Frame(topFrame, bg=FOOTER_BG)
        # topBtnsFrame = LabelFrame(topFrame, text='Управление')
        self.btn_start = Button(topBtnsFrame, text='Начать игру', activebackground=BTN_BG_active, bg=BTN_BG_bg, command=self.start_game, font="Arial 13", height=2)
        self.btn_write = Button(topBtnsFrame, text='Заполнить', activebackground=BTN_BG_active, bg=BTN_BG_bg, command=lambda act=1: self.check_score(self.game.check_step(act)), font="Arial 13", height=2)
        self.btn_next = Button(topBtnsFrame, text='Дальше', activebackground=BTN_BG_active, bg=BTN_BG_bg, command=lambda act=0: self.check_score(self.game.check_step(act)), font="Arial 13", height=2)


        topBtnsFrame.pack(fill=BOTH, expand=0)
        self.btn_start.pack(expand=1, fill=BOTH, side=LEFT, padx=20, pady=5)

    def hide_control(self):
        """Скрвыет кнопки управления в конце игры, что бы нельзя было продолжить"""
        # Просто закоментируй что бы читерить
        self.btn_write.pack_forget()
        self.btn_next.pack_forget()
        self.btn_start.pack(expand=1, fill=BOTH, side=LEFT, padx=20, pady=5)
        pass

    def check_score(self, score):
        if score == 1:
            self.hide_control()
            mb.showinfo('Победа', 'Вы победили!')
        if score == 2:
            self.hide_control()
            mb.showinfo('Неудача', 'Вы проиграли!')
        else:
            self.next_round()

    def update_cards(self):
        """Обновляет карточки с данными игры"""
        card_data = (self.game.usercard.data, self.game.compcard.data)
        for i in range(len(card_data[0])):
            self.player_card_dict[i].config(text=self.get_field_text(card_data[0][i]))
            self.machine_card_dict[i].config(text=self.get_field_text(card_data[1][i]))

    @staticmethod
    def get_field_text(value):
        if value == -1:
            return '--'
        if value == 0:
            return ' '
        return value

    def next_round(self):
        """Генериует след бочонок и обновляет карточки"""
        self.update_cards()
        tmp_keg = self.game.generate_keg()
        self.keg_Text.set(str(tmp_keg))
        self.keg_left_Text.set(str(self.game.left_kegs))


    def start_game(self):
        """Начало игры, генерирует первый бочонок и показывает кнопки упрвления"""
        self.btn_start.pack_forget()
        self.btn_write.pack(expand=1, fill=BOTH, side=LEFT, padx=10, pady=5)
        self.btn_next.pack(expand=1, fill=BOTH, side=LEFT, padx=10, pady=5)

        self.game = Game()
        self.update_cards()
        self.keg_Text.set(str(self.game.generate_keg()))
        self.keg_left_Text.set(str(self.game.left_kegs))


def main():
    root = Tk()
    ex = MainWindow(root)
    root.geometry('700x300+300+300')
    root.mainloop()


if __name__ == '__main__':
    main()