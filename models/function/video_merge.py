import os
import urllib.request
import glob
from moviepy.editor import VideoFileClip, concatenate_videoclips
import shutil
import re
import cv2
from moviepy.video.io.ffmpeg_tools import *
from moviepy.video.fx.crop import *
from moviepy.editor import *
import shutil

def save_signlanguage_video(href,name, num):  #일치하는 수화영상을 크롭하여 저장
    output_location = os.getcwd() + f'/models/function/word/word{num}/' + 'word_'+str(name)+ '.mp4'
    try: clip = VideoFileClip(href)
    except: clip = VideoFileClip(href)
    if clip.duration > 3: clip = clip.subclip(1,3).resize((560,360))    #수화영상의 1~3초만 잘라냄 > 크기 조절
    else: clip = clip.subclip(1, clip.duration).resize((560,360))

    new_clip = crop(clip, x1=70, y1=0, x2=490, y2=270)   #가슴까지 보이도록 crop
    new_clip.write_videofile(output_location)

    return output_location

def speedx(file_list,n, ans):   # 수화영상들을 병합해서 배속
    clip_list = []
    for i in file_list:
        clip_list.append(VideoFileClip(i))
    final_clip = concatenate_videoclips(clip_list)
    print("final: ", final_clip.duration)
#     t=ans[n][2]/final_clip.duration
    t=round(final_clip.duration/ans[n][2],1)

    print("비율 : ", t)
    final_clip.speedx(t).write_videofile(os.getcwd() + f"/models/function/sentence/sentence_{n}.mp4")
    

def merge_video(link, ans, filepath, writepath, filename):
    try: shutil.rmtree(os.getcwd() + "/models/function/word/")
    except: pass
    try: shutil.rmtree(os.getcwd() + "/models/function/sentence/")
    except: pass
    num = 0 # 줄 몇갠지
    output_path = writepath + filename + "_output.mp4"
    for i in link:
        n=0   # 한 줄안에 들어갈 영상 몇갠지
        try: os.mkdir(os.getcwd() + "/models/function/word/")
        except: pass
        try: os.mkdir(os.getcwd() + f"/models/function/word/word{num}")
        except: pass
        try: os.mkdir(os.getcwd() + "/models/function/sentence")
        except: pass
        for j in i:
            href =j
            save_signlanguage_video(href, n, num)
            n+=1
        file_list = sorted(glob.glob(os.getcwd() + f'/models/function/word/word{num}/*.mp4'),key=os.path.getctime)
        
        print(file_list)
        speedx(file_list, num, ans)    
        num+=1
        
    file_tot_list = sorted(glob.glob(os.getcwd() + '/models/function/sentence/*.mp4'), key=os.path.getctime)
    clip_tot_list = []

    for i in file_tot_list:
        clip_tot_list.append(VideoFileClip(i))
        
    final_tot_clip = concatenate_videoclips(clip_tot_list)
    final_tot_clip.write_videofile(output_path)    

    #####
    # 강의 영상, 수어 영상 매핑
    #####
    
    length_L = get_duration(filepath + filename + '_original.mp4')  # 강의 영상 길이
    length_R = get_duration(filepath + filename + '_output.mp4') # 수어 영상 길이 반환

    clip1 = VideoFileClip(filepath + filename + '_original.mp4').subclip(0, 0 + length_L).margin(2) # 왼쪽 영상 
    clip2 = VideoFileClip(filepath + filename + '_output.mp4').subclip(0, 0 + length_R) # 오른쪽 영상

    final_clip = clips_array([[clip1,clip2]])
    final_clip.write_videofile(writepath+filename+'_merge.mp4', threads=8, fps=60)
    
    temp = os.path.dirname(os.path.realpath(__file__))
    
    
    return 'mysite/static/request/' + filename + '_merge.mp4'

def get_duration(filename): #영상 길이 반환 함수
    clip = VideoFileClip(filename)
    return clip.duration
    
# leftfile = "video/hand.mp4"  # 왼손코딩 강의 영상 
# rightfile = "video/u2net_test.mp4" # 왼손코딩 강의를 수어로 번역한 영상