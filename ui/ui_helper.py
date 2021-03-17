from PIL import ImageTk, Image
import cv2
import tkinter as tk
from tkinter import filedialog
import os


def get_max_window():
    res_window = tk.Tk()
    res_window.title("my window")
    w, h = res_window.maxsize()
    # print(w, h)
    res_window.geometry("{}x{}".format(w, h))
    return res_window


def show_img(cv_img, canvas):
    global tk_img  # 必须保持对图片的引用
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)))
    canvas.create_image(0, 0, image=tk_img)
    canvas.pack()


def get_choose_file_button(window, btn_text, label):
    button = tk.Button(window, text=btn_text, command=lambda: choose_file(label))
    return button


def rotate_video():
    # TODO:
    pass


def start_detect():
    pass


def choose_file(label=None):
    file_path = filedialog.askopenfilename()

    if label is not None:
        label['text'] = file_path

    return file_path


def split_url(url):
    (_dir, file) = os.path.split(url)
    temp = file.split('.')
    filename = temp[0]
    ext = temp[1]
    result = {'dir': _dir, 'filename': filename, 'ext': ext}
    print(result)
    return result


if __name__ == '__main__':
    window = get_max_window()

    label = tk.Label(window)
    label.pack()

    label['text'] = "test text2"
    print(label['text'])

    window.mainloop()
