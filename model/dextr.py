#!/home/ping501f/anaconda3/envs/py36/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cv2
from collections import OrderedDict
import numpy as np
from PIL import Image

import torch
import torch.nn.functional as F

DEXTR_ROOT = "/home/ping501f/member/G3/DEXTR-PyTorch/"
sys.path.append(DEXTR_ROOT)

import networks.deeplab_resnet as resnet
from dataloaders import helpers as helpers

MODEL_CKPT_PATH = os.path.join(DEXTR_ROOT, "models/dextr_pascal-sbd.pth")

MASK_SAVE_PATH = os.path.join(os.getcwd(), "mask.png")
OVERLAY_SAVE_PATH = os.path.join(os.getcwd(), "overlay.png")


def get_expt_coordinate(expt: str) -> np.ndarray:
    expt_list = [float(i) for i in expt.split()]
    return np.array(expt_list, dtype=np.int).reshape(4, 2)


def get_first_frame(video_path: str) -> np.ndarray:
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame


def get_inputs(image, bbox, expt, pad):
    crop_image = helpers.crop_from_bbox(image, bbox, zero_pad=True)
    resize_image = helpers.fixed_resize(crop_image, (512, 512)).astype(np.float32)

    #  Generate extreme point heat map normalized to image values
    extreme_points = expt - [np.min(expt[:, 0]), np.min(expt[:, 1])] + [pad, pad]
    extreme_points = (512 * extreme_points * [1 / crop_image.shape[1], 1 / crop_image.shape[0]]).astype(np.int)
    extreme_heatmap = helpers.make_gt(resize_image, extreme_points, sigma=10)
    extreme_heatmap = helpers.cstm_normalize(extreme_heatmap, 255)

    #  Concatenate inputs and convert to tensor
    input_dextr = np.concatenate((resize_image, extreme_heatmap[:, :, np.newaxis]), axis=2)
    inputs = torch.tensor(input_dextr.transpose((2, 0, 1))[np.newaxis, ...])
    return inputs


def gen_seg(inputs):
    #  Create the network and load the weights
    net = resnet.resnet101(1, nInputChannels=4, classifier="psp")
    state_dict_checkpoint = torch.load(MODEL_CKPT_PATH, map_location=torch.device("cuda"))

    # Remove the prefix .module from the model when it is trained using DataParallel
    if 'module.' in list(state_dict_checkpoint.keys())[0]:
        new_state_dict = OrderedDict()
        for k, v in state_dict_checkpoint.items():
            name = k[7:]  # remove `module.` from multi-gpu training
            new_state_dict[name] = v
    else:
        new_state_dict = state_dict_checkpoint
    net.load_state_dict(new_state_dict)
    net.cuda()
    net.eval()
    
    inputs = inputs.cuda()
    with torch.no_grad():
        outputs = net.forward(inputs)
    outputs = F.interpolate(outputs, size=(512, 512), mode='bilinear', align_corners=True)

    return outputs


def gen_mask(outputs, bbox, im_size, pad, thres):
    pred = np.transpose(outputs.detach().cpu().numpy()[0, ...], (1, 2, 0))
    pred = 1 / (1 + np.exp(-pred))
    pred = np.squeeze(pred)
    mask = helpers.crop2fullmask(pred, bbox, im_size=im_size, zero_pad=True, relax=pad) > thres

    return mask


def gen_init_mask(video_path: str, extreme_points: str) -> str:
    """ Generate mask of a single image by 4 extreme points.

    Args:
        video_path(str): path to original video.
        extreme_points(str): coordinate of 4 extreme points, split by '|'.
    Returns:
        overlay_save_path(str): path to the generated overlay mask.
    """

    pad = 50
    thres = 0.8

    mask_arr = []

    image = get_first_frame(video_path)
    extreme_points = get_expt_coordinate(extreme_points)
    bbox = helpers.get_bbox(image, points=extreme_points, pad=pad, zero_pad=True)
    inputs = get_inputs(image, bbox, extreme_points, pad)
    outputs = gen_seg(inputs) 
    mask = gen_mask(outputs, bbox, image.shape[:2], pad, thres)

    mask_arr.append(mask)

    overlay_mask = helpers.overlay_masks(image/255, mask_arr) * 255

    mask = Image.fromarray(mask)
    mask.save(MASK_SAVE_PATH)
    overlay_mask = Image.fromarray(overlay_mask.astype("uint8"))
    overlay_mask.save(OVERLAY_SAVE_PATH)

    return OVERLAY_SAVE_PATH