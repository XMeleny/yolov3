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
    res_window.update()
    # res_window.configure(width=w, height=h)

    # print(w, h)
    # print(res_window.winfo_width())
    # print(res_window.winfo_reqwidth())
    # print(res_window.winfo_vrootwidth())
    # print(res_window.winfo_screenmmwidth())
    # print(res_window.winfo_screenwidth())
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


def get_choose_file_button_and_label(window):
    label = tk.Label(window)
    button = tk.Button(window, command=lambda: choose_file(label))
    return button, label


def rotate_video():
    pass


def start_detect():
    pass


def choose_file(label=None):
    # TODO: 文件类型限制。比如视频应该为mp4等，权重文件为pt
    file_path = filedialog.askopenfilename()

    if label is not None:
        label['text'] = file_path

    return file_path


def choose_classes():
    pass


def split_url(url):
    (_dir, file) = os.path.split(url)
    temp = file.split('.')
    filename = temp[0]
    ext = temp[1]
    result = {'dir': _dir, 'filename': filename, 'ext': ext}
    print(result)
    return result


def log():
    """保存log文件"""
    pass


def init_window():
    # TODO: 用变量把text们都存起来
    window = get_max_window()

    choose_file_weight = 1
    file_path_label_weight = 4
    function_button_weight = 1
    detect_button_weight = 1
    all_weitght = choose_file_weight + file_path_label_weight + function_button_weight + detect_button_weight

    canvas = tk.Canvas(window, bg='green',
                       width=window.winfo_width(),
                       height=window.winfo_height() - 200)
    canvas.grid(row=0, columnspan=4)

    choose_video_button, video_path_label = get_choose_file_button_and_label(window)
    choose_video_button['text'] = "选择视频"
    video_path_label['fg'] = 'gray'
    video_path_label['bg'] = 'red'
    rotate_video_button = tk.Button(window, text='旋转视频', command=rotate_video)

    choose_video_button.grid(row=1, column=0, sticky='we')
    video_path_label.grid(row=1, column=1, sticky='we')
    rotate_video_button.grid(row=1, column=2, sticky='we')

    choose_model_button, model_path_label = get_choose_file_button_and_label(window)
    choose_model_button['text'] = "选择模型"
    model_path_label['fg'] = 'gray'
    model_path_label['bg'] = 'red'
    choose_classes_button = tk.Button(window, text="选择检测类别")  # TODO: command

    choose_model_button.grid(row=2, column=0, sticky='we')
    model_path_label.grid(row=2, column=1, sticky='we')
    choose_classes_button.grid(row=2, column=2, sticky='we')

    start_detect_button = tk.Button(window, text="开始检测")  # TODO: command
    start_detect_button.grid(row=1, column=3, rowspan=2, sticky='wens')

    process_label = tk.Label(window, text='进度...', fg='gray', bg='#000000')
    process_label.grid(row=3, columnspan=4, sticky='we')

    window.mainloop()


if __name__ == '__main__':
    init_window()
