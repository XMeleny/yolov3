import os
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import ImageTk, Image


class Window:
    # ui
    window = None

    canvas = None

    btn_choose_video = None
    label_video_path = None
    btn_rotate_video = None

    btn_choose_model = None
    label_model_path = None
    btn_choose_classes = None

    btn_start_detect = None

    label_process = None

    # ui pattern
    LABEL_RELIEF = tk.RIDGE
    LABEL_FOREGROUND = 'gray'
    LABEL_ANCHOR = tk.W
    FILE_PATH_LABEL_WEIGHT = 10  # 表示路径标签的宽度横跨多少列

    # data
    TEXT_CHOOSE_VIDEO = '选择视频'
    TEXT_ROTATE_VIDEO = '旋转视频'
    TEXT_CHOOSE_MODEL = '选择模型'
    TEXT_CHOOSE_CLASSES = '选择检测类别'
    TEXT_START_DETECT = '开始检测'

    TEXT_VIDEO_FILE_TYPE = "视频文件"
    TEXT_MODEL_FILE_TYPE = "模型文件"

    TEXT_TEST = "testing..."

    VIDEO_TYPE = ".mp4 .m4v .mkv .webm .mov .avi .wmv .mpg .flv"
    MODEL_TYPE = ".pt"

    first_frame = None
    rotate_degree = 0
    video_path = ""
    model_path = ""
    is_video = False
    classes = []

    def __init__(self):
        self.init_ui()

    def init_ui(self):
        self.window = Window.get_max_window()
        self.window.update()

        self.create_widgets()
        self.layout()
        self.bind_ui_data()

        self.init_button_state()
        self.bind_ui_function()

        self.window.mainloop()

    def create_widgets(self):
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        self.canvas = tk.Canvas(self.window, width=w, height=h - 200)

        self.btn_choose_video = tk.Button(self.window)
        self.label_video_path = tk.Label(self.window)
        self.btn_rotate_video = tk.Button(self.window)

        self.btn_choose_model = tk.Button(self.window)
        self.label_model_path = tk.Label(self.window)
        self.btn_choose_classes = tk.Button(self.window)

        self.btn_start_detect = tk.Button(self.window)

        self.label_process = tk.Label(self.window)

    def layout(self):
        self.canvas.grid(row=0, columnspan=self.FILE_PATH_LABEL_WEIGHT + 3)

        self.btn_choose_video.grid(row=1, column=0, sticky='we')
        self.label_video_path.grid(row=1, column=1, columnspan=self.FILE_PATH_LABEL_WEIGHT, sticky='we')
        self.btn_rotate_video.grid(row=1, column=self.FILE_PATH_LABEL_WEIGHT + 1, sticky='we')

        self.btn_choose_model.grid(row=2, column=0, sticky='we')
        self.label_model_path.grid(row=2, column=1, columnspan=self.FILE_PATH_LABEL_WEIGHT, sticky='we')
        self.btn_choose_classes.grid(row=2, column=self.FILE_PATH_LABEL_WEIGHT + 1, sticky='we')

        self.btn_start_detect.grid(row=1, rowspan=2, column=self.FILE_PATH_LABEL_WEIGHT + 2, sticky='wens')

        self.label_process.grid(row=3, columnspan=self.FILE_PATH_LABEL_WEIGHT + 3, sticky='we')

    def bind_ui_data(self):
        self.btn_choose_video['text'] = self.TEXT_CHOOSE_VIDEO
        self.btn_rotate_video['text'] = self.TEXT_ROTATE_VIDEO
        self.btn_choose_model['text'] = self.TEXT_CHOOSE_MODEL
        self.btn_choose_classes['text'] = self.TEXT_CHOOSE_CLASSES
        self.btn_start_detect['text'] = self.TEXT_START_DETECT

        self.label_video_path['relief'] = self.LABEL_RELIEF
        self.label_model_path['relief'] = self.LABEL_RELIEF

        self.label_video_path['fg'] = self.LABEL_FOREGROUND
        self.label_model_path['fg'] = self.LABEL_FOREGROUND
        self.label_process['fg'] = self.LABEL_FOREGROUND

        self.label_video_path['anchor'] = self.LABEL_ANCHOR
        self.label_model_path['anchor'] = self.LABEL_ANCHOR
        self.label_process['anchor'] = self.LABEL_ANCHOR

    def init_button_state(self):
        self.btn_rotate_video['state'] = tk.DISABLED
        self.btn_choose_classes['state'] = tk.DISABLED
        self.btn_start_detect['state'] = tk.DISABLED

    def bind_ui_function(self):
        self.btn_choose_video['command'] = lambda: self.choose_video_clicked()
        self.btn_choose_model['command'] = lambda: self.choose_model_clicked()
        self.btn_rotate_video['command'] = lambda: self.rotate_video_clicked()
        self.btn_choose_classes['command'] = lambda: self.choose_classes_clicked()
        self.btn_start_detect['command'] = lambda: self.start_detect_clicked()

    @classmethod
    def get_max_window(cls):
        res_window = tk.Tk()
        res_window.title("my window")

        w, h = res_window.maxsize()
        res_window.geometry("{}x{}".format(w, h))

        return res_window

    @classmethod
    def print_winfo(cls, widget):
        print(f'widget.winfo_width = {widget.winfo_width()}')
        print(f'widget.winfo_reqwidth = {widget.winfo_reqwidth()}')
        print(f'widget.winfo_vrootwidth = {widget.winfo_vrootwidth()}')
        print(f'widget.winfo_screenmmwidth = {widget.winfo_screenmmwidth()}')
        print(f'widget.winfo_screenwidth = {widget.winfo_screenwidth()}')

    def choose_video_clicked(self):
        self.update_video_path()
        self.update_label_video_path()

        self.update_is_video()
        self.update_first_frame()
        self.update_canvas_frame_auto_resize()

        self.update_btn_rotate_video_state()
        self.update_btn_start_detect_state()

        self.rotate_degree = 0

    def rotate_video_clicked(self):
        self.rotate_first_frame()

    def choose_model_clicked(self):
        print("choose_model_clicked")
        # TODO: classes = get_all_classes(model)
        # TODO: update start_detect state

    def choose_classes_clicked(self):
        print("choose_classes_clicked")
        # TODO: get classes and show, and refresh the chosen classes

    def start_detect_clicked(self):
        self.rotate_video()

    def update_video_path(self):
        self.video_path = filedialog.askopenfilename(filetypes=[(self.TEXT_VIDEO_FILE_TYPE, self.VIDEO_TYPE)])

    def update_label_video_path(self):
        self.label_video_path['text'] = self.video_path

    def update_is_video(self):
        if len(self.video_path) <= 0:
            self.is_video = False
            return

        cap = cv2.VideoCapture(self.video_path)
        self.is_video = cap.isOpened()
        cap.release()

    def update_first_frame(self):
        if len(self.video_path) <= 0 or not self.is_video:
            self.first_frame = None
            return

        video_capture = cv2.VideoCapture(self.video_path)
        success, frame = video_capture.read()
        video_capture.release()
        if success:
            self.first_frame = frame
        else:
            self.first_frame = None

    def update_canvas_frame_auto_resize(self):
        if self.first_frame is None:
            self.canvas.delete("all")
            return

        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()

        shape = self.first_frame.shape
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

        result_cv_image = cv2.resize(self.first_frame, (int(w), int(h)))

        # canvas显示opencv格式的图片
        global tk_img  # 必须保持对图片的引用
        tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(result_cv_image, cv2.COLOR_BGR2RGB)))

        center_x = int(canvas_width / 2)
        center_y = int(canvas_height / 2)
        self.canvas.create_image(center_x, center_y, image=tk_img)

    def rotate_first_frame(self):
        if self.first_frame is None:
            return

        self.rotate_degree = (self.rotate_degree + 90) % 360
        self.first_frame = self.rotate_frame(self.first_frame, 90)
        self.update_canvas_frame_auto_resize()

    @staticmethod
    def rotate_frame(frame, degree):
        if frame is None:
            return None
        else:
            h, w = frame.shape[:2]
            (cx, cy) = (w / 2, h / 2)

            # 设置旋转矩阵
            matrix = cv2.getRotationMatrix2D((cx, cy), -degree, scale=1.0)  # FIXME: -degree 和 degree有什么区别吗？
            cos = np.abs(matrix[0, 0])
            sin = np.abs(matrix[0, 1])

            # 计算图像旋转后的新边界
            nW = int((h * sin) + (w * cos))
            nH = int((h * cos) + (w * sin))

            # 调整旋转矩阵的移动距离（t_{x}, t_{y}）
            matrix[0, 2] += (nW / 2) - cx
            matrix[1, 2] += (nH / 2) - cy

            frame = cv2.warpAffine(frame.copy(), matrix, (nW, nH))
            return frame

    def rotate_video(self):
        # TODO: show progress
        if self.rotate_degree == 0:
            return

        src_video = cv2.VideoCapture(self.video_path)
        fourcc = int(src_video.get(cv2.CAP_PROP_FOURCC))
        fps = src_video.get(cv2.CAP_PROP_FPS)
        w = int(src_video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(src_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if self.rotate_degree % 180 == 0:
            size = (w, h)
        else:
            size = (h, w)

        video_writer = cv2.VideoWriter(self.get_rotated_video_path(), fourcc, fps, size)

        read_status, video_frame = src_video.read()
        while read_status:
            video_frame = Window.rotate_frame(video_frame, self.rotate_degree)
            video_writer.write(video_frame)
            read_status, video_frame = src_video.read()

        src_video.release()
        video_writer.release()

    @staticmethod
    def split_url(url):
        (_dir, file) = os.path.split(url)
        temp = file.split('.')
        filename = temp[0]
        ext = temp[1]
        return {'dir': _dir, 'filename': filename, 'ext': ext}

    @staticmethod
    def get_des_file_path(src_url, prefix='', suffix='', ext=''):
        split_result = Window.split_url(src_url)

        # 添加前后缀
        filename = split_result['filename']
        if len(prefix) > 0:
            filename = prefix + "_" + filename
        if len(suffix) > 0:
            filename = filename + "_" + suffix

        # 添加文件格式
        if len(ext) == 0:
            filename = filename + "." + split_result['ext']
        else:
            filename = filename + "." + ext

        des_url = os.path.join(split_result['dir'], filename)
        # print(f'des_url = {des_url}')
        return des_url

    def get_rotated_video_path(self):
        if self.rotate_degree == 0:
            return self.video_path
        return Window.get_des_file_path(self.video_path, suffix=f'rotated_{self.rotate_degree}')

    def update_btn_rotate_video_state(self):
        if self.is_video:
            self.btn_rotate_video['state'] = tk.NORMAL
        else:
            self.btn_rotate_video['state'] = tk.DISABLED

    def update_btn_start_detect_state(self):
        # is video and is model, enable
        pass

    def log(self):
        pass


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


if __name__ == '__main__':
    window = Window()
