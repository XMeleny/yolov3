import time

import cv2
import torch
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import check_img_size, non_max_suppression, scale_coords, set_logging
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized

from path_helper import *


# TODO: rename to helper.py

def real_detect(weights, source, conf_threshold, iou_threshold, classes):
    imgsz = 640
    split_result = split_url(source)

    save_dir = split_result['dir']

    # Initialize
    set_logging()
    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Set Dataloader
    vid_path, vid_writer = None, None
    save_img = True
    dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names  # 应该是在这里获得names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, conf_threshold, iou_threshold, classes=classes, agnostic=False)
        t2 = time_synchronized()

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            s, im0, frame = '', im0s, getattr(dataset, 'frame', 0)

            save_path = get_des_file_path(path, suffix="detected")

            s += '%gx%g ' % img.shape[2:]  # print string
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f'{n} {names[int(c)]}s, '  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_img:  # Add bbox to image
                        label = f'{names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=3)

                        # TODO: print custom information, remind that classes_ may be None
                        # # xmer: 在下面可以print，也就可以alarm
                        # if int(cls) in classes_:
                        #     print(f"xm: detected {names[int(cls)]}")

            # Print time (inference + NMS)
            print(f'{s}Done. ({t2 - t1:.3f}s)')

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video'
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fourcc = 'mp4v'  # output video codec
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                    vid_writer.write(im0)

    print(f"Results saved to {save_dir}")
    print(f'Done. ({time.time() - t0:.3f}s)')  # 展示总时间


# TODO: add params 1. alarm 2. log
def func_detect(weights, source, conf_threshold=0.25, iou_threshold=0.45, classes=None):
    with torch.no_grad():
        real_detect(weights, source, conf_threshold, iou_threshold, classes)


if __name__ == '__main__':
    func_detect(
        weights=r"C:\Users\Meleny\Desktop\m'file\compulsory courses\GraduationProject\dataset\best.pt",
        source=r"C:\Users\Meleny\Desktop\m'file\compulsory courses\GraduationProject\dataset\video\test.mp4",
        classes=[1]
    )
