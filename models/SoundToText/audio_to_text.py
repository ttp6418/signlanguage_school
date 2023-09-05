import io
import os

from google.cloud import speech, storage

# google api credentials 경로 환경변수 설정부분
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r"C:\Users\User\Desktop\googleSTTkey\bigprojstt-2775effac8a3.json"


def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))


def transcribe_gcs(gcs_uri, language):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    ## 버킷 gcs_uri 활용 번역 기능 함수, timestamp 미출력
    
    from google.cloud import speech

    client = speech.SpeechClient()
    
    # 입력 영상 인코딩 방식, 샘플링 개수 맞춰줄것
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code=language,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u"Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))


        for trans in result.alternatives[0].words:
            word = trans.word
            start_time = trans.start_time
            end_time = trans.end_time
            
            text_file.write('%s '%word)
            text_file.write('start_time %s '%(start_time.seconds + start_time.nanos * 1e-9))
            text_file.write('end_time %s'%(end_time.seconds + end_time.nanos * 1e-9))
            text_file.write('\n')
            print('Word: {}, start_time: {}, end_time: {}'.format(
                    word,
                    start_time.seconds + start_time.nanos * 1e-9,
                    end_time.seconds + end_time.nanos * 1e-9))
            
            
def transcribe_gcs_with_word_time_offsets(gcs_uri, language):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    ## 버킷 gcs_uri 활용 번역 기능 함수, timestamp 출력 가능
    
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    
    # 입력 영상 인코딩 방식, 샘플링 개수 맞춰줄것
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code=language,
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    result = operation.result(timeout=90)

    for result in result.results:
        alternative = result.alternatives[0]
        print("Transcript: {}".format(alternative.transcript))
        print("Confidence: {}".format(alternative.confidence))

        
        # 단어, 시작시간, 종료 시간 textfile 기록
        # 정보 별 공백 기준 분할, 문장 별 \n 기준 분할
        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            text_file.write('%s '%word)
            text_file.write('start_time %s '%(start_time.total_seconds()))
            text_file.write('end_time %s'%(end_time.total_seconds()))
            text_file.write('\n')
            
            # print(
            #     f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            # )            
            
            
            
## 저장소에 파일 업로드부분
storage_client = storage.Client()
bucket = storage_client.bucket('bigproj_stt_bucket')
blob = bucket.blob('temp1')

# 음원 추출 경로
speech_file = "audio/audio.wav"
blob.upload_from_filename(speech_file)


gsc_uri = 'gs://bigproj_stt_bucket/temp1' # 클라우드 버킷 설정 경로

text_path = 'text/script.txt'
text_file = open(text_path, 'w')

transcribe_gcs_with_word_time_offsets(gsc_uri, 'ko-KR')

