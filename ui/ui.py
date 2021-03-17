import tkinter as tk
import ui_helper

if __name__ == '__main__':
    window = ui_helper.get_max_window()

    str_var = tk.StringVar()
    label = tk.Label(window, textvariable=str_var)

    btn_choose_file = ui_helper.get_choose_file_button(window, "choose file", string_var=str_var)

    btn_choose_file.pack()
    label.pack()

    window.mainloop()
