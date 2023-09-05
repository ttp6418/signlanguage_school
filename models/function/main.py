from models.function.video_to_audio import video_to_audio
from models.function.audio_to_text import audio_to_text
from models.function.word_to_sentence import word_to_sentence
from models.function.youtube_video import youtube_video
from models.function.mapping import *
from models.function.video_merge import merge_video
from models.function.subtitle import make_srt_format
import subprocess

# filepath = 'video/opencv_0.mp4'
# url = 'https://www.youtube.com/watch?v=qYOk-d9bIBs&list=PLuHgQVnccGMDtnr4nTSFfmocHL5FeH1xR&index=2'
# url = 'https://www.youtube.com/watch?v=DzNYhZIdsOo'


def video_source_function(filepath, writepath, filename):
    # filepath = 'video/videoplayback.mp4'
    video_to_audio(filepath, writepath, filename)
    audio_to_text(filepath, writepath, filename)
    word_to_sentence(filepath, writepath, filename)
    ans = load_sentence(filepath, writepath, filename)
    words_list_new = word_process(ans)
    link = mapping(words_list_new)
    video_path = merge_video(link, ans, filepath, writepath, filename)
    srt_path = make_srt_format(writepath, filename)
    
    final_path = writepath + filename + '_complete.mp4'
    command_ = f'ffmpeg -i {video_path} -vf subtitles={srt_path} {final_path}'
    
    subprocess.call(command_)
    # os.system("ffmpeg -i " + video_path + " -vf subtitles=" + srt_path + " " + final_path)
    
def youtube_source_function(url, writepath, filename):
    filepath = youtube_video(url, writepath, filename)
    video_to_audio(filepath, writepath, filename)
    audio_to_text(filepath, writepath, filename)
    word_to_sentence(filepath, writepath, filename)
    ans = load_sentence(filepath, writepath, filename)
    words_list_new = word_process(ans)
    link = mapping(words_list_new)
    video_path = merge_video(link, ans, filepath, writepath, filename)
    srt_path = make_srt_format(writepath, filename)
    
    final_path = 'mysite/static/request/' + filename + '_complete.mp4'
    command_ = f'ffmpeg -i {video_path} -vf subtitles={srt_path} {final_path}'
    # # os.system(command_)
    # os.system("ffmpeg -i " + video_path + " -vf subtitles=" + srt_path + " " + final_path)
    subprocess.call(command_)
    
# url = 'https://www.youtube.com/watch?v=9RS6xUNAFTk'

# youtube_source_function(url)

