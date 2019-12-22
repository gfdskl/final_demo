#!/home/ping501f/anaconda3/envs/py36/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cv2
import numpy as np
from PIL import Image

import torch

from .utils import overlay_masks

AGAME_ROOT = "/home/ping501f/member/G3/agame-vos"
sys.path.append(AGAME_ROOT)

from models.agame_model import AGAME

MODEL_CKPT_PATH = os.path.join(AGAME_ROOT, "main_runfile_alpha_best.pth.tar")
MASK_SAVE_PATH = os.path.join(os.getcwd(), "mask.png")

VIDEO_WRITE_PATH = os.path.join(os.getcwd(), "gen_video.avi")


def video2frames(video_path: str):
    video = cv2.VideoCapture(video_path)
    frames = []
    success, frame = video.read()
    while success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame)
        success, frame = video.read()
    frames = np.stack(frames) / 255
    return frames.astype("float32") # (n, h, w, c)


def read_given_seg(mask_path: str):
    mask = Image.open(mask_path)
    return np.array(mask, dtype=np.int)


def gen_segs(frames: np.ndarray, given_seg: np.ndarray):
    """
    Args:
        frames: shape (n, h, w, c)
        given_seg: (h, w)
    """
    frames = torch.tensor(frames).cuda()
    frames = frames.permute(0, 3, 1, 2)
    given_seg = torch.tensor(given_seg).cuda()
    given_seg = given_seg.view(1, 1, given_seg.size(0), given_seg.size(1))
    model = AGAME(
        backbone=('embed_resnets16', (256, 100, True, ('layer4',),('layer4',),('layer2',),('layer1',))),
        appearance=('GaussiansAgame', (2048, 512, .1, -2)),
        dynamic=('SIM', (7, [('ConvRelu', (256+4+4,256,1,1,0)),
                               ('DilationpyramidRelu',(256,256,3,1,(1,3,6),(1,3,6))),
                               ('ConvRelu',(256*3,512,3,1,1))],)),
        fusion=('FusionAgame',
                ([('ConvRelu',(516,512,3,1,1)), ('ConvRelu',(512,128,3,1,1))],
                 [('Conv', (128, 2, 1, 1, 0))])),
        segmod=('UpsampleAgame', ({'s8':512,'s4':256}, 128)),
        update_with_fine_scores=False, update_with_softmax_aggregation=False, process_first_frame=True,
        output_logsegs=False, output_coarse_logsegs=False, output_segs=True)
    model.load_state_dict(torch.load(MODEL_CKPT_PATH)['net'])
    model.cuda()
    model.eval()

    seqlen = 128
    nframes = frames.shape[0]
    partitioned_frames = [frames[start_idx : start_idx + seqlen] for start_idx in range(0, nframes, seqlen)]

    init = True
    with torch.no_grad():
        states = None
        segs = []
        for part in partitioned_frames:
            output, states = model(part.unsqueeze(0).cuda(), given_seg if init else None, states)
            s = output['segs'].squeeze()
            segs.append(s.detach().cpu().numpy())
            init = False
        segs = np.concatenate(segs, axis=0)
    return segs # (n, h, w)


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
        n_object = len(np.unique(anno))
    oh_anno = [anno == i for i in range(n_object)]
    oh_anno = np.stack(oh_anno)
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
        overlay.append(overlay_masks(frame, seg[1]) * 255)

    writer = cv2.VideoWriter(VIDEO_WRITE_PATH, cv2.VideoWriter_fourcc(*"XVID"), 24, (frames.shape[2], frames.shape[1]))

    for ol in overlay:
        writer.write(ol.astype("uint8"))
    
    writer.release()


def do_vos(video_path: str) -> str:
    """ Generate segmentation of given video and initial annotation, this function returns a path where the generated video saved.

    Args:
        video_path(str): path to original video.
    Returns:
        video_write_path(str): path to the generated video.
    """
    given_seg = read_given_seg(MASK_SAVE_PATH)
    frames = video2frames(video_path)
    segs = gen_segs(frames, given_seg)
    get_overlay_video(frames, segs)

    return VIDEO_WRITE_PATH