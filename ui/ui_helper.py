from PIL import ImageTk, Image
import cv2
import tkinter as tk
from tkinter import filedialog
import os
from enum import Enum

'''
# TODO: extract some global variable
like:
    video_path
    model_path
'''


def get_max_window():
    res_window = tk.Tk()
    res_window.title("my window")
    w, h = res_window.maxsize()

    res_window.geometry("{}x{}".format(w, h))
    # res_window.configure(width=w, height=h)

    # res_window.update()
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


def get_choose_file_button_and_label(window, file_type):
    label = tk.Label(window)
    button = tk.Button(window,
                       command=lambda: choose_file(file_type=file_type,
                                                   label=label)
                       )
    return button, label


def get_choose_video_button_and_label(window, canvas):
    label = tk.Label(window)
    button = tk.Button(window, command=lambda: choose_video_click(canvas, label))
    return button, label


# 每种按钮还是有必要分开来写的
def choose_video_click(canvas, label):
    video_type = ".mp4 .m4v .mkv .webm .mov .avi .wmv .mpg .flv"
    video_path = filedialog.askopenfilename(
        filetypes=[("video file", video_type)])  # FIXME: 只支持这几种，有没有必要更多呢 or 判断选择的文件是否视频

    # update canvas
    frame = get_first_frame(video_path)
    show_image_auto_resize(canvas, frame)

    # update label
    label['text'] = video_path

    update_rotate_button_status(video_path)

    update_start_detect_button_status()


def get_first_frame(video_path):
    video_capture = cv2.VideoCapture(video_path)
    success, frame = video_capture.read()
    video_capture.release()
    if success:
        return frame
    else:
        return None


def update_start_detect_button_status():
    """
        if video is not empty and model is not empty, then enable
    """
    pass


def update_choose_classes_button_status():
    """
    if model is not empty
    """
    pass


def update_rotate_button_status(video_path):
    """
    if video path is not empty and video is really video
    :return:
    """
    pass


def rotate_image():
    # 可以用个hash map把4个角度的图片存下来，避免多次计算。
    pass


def rotate_video(video_path, degree):
    # 获取旋转角度
    pass


def start_detect():
    pass


class FileType(Enum):
    video = 1
    model = 2


def choose_file(file_type, label=None):
    if file_type == FileType.video:
        file_path = filedialog.askopenfilename(
            filetypes=[("video file", ".mp4 .m4v .mkv .webm .mov .avi .wmv .mpg .flv")])  # FIXME: 只支持这几种，有没有必要更多呢
    elif file_type == FileType.model:
        file_path = filedialog.askopenfilename(
            filetypes=[("model file", ".pt")])
    else:
        file_path = ''

    # print("file_path = {}".format(file_path))

    if label is not None:
        label['text'] = file_path

    return file_path


def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def is_video(video_path):
    cap = cv2.VideoCapture(video_path)
    result = cap.isOpened()
    cap.release()
    return result


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
    window.update()  # 使长宽正常获取

    file_path_label_weight = 10  # 表示路径标签的宽度横跨多少列

    choose_video_text = '选择视频'
    rotate_video_text = '旋转视频'
    choose_model_text = '选择模型'
    choose_classes_text = '选择检测类别'
    start_detect_text = '开始检测'

    label_relief = 'ridge'

    # 第一行，视频第一帧显示
    canvas = tk.Canvas(window, bg='green',
                       width=window.winfo_width(),
                       height=window.winfo_height() - 200)
    canvas.grid(row=0, columnspan=file_path_label_weight + 3)

    # 第二行，选择视频按钮、视频位置标签、旋转视频按钮
    choose_video_button, video_path_label = get_choose_video_button_and_label(window, canvas)
    rotate_video_button = tk.Button(window, text=rotate_video_text, command=rotate_video)

    choose_video_button['text'] = choose_video_text
    video_path_label['relief'] = label_relief
    video_path_label['fg'] = 'gray'
    video_path_label['anchor'] = 'w'
    rotate_video_button['state'] = tk.DISABLED

    choose_video_button.grid(row=1, column=0, sticky='we')
    video_path_label.grid(row=1, column=1, columnspan=file_path_label_weight, sticky='we')
    rotate_video_button.grid(row=1, column=file_path_label_weight + 1, sticky='we')

    # 第三行，选择模型按钮、模型位置标签、选择检测类别按钮
    choose_model_button, model_path_label = get_choose_file_button_and_label(window, file_type=FileType.model)
    choose_classes_button = tk.Button(window, text=choose_classes_text)  # TODO: command

    choose_model_button['text'] = choose_model_text
    model_path_label['relief'] = label_relief
    model_path_label['fg'] = 'gray'
    model_path_label['anchor'] = 'w'
    choose_classes_button['state'] = tk.DISABLED

    choose_model_button.grid(row=2, column=0, sticky='we')
    model_path_label.grid(row=2, column=1, columnspan=file_path_label_weight, sticky='we')
    choose_classes_button.grid(row=2, column=file_path_label_weight + 1, sticky='we')

    # 跨二三行，检测按钮
    start_detect_button = tk.Button(window, text=start_detect_text)  # TODO: command
    start_detect_button.grid(row=1, column=2 + file_path_label_weight, rowspan=2, sticky='wens')

    # 第四行，进度标签
    process_label = tk.Label(window, fg='gray', anchor='w')
    process_label.grid(row=3, columnspan=3 + file_path_label_weight, sticky='we')

    # 窗口开始主循环
    window.mainloop()


if __name__ == '__main__':
    init_window()
