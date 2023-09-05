from pytube import YouTube

# url = 'https://www.youtube.com/watch?v=-3DHpwy498o&list=PLuHgQVnccGMDtnr4nTSFfmocHL5FeH1xR'

def youtube_video(url, writepath, filename):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(writepath, filename + '_original.mp4')
    
    return writepath