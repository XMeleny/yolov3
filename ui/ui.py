import tkinter as tk

from ui_helper import get_max_window, get_choose_file_button

if __name__ == '__main__':
    window = get_max_window()

    str_var = tk.StringVar()
    label = tk.Label(window, textvariable=str_var)

    btn_choose_file = get_choose_file_button(window, "choose file", string_var=str_var)

    btn_choose_file.pack()
    label.pack()

    window.mainloop()
