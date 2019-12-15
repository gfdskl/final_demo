#!/home/ping501f/anaconda3/envs/py36/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np

import torch

AGAME_ROOT = "/home/ping501f/member/G3/agame-vos/"
sys.path.append(AGAME_ROOT)

from models.agame_model import AGAME
import utils

MODEL_CKPT_PATH = os.path.join(AGAME_ROOT, "main_runfile_alpha_best.pth.tar")

VIDEO_WRITE_PATH = os.path.join(os.getcwd(), "gen_video.avi")


def video2frames(video_path: str):
    video = cv2.VideoCapture(video_path)
    frames = []
    success, frame = video.read()
    while success:
        frames.append(frame)
        success, frame = video.read()
    frames = np.stack(frames)
    return frames # (n, h, w, c)


def gen_segs(frames: np.ndarray, given_seg: np.ndarray):
    """
    Args:
        frames: shape (n, h, w, c)
        given_seg: (h, w)
    """
    frames = torch.tensor(frames).cuda()
    frames = frames.permute(0, 3, 1, 2)
    given_seg = torch.tensor(given_seg).cuda()
    frames = frames.unsqueeze(0)
    given_seg = given_seg.view(1, 1, given_seg.size(0), given_seg.size(1))
    model = AGAME()
    model.load_state_dict(torch.load(MODEL_CKPT_PATH))
    model.eval()
    with torch.no_grad():
        output, _ = model(frames, given_seg)
        segs = output['segs'].squeeze()
    return segs.detach().numpy() # (n, h, w)


def to_onehot_anno(anno, n_object=None):
    """
    Convert a dense annotation map to one-hot version.
    Args:
        anno: dense annotation of shape (h, w).
        n_object: object number.
    Returns:
        oh_anno: onne-hot annnotation of shape (n_object, h, w).
    """
    if not n_object:
        n_object = len(anno.unique())
    oh_anno = [anno == i for i in range(n_object)]
    oh_anno = numpy.stack(oh_anno)
    return oh_anno


def get_overlay_video(frames: np.ndarray, segs: np.ndarray):
    """
    Args:
        frames: shape (n, h, w, c)
        segs: shape (n, h, w)
    """
    overlay = []
    for frame, seg in zip(frames, segs):
        seg = to_onehot_anno(seg) # (n_obj, h, w)
        overlay.append(utils.overlay_masks(frame/255, seg))

    writer = cv2.VideoWriter(VIDEO_WRITE_PATH, cv2.VideoWriter_fourcc(*'XVID'), 24, (frames.shape[2], frames.shape[1]))

    for ol in overlay:
        writer.write(ol)
    
    writer.release()


def do_vos(video_path: str, given_seg: np.ndarray) -> str:
    """ Generate segmentation of given video and initial annotation, this function returns a path where the generated video saved.

    Args:
        video_path(str): path to original video.
        given_seg(np.ndarray): segmentation of first frame of shape (h, w), generated from dextr.
    Returns:
        video_write_path(str): path to the generated video.
    """
    frames = video2frames(video_path)
    segs = gen_segs(frames, given_seg)
    get_overlay_video(frames, segs)

    return VIDEO_WRITE_PATH