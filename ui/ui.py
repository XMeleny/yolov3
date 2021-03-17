import tkinter as tk

from ui_helper import get_max_window, get_choose_file_button

if __name__ == '__main__':
    window = get_max_window()

    label = tk.Label(window)
    btn_choose_file = get_choose_file_button(window, "choose file", label)

    btn_choose_file.pack()
    label.pack()

    window.mainloop()
