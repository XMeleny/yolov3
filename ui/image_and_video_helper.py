import cv2
import numpy as np


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


if __name__ == '__main__':
    pass
