import os
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import ImageTk, Image

from models.experimental import attempt_load

import func_detect

from _thread import *


# TODO: delete test data and test code
# TODO: 耗时操作打 progress
# TODO: 打 log
# TODO: 按钮 enable 和 disable

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
    list_all_classes = []
    set_chosen_classes = {}

    is_video = False
    is_model = False
    getting_model = False
    rotating = False
    detecting = False

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

    @staticmethod
    def get_max_window():
        res_window = tk.Tk()
        res_window.title("my window")

        w, h = res_window.maxsize()
        res_window.geometry("{}x{}".format(w, h))

        return res_window

    @staticmethod
    def print_winfo(widget):
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
        self.model_path = filedialog.askopenfilename(filetypes=[(self.TEXT_MODEL_FILE_TYPE, self.MODEL_TYPE)])
        self.label_model_path['text'] = self.model_path

        try:
            start_new_thread(self.choose_model, ())  # 获取 all_classes 是耗时操作，需要多线程操作，避免卡死页面
        except Exception:
            print(Exception)
            print("error: unable to start a new thread")

    def setup_classes(self):
        # clear
        self.list_all_classes = []

        # TODO: move this part to func_detect.py
        # get classes, time consuming
        self.update_progress("开始检测分类...")
        if len(self.model_path) > 0:
            model = attempt_load(self.model_path)
            self.list_all_classes = model.module.names if hasattr(model, 'module') else model.names
        self.update_progress("分类检测完成...")
        # test
        # for i in range(50):
        #     self.list_all_classes.append(str(i))

        # print(f"all_classes = {self.all_classes}")

        # 默认全选
        self.set_chosen_classes.clear()
        for class_name in self.list_all_classes:
            self.set_chosen_classes[class_name] = tk.BooleanVar(value=True)

    def choose_model(self):
        self.setup_classes()

        self.update_btn_choose_classes_state()
        self.update_btn_start_detect_state()

    def choose_classes_clicked(self):
        # TODO: 焦点控制。如何将焦点控制在新打开的窗口，在新窗口打开的时候不允许点击主窗口？
        self.show_choose_window()

    def show_choose_window(self):
        choose_window = tk.Toplevel(self.window)
        choose_window.title('choose classes to detect')

        canvas_weight = 10

        # 修正 canvas_weight 为奇数
        if canvas_weight % 2 == 0:
            canvas_weight += 1

        all_weight = canvas_weight + 1
        half_weight = int(all_weight / 2)

        canvas = tk.Canvas(choose_window)
        canvas.grid(row=0, column=0, columnspan=canvas_weight)

        scrollbar = tk.Scrollbar(choose_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=canvas_weight, sticky='ns')

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas)

        for idx, class_name in enumerate(self.list_all_classes):
            tk.Checkbutton(frame, text=class_name, variable=self.set_chosen_classes[class_name]).grid(row=idx)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # 要 update 才能正常设置
        choose_window.update()
        canvas.configure(scrollregion=canvas.bbox("all"))

        btn_select_all = tk.Button(choose_window, text="select all", command=self.select_all_clicked)
        btn_select_all.grid(row=1, column=0, columnspan=half_weight, sticky='we')

        btn_deselect_all = tk.Button(choose_window, text='deselect all', command=self.deselect_all_clicked)
        btn_deselect_all.grid(row=1, column=half_weight, columnspan=half_weight, sticky='we')

        btn_confirm = tk.Button(choose_window, text="confirm", command=lambda: self.confirm_clicked(choose_window))
        btn_confirm.grid(row=2, column=0, columnspan=all_weight, sticky='we')

        choose_window.mainloop()

    def select_all_clicked(self):
        for bool_var in self.set_chosen_classes.values():
            bool_var.set(True)

    def deselect_all_clicked(self):
        for bool_var in self.set_chosen_classes.values():
            bool_var.set(False)

    def confirm_clicked(self, choose_window):
        print(f'res = {self.get_chosen_classes_list()}')
        choose_window.destroy()

    def get_chosen_classes_list(self):
        res = []
        for key in self.set_chosen_classes:
            if self.set_chosen_classes[key].get() and key in self.list_all_classes:
                res.append(self.list_all_classes.index(key))
        return res

    def start_detect_clicked(self):
        try:
            start_new_thread(self.start_detect, ())
        except Exception:
            print(Exception)
            print("error: unable to start a new thread")

    def start_detect(self):
        self.rotate_video()
        func_detect.func_detect(weights=self.model_path,
                                source=self.get_rotated_video_path(),
                                classes=self.get_chosen_classes_list())

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

        # FIXME: 尝试 window.update() 看获取 winfo_width 是否正常
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
        if self.rotate_degree == 0:
            return

        self.update_progress("开始旋转视频...")
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

        self.update_progress("视频旋转完成...")

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

    def update_btn_choose_classes_state(self):
        if len(self.list_all_classes) > 0:
            self.btn_choose_classes['state'] = tk.NORMAL
        else:
            self.btn_choose_classes['state'] = tk.DISABLED

    def update_btn_start_detect_state(self):
        if self.is_video and len(self.list_all_classes) > 0:
            self.btn_start_detect['state'] = tk.NORMAL
        else:
            self.btn_start_detect['state'] = tk.DISABLED

    def update_progress(self, text):
        self.label_process['text'] = text

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
