import tkinter as tk


def get_max_window():
    res_window = tk.Tk()
    res_window.title("my window")

    w, h = res_window.maxsize()
    res_window.geometry("{}x{}".format(w, h))

    return res_window


def print_winfo(widget):
    print(f'widget.winfo_width = {widget.winfo_width()}')
    print(f'widget.winfo_reqwidth = {widget.winfo_reqwidth()}')
    print(f'widget.winfo_vrootwidth = {widget.winfo_vrootwidth()}')
    print(f'widget.winfo_screenmmwidth = {widget.winfo_screenmmwidth()}')
    print(f'widget.winfo_screenwidth = {widget.winfo_screenwidth()}')
