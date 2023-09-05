import moviepy.editor as mp
from pydub import AudioSegment

filepath = 'video/videoplayback.mp4'

clip = mp.VideoFileClip(filepath)
clip.audio.write_audiofile("audio/audio.wav")

# 스테레오 음원을 모노음원으로 변경
sound = AudioSegment.from_wav('audio/audio.wav')
sound = sound.set_channels(1)
sound.export('audio/audio.wav', format='wav')