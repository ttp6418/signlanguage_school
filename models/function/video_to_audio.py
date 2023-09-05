import moviepy.editor as mp
from pydub import AudioSegment

# default filepath
# filepath = 'video/opencv_0.mp4'

def video_to_audio(filepath, writepath, filename):
    clip = mp.VideoFileClip(filepath + filename + '_original.mp4')
    clip.audio.write_audiofile(writepath + filename + ".wav")

    # 스테레오 음원을 모노음원으로 변경
    sound = AudioSegment.from_wav(writepath + filename + '.wav')
    sound = sound.set_channels(1)
    sound.export(writepath + filename + '.wav', format='wav')