import cv2
import numpy as np

from PIL import ImageTk, Image


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


def rotate_video(video_path, rotate_degree, des_path):
    if rotate_degree == 0:
        return

    src_video = cv2.VideoCapture(video_path)
    fourcc = int(src_video.get(cv2.CAP_PROP_FOURCC))
    fps = src_video.get(cv2.CAP_PROP_FPS)
    w = int(src_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(src_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if rotate_degree % 180 == 0:
        size = (w, h)
    else:
        size = (h, w)

    video_writer = cv2.VideoWriter(des_path, fourcc, fps, size)

    read_status, video_frame = src_video.read()
    while read_status:
        video_frame = rotate_frame(video_frame, rotate_degree)
        video_writer.write(video_frame)
        read_status, video_frame = src_video.read()

    src_video.release()
    video_writer.release()
    print("video rotate done")


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


tk_img_dict = {}
default_tag = ''
all_tag = 'all'


def show_frame_in_canvas_auto_resize(canvas, frame, tag=default_tag):
    # self.window.update()  # 竟然不需要 update 就能正常获取 w 和 h
    # self.print_winfo(self.canvas)
    canvas.update()

    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    # print(f"canvas w, h = {canvas_width}, {canvas_height}")

    shape = frame.shape
    pic_width = shape[1]
    pic_height = shape[0]
    # print(f"pic w, h = {pic_width}, {pic_height}")

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

    result_cv_image = cv2.resize(frame, (int(w), int(h)))

    # canvas显示opencv格式的图片
    tk_img = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(result_cv_image, cv2.COLOR_BGR2RGB)))
    add_to_tk_img_list(tk_img, tag)  # 必须保持对图片的引用
    center_x = int(canvas_width / 2)
    center_y = int(canvas_height / 2)
    canvas.create_image(center_x, center_y, image=tk_img)


def add_to_tk_img_list(tk_img, tag):
    if tag not in tk_img_dict:
        tk_img_dict[tag] = []
    tk_img_dict[tag].append(tk_img)


def clear_tk_img_list(tag=all_tag):
    if tag == all_tag or tag not in tk_img_dict:
        tk_img_dict.clear()
    else:
        tk_img_dict[tag].clear()


if __name__ == '__main__':
    pass
