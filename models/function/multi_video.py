import sys
import cv2
import numpy as np
import moviepy
from moviepy.editor import *


leftfile = "video/youtube_video.mp4"  # 왼손코딩 강의 영상 
rightfile = "output/output_video.mp4" # 왼손코딩 강의를 수어로 번역한 영상


def get_duration(filename): #영상 길이 반환 함수
    clip = VideoFileClip(filename)
    return clip.duration

length_L = get_duration(leftfile)  # 왼쪽 영상 길이 
length_R = get_duration(rightfile) # 오른쪽 영상 길이 반환

clip1 = VideoFileClip(leftfile).subclip(0, 0 + length_L).margin(2) # 왼쪽 영상 
clip2 = VideoFileClip(rightfile).subclip(0, 0 + length_R) # 오른쪽 영상

final_clip = clips_array([[clip1,clip2]])
final_clip.resize(width = 480).write_videofile("complete.mp4")