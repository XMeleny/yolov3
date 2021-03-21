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


def rotate_image():
    # 可以用个hash map把4个角度的图片存下来，避免多次计算。
    pass


def rotate_video():
    # 获取旋转角度
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


def update_process():
    pass


def init_window():
    # TODO: 用变量把text们都存起来
    # TODO: 修改颜色
    # TODO: 按钮可用状态转换
    window = get_max_window()

    file_path_label_weight = 10  # 表示路径标签的宽度横跨多少列

    choose_video_text = '选择视频'
    video_path_text = '视频位置...'
    rotate_video_text = '旋转视频'
    model_path_text = '模型位置...'
    choose_model_text = '选择模型'
    choose_classes_text = '选择检测类别'
    start_detect_text = '开始检测'
    progress_text = '显示进度...'

    label_relief = 'ridge'

    # 第一行，视频第一帧显示
    canvas = tk.Canvas(window, bg='green',
                       width=window.winfo_width(),
                       height=window.winfo_height() - 200)
    canvas.grid(row=0, columnspan=file_path_label_weight + 3)

    # 第二行，选择视频按钮、视频位置标签、旋转视频按钮
    choose_video_button, video_path_label = get_choose_file_button_and_label(window)
    rotate_video_button = tk.Button(window, text=rotate_video_text, command=rotate_video)

    choose_video_button['text'] = choose_video_text
    video_path_label['text'] = video_path_text
    video_path_label['relief'] = label_relief
    video_path_label['fg'] = 'gray'
    video_path_label['anchor'] = 'w'

    choose_video_button.grid(row=1, column=0, sticky='we')
    video_path_label.grid(row=1, column=1, columnspan=file_path_label_weight, sticky='we')
    rotate_video_button.grid(row=1, column=file_path_label_weight + 1, sticky='we')

    # 第三行，选择模型按钮、模型位置标签、选择检测类别按钮
    choose_model_button, model_path_label = get_choose_file_button_and_label(window)
    choose_classes_button = tk.Button(window, text=choose_classes_text)  # TODO: command

    choose_model_button['text'] = choose_model_text
    model_path_label['text'] = model_path_text
    model_path_label['relief'] = label_relief
    model_path_label['fg'] = 'gray'
    model_path_label['anchor'] = 'w'

    choose_model_button.grid(row=2, column=0, sticky='we')
    model_path_label.grid(row=2, column=1, columnspan=file_path_label_weight, sticky='we')
    choose_classes_button.grid(row=2, column=file_path_label_weight + 1, sticky='we')

    # 跨二三行，检测按钮
    start_detect_button = tk.Button(window, text=start_detect_text)  # TODO: command
    start_detect_button.grid(row=1, column=2 + file_path_label_weight, rowspan=2, sticky='wens')

    # 第四行，进度标签
    process_label = tk.Label(window, fg='gray', text=progress_text, anchor='w', relief=label_relief)
    process_label.grid(row=3, columnspan=3 + file_path_label_weight, sticky='we')

    window.mainloop()


if __name__ == '__main__':
    init_window()
