from _thread import *
from tkinter import filedialog
from tkinter import messagebox

from detect_helper import *
from image_and_video_helper import *
from path_helper import *
from widget_helper import *


class Window:
    # ui
    window = None
    choose_window = None
    result_window = None

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

    VIDEO_TYPE = ".mp4 .m4v .mkv .webm .mov .avi .wmv .mpg .flv"
    MODEL_TYPE = ".pt"

    TAG_CANVAS = 'canvas'
    TAG_TEMP = 'temp'

    WINDOW_CLOSE_EVENT = "WM_DELETE_WINDOW"

    first_frame = None
    rotate_degree = 0
    video_path = ""
    model_path = ""
    list_all_classes = []
    dict_chosen_classes = {}

    is_video = False
    is_model = False

    result_album = {}

    def __init__(self):
        self.init_ui()

    def init_ui(self):
        self.window = get_max_window()
        self.window.update()

        self.create_widgets()
        self.layout()
        self.bind_ui_data()

        self.init_button_state()
        self.bind_ui_function()

        self.window.protocol(self.WINDOW_CLOSE_EVENT, self.on_closing)
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

    def enable_btn_rotate_video(self):
        if self.is_video:
            self.btn_rotate_video['state'] = tk.NORMAL

    def enable_btn_choose_classes(self):
        if self.is_model:
            self.btn_choose_classes['state'] = tk.NORMAL

    def enable_btn_start_detect(self):
        if self.is_video and self.is_model:
            self.btn_start_detect['state'] = tk.NORMAL
        if len(self.result_album) > 0:
            self.btn_start_detect['text'] = '显示结果'

    def restore_result_data(self):
        self.result_album = {}
        self.btn_start_detect['text'] = self.TEXT_START_DETECT

    def choose_video_clicked(self):
        self.restore_video_data()
        self.restore_video_widgets()
        self.get_video()

    def restore_video_data(self):
        self.is_video = False
        self.video_path = ""
        self.rotate_degree = 0
        self.first_frame = None
        self.restore_result_data()

    def restore_video_widgets(self):
        self.btn_rotate_video['state'] = tk.DISABLED
        self.btn_start_detect['state'] = tk.DISABLED
        self.label_video_path['text'] = self.video_path
        self.update_progress("")
        self.canvas.delete("all")
        clear_tk_img_list()

    def get_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[(self.TEXT_VIDEO_FILE_TYPE, self.VIDEO_TYPE)])
        self.label_video_path['text'] = self.video_path
        try:
            start_new_thread(self.thread_get_first_frame, ())
        except Exception as e:
            print(f"error when start new thread, Exception = {e}")

    def thread_get_first_frame(self):
        """
        This function should be run in new thread.
        Please use start_new_thread to run this function
        """
        if len(self.video_path) <= 0:
            return

        self.update_progress("获取视频开始...")
        cap = cv2.VideoCapture(self.video_path)

        self.is_video = cap.isOpened()

        if self.is_video:
            success, frame = cap.read()
            if success:
                self.first_frame = frame
                show_frame_in_canvas_auto_resize(self.canvas, self.first_frame, self.TAG_CANVAS)
                self.enable_btn_rotate_video()
                self.enable_btn_start_detect()

        cap.release()
        self.update_progress("视频获取完成...")

    def rotate_video_clicked(self):
        self.rotate_first_frame()
        self.restore_result_data()

    def choose_model_clicked(self):
        self.restore_model_data()
        self.restore_model_widgets()
        self.get_model()

    def restore_model_data(self):
        self.is_model = False
        self.model_path = ""
        self.list_all_classes = []
        self.dict_chosen_classes = {}
        self.restore_result_data()

    def restore_model_widgets(self):
        self.btn_choose_classes['state'] = tk.DISABLED
        self.btn_start_detect['state'] = tk.DISABLED
        self.label_model_path['text'] = self.model_path
        self.update_progress("")

    def get_model(self):
        self.model_path = filedialog.askopenfilename(filetypes=[(self.TEXT_MODEL_FILE_TYPE, self.MODEL_TYPE)])
        self.label_model_path['text'] = self.model_path
        try:
            start_new_thread(self.thread_get_classes, ())
        except Exception as e:
            print(f"error when start new thread, Exception = {e}")

    def thread_get_classes(self):
        """
        This function should be run in new thread.
        Please use start_new_thread to run this function
        """
        if len(self.model_path) <= 0:
            return

        self.update_progress("开始获取检测类型...")
        try:
            model = attempt_load(self.model_path)

            self.is_model = True

            self.list_all_classes = model.module.names if hasattr(model, 'module') else model.names
            for class_name in self.list_all_classes:
                self.dict_chosen_classes[class_name] = tk.BooleanVar(value=True)

            self.enable_btn_choose_classes()
            self.enable_btn_start_detect()
        except Exception as e:
            self.is_model = False
            print(f"error when getting classes, Exception = {e}")

        self.update_progress("检测类型获取完成...")

    def choose_classes_clicked(self):
        # TODO: 焦点控制。如何将焦点控制在新打开的窗口，在新窗口打开的时候不允许点击主窗口？
        self.show_choose_window()
        self.restore_result_data()

    def show_choose_window(self):
        if self.choose_window is not None:
            return
        self.choose_window = tk.Toplevel(self.window)
        self.choose_window.title('choose classes to detect')

        canvas_weight = 10

        # 修正 canvas_weight 为奇数
        if canvas_weight % 2 == 0:
            canvas_weight += 1

        all_weight = canvas_weight + 1
        half_weight = int(all_weight / 2)

        canvas = tk.Canvas(self.choose_window)
        canvas.grid(row=0, column=0, columnspan=canvas_weight)

        scrollbar = tk.Scrollbar(self.choose_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.grid(row=0, column=canvas_weight, sticky='ns')

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas)

        for idx, class_name in enumerate(self.list_all_classes):
            tk.Checkbutton(frame, text=class_name, variable=self.dict_chosen_classes[class_name]).grid(row=idx)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # 要 update 才能正常设置
        self.choose_window.update()
        canvas.configure(scrollregion=canvas.bbox("all"))

        btn_select_all = tk.Button(self.choose_window, text="select all", command=self.select_all_clicked)
        btn_select_all.grid(row=1, column=0, columnspan=half_weight, sticky='we')

        btn_deselect_all = tk.Button(self.choose_window, text='deselect all', command=self.deselect_all_clicked)
        btn_deselect_all.grid(row=1, column=half_weight, columnspan=half_weight, sticky='we')

        btn_confirm = tk.Button(self.choose_window, text="confirm", command=self.on_choose_window_closing)
        btn_confirm.grid(row=2, column=0, columnspan=all_weight, sticky='we')

        self.choose_window.protocol(self.WINDOW_CLOSE_EVENT, self.on_choose_window_closing)
        self.choose_window.mainloop()

    def select_all_clicked(self):
        for bool_var in self.dict_chosen_classes.values():
            bool_var.set(True)

    def deselect_all_clicked(self):
        for bool_var in self.dict_chosen_classes.values():
            bool_var.set(False)

    def get_chosen_classes_list(self):
        res = []
        for key in self.dict_chosen_classes:
            if self.dict_chosen_classes[key].get() and key in self.list_all_classes:
                res.append(self.list_all_classes.index(key))
        return res

    def start_detect_clicked(self):
        if len(self.result_album) == 0:
            self.disable_all_buttons()
            self.start_detect()
        else:
            self.show_result_window()

    def disable_all_buttons(self):
        self.btn_choose_video['state'] = tk.DISABLED
        self.btn_choose_model['state'] = tk.DISABLED
        self.btn_rotate_video['state'] = tk.DISABLED
        self.btn_choose_classes['state'] = tk.DISABLED
        self.btn_start_detect['state'] = tk.DISABLED

    def enable_all_buttons(self):
        self.btn_choose_video['state'] = tk.NORMAL
        self.btn_choose_model['state'] = tk.NORMAL
        self.enable_btn_rotate_video()
        self.enable_btn_choose_classes()
        self.enable_btn_start_detect()

    def thread_start_detect(self):
        """
        This function should be run in new thread.
        Please use start_new_thread to run this function
        """
        if self.rotate_degree != 0:
            self.update_progress("开始旋转视频...")
            rotate_video(self.video_path, self.rotate_degree, self.get_rotated_video_path())
            self.update_progress("视频旋转完成...")

        self.update_progress("开始检测...")
        func_detect(weights=self.model_path,
                    source=self.get_rotated_video_path(),
                    classes=self.get_chosen_classes_list(),
                    log_function=self.update_progress,
                    update_album_function=self.update_result_album)
        self.update_progress("检测完成...")

        self.enable_all_buttons()

    def start_detect(self):
        try:
            start_new_thread(self.thread_start_detect, ())
        except Exception as e:
            print(f"error when start new thread, Exception = {e}")

    def rotate_first_frame(self):
        self.rotate_degree = (self.rotate_degree + 90) % 360
        # print(f"rotate degree = {self.rotate_degree}")
        self.first_frame = rotate_frame(self.first_frame, 90)
        clear_tk_img_list(self.TAG_CANVAS)
        show_frame_in_canvas_auto_resize(self.canvas, self.first_frame, self.TAG_CANVAS)

    def get_rotated_video_path(self):
        if self.rotate_degree == 0:
            return self.video_path
        return get_des_file_path(self.video_path, suffix=f'rotated_{self.rotate_degree}')

    def get_save_path(self):
        return get_detected_save_path(self.get_rotated_video_path())

    def update_progress(self, text):
        print(text)
        self.label_process['text'] = text

    def update_result_album(self, album):
        self.result_album = album

    def show_result_window(self):
        if self.result_album is None:
            return

        self.result_window = tk.Toplevel(self.window)
        self.result_window.geometry('600x400')
        self.result_window.title('检测结果')
        self.result_window.update()

        album_length = len(self.result_album)
        canvas_width = int(self.result_window.winfo_width() / album_length)
        idx = 0
        list_result_canvas = []
        for img in self.result_album.values():
            result_canvas = tk.Canvas(self.result_window, width=canvas_width)
            result_canvas.grid(row=0, column=idx, columnspan=1)
            result_canvas.update()
            list_result_canvas.append(result_canvas)
            show_frame_in_canvas_auto_resize(result_canvas, img, self.TAG_TEMP)
            idx += 1

        result_label = tk.Label(self.result_window, text=f"检测详细结果请查看：\n{self.get_save_path()}")
        # result_label = tk.Label(self.result_window, text=f"检测详细结果请查看")
        result_label.grid(row=1, columnspan=idx, sticky='we')

        self.result_window.protocol(self.WINDOW_CLOSE_EVENT, self.on_result_window_closing)
        self.result_window.mainloop()

    def on_closing(self):
        video_state = self.btn_choose_video['state']
        model_state = self.btn_choose_model['state']
        disable = tk.DISABLED

        if video_state == disable and model_state == disable:
            if messagebox.askokcancel("退出", "退出会导致检测失败，确定退出吗？"):
                self.window.destroy()
        else:
            self.window.destroy()

    def on_result_window_closing(self):
        clear_tk_img_list(self.TAG_TEMP)
        self.result_window.destroy()
        self.result_window = None

    def on_choose_window_closing(self):
        self.choose_window.destroy()
        self.choose_window = None


if __name__ == '__main__':
    window = Window()
