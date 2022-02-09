from typing_core import Window
from tkinter import simpledialog
import random
import re
import os


main_window = Window(width="500", height="800", start_pos_x="500", start_pos_y="300", bg='#000a17')
with open(os.path.join("meta", "words.txt"), "r") as f:
    num_words = 2000
    while num_words > 1000:
        num_words = simpledialog.askinteger('Num', 'How many words do you want to type? (int < 1000)',
                                            parent=main_window)
    lines = f.readlines()
    main_window.words_list = random.sample(lines, num_words)
    del lines
    main_window.reg = re.compile('[\n]')
    output_list = []
    for i, item in enumerate(main_window.words_list):
        if i not in range(0, num_words + 1, 7):
            output_list.append(main_window.reg.sub('', item))
        elif i == 0:
            output_list.append(main_window.reg.sub('', item))
        else:
            output_list.append(item)
    main_window.words_string = ' '.join(output_list)
    main_window.words_string_list = list(main_window.words_string)
    main_window.lift()

main_window.add_text(main_window.words_string)


# type_pos[0] is the character's index in the text box line, type_pos[2] is the line's index in the text box
# type_pos[2] is the character's index in the words_string_list
type_pos = [0, 1, 0]


def check_user_input(event):
    main_window.run_timer()
    # \x08 = backspace
    if event.char.lower() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\x08', ' ']:
        return

    if event.char == '\x08':
        if not (main_window.words_string_list[type_pos[2]-1] == ' ' and main_window.words_string_list[type_pos[2]-2]
                == '\n'):
            try:
                main_window.un_mark(f"{type_pos[1]}.{type_pos[0]-1}", f"{type_pos[1]}.{type_pos[0]}")
            except IndexError:
                pass
            else:
                type_pos[0] -= 1
                type_pos[2] -= 1

    else:
        if main_window.words_string_list[type_pos[2]] == '\n':
            type_pos[1] += 1
            type_pos[0] = 0
            type_pos[2] += 1
            main_window.see_text(f"{type_pos[1]}.{type_pos[0]}")
            main_window.clear_input()

        if event.char == main_window.words_string_list[type_pos[2]].lower():
            main_window.mark("Correct", f"{type_pos[1]}.{type_pos[0]}", f"{type_pos[1]}.{type_pos[0]+1}")
            type_pos[0] += 1
            type_pos[2] += 1

        else:
            main_window.mark("Wrong", f"{type_pos[1]}.{type_pos[0]}", f"{type_pos[1]}.{type_pos[0]+1}")
            type_pos[0] += 1
            type_pos[2] += 1

    if type_pos[2] > 5:
        main_window.place_calculate_btn()
    else:
        main_window.forget_calculate_btn()

    try:
        main_window.words_string_list[type_pos[2]]
    except IndexError:
        main_window.return_result()
        return


main_window.bind_user_input(check_user_input)
main_window.mainloop()
