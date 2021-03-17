from PIL import ImageTk, Image
import cv2
import tkinter as tk
import function


def get_max_window():
    window = tk.Tk()
    window.title("my window")
    w, h = window.maxsize()
    print(w, h)
    window.geometry("{}x{}".format(w, h))
    return window


def show_img(cv_img, canvas):
    global tk_img  # 必须保持对图片的引用
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)))
    canvas.create_image(0, 0, image=tk_img)
    canvas.pack()


def get_choose_file_button(window, btn_text, string_var=None):
    button = tk.Button(window, text=btn_text, command=lambda: function.choose_file(string_var))  # 可以用lambda把var传进去
    return button


if __name__ == '__main__':
    pass
