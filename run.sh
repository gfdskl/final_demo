#!/bin/bash

cd /home/ping501f/member/G3/final_demo

avi_path="./gen_video.avi"
mp4_path="./gen_video.mp4"

source ~/anaconda3/etc/profile.d/conda.sh
conda activate py36
python main.py $1 $2

ffmpeg -y -i $avi_path -vcodec libx264 $mp4_path