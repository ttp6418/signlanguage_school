import moviepy.editor as mp
import speech_recognition as sr
# from PyKomoran import Komoran, DEFAULT_MODEL
from konlpy.tag import Okt, Komoran

filepath = 'videoplayback.mp4'

clip = mp.VideoFileClip(filepath)
clip.audio.write_audiofile("audio.wav")

# 스테레오 음원을 모노음원으로 변경

from pydub import AudioSegment

sound = AudioSegment.from_wav('audio.wav')
sound = sound.set_channels(1)
sound.export('audio.wav', format='wav')



# r = sr.Recognizer()
# with sr.AudioFile('audio.wav') as source:
#     audio = r.record(source)
    
# vToText = r.recognize_google(audio_data=audio, language='ko-KR')
# print(vToText)
# print('='*30)


# # okt = Okt()
# # print(okt.morphs(vToText))


# komoran = Komoran()
# print(komoran.pos(vToText))


# result = komoran.get_list(vToText)

# print('형태소 분석 결과')
# print(result)
