from tkinter import filedialog
import os


def video_rotate_manual():
    pass


def video_rotate_auto():
    pass


def start_detect():
    pass


def choose_file(string_var=None):
    """:returns file_path"""
    file_path = filedialog.askopenfilename()

    if string_var is not None:
        string_var.set(file_path)

    return file_path


def split_url(url):
    (_dir, file) = os.path.split(url)
    temp = file.split('.')
    filename = temp[0]
    ext = temp[1]
    result = {'dir': _dir, 'filename': filename, 'ext': ext}
    print(result)
    return result
