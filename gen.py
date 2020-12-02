"""Генератор кода для размещения сетки карточки"""

def wr_dict_data(data):
    big_string = '{'
    for key, val in data.items():
        big_string += f'{key}: {val}, '
    big_string = big_string[:-2] + '}'
    return big_string


if __name__ == '__main__':
    with open('card_grid.py', 'w') as file:
        file.write('''from tkinter.ttk import * \nfrom tkinter import * \n\n\ndef user_card_draw(rootFrame):\n''')
        c = 0
        for i in range(3):
            for j in range(9):
                template = '    label_{0} = Label(rootFrame, text="{1}", fg="#eee", bg="#333")\n' \
                           '    label_{0}.grid(row={2}, column={3}, ipadx=4, ipady=4, sticky=NSEW)\n'
                file.write(template.format(f'{c}', f'{i}{j}', i, j))
                c += 1

        data = {int(f'{i}'): f'label_{i}' for i in range(27)}
        file.write('    data = {}\n'.format(wr_dict_data(data)))
        file.write('    return data')
