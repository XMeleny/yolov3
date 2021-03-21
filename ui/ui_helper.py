from PIL import ImageTk, Image
import cv2
import tkinter as tk
from tkinter import filedialog
import os


def get_max_window():
    res_window = tk.Tk()
    res_window.title("my window")
    w, h = res_window.maxsize()
    res_window.geometry("{}x{}".format(w, h))
    return res_window


def show_image_auto_resize(canvas, cv_image):
    # 获取canvas和图片的尺寸
    canvas_width = canvas.winfo_reqwidth()
    canvas_height = canvas.winfo_reqheight()

    shape = cv_image.shape
    pic_width = shape[1]
    pic_height = shape[0]

    canvas_ratio = canvas_width / canvas_height
    pic_ratio = pic_width / pic_height

    # 尺寸自适应
    if pic_ratio > canvas_ratio:
        w = canvas_width
        h = canvas_width / pic_ratio
    elif pic_ratio < canvas_ratio:
        h = canvas_height
        w = canvas_height * pic_ratio
    else:
        w = canvas_width
        h = canvas_height

    result_cv_image = cv2.resize(cv_image, (int(w), int(h)))

    # canvas显示opencv格式的图片
    global tk_img  # 必须保持对图片的引用
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(result_cv_image, cv2.COLOR_BGR2RGB)))

    center_x = int(canvas_width / 2)
    center_y = int(canvas_height / 2)
    canvas.create_image(center_x, center_y, image=tk_img)


def get_choose_file_button(window, btn_text, label):
    button = tk.Button(window, text=btn_text, command=lambda: choose_file(label))
    return button


def rotate_video():
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


def init_window():
    window = get_max_window()
    # window.geometry('500x300')

    canvas = tk.Canvas(window, bg='green', width=500, height=400)
    canvas.pack()

    img = cv2.imread(r"C:\Users\Meleny\Pictures\wallpaper\222_small.jpg")

    show_image_auto_resize(canvas, img)
    window.mainloop()


if __name__ == '__main__':
    init_window()
