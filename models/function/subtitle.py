import datetime
import os
import pandas as pd

def make_srt_format(writepath, filename):
    f=open(writepath+filename+'_sentence.txt')
    text = f.read()
    temp = text.split('\n')
    del temp[-1]
    f.close()

    sub_df = pd.DataFrame(columns=['sentence', 'start_time', 'end_time'])
    for i in range(len(temp)):
        data = temp[i].split('|')
        sub_df.loc[i] = data

    sub_df['start_time'] = ['0'+str(datetime.timedelta(seconds=float(i))) for i in sub_df['start_time']]
    sub_df['end_time'] = ['0'+str(datetime.timedelta(seconds=float(i))) for i in sub_df['end_time']]

    sub_df['start_time'] = pd.to_datetime(sub_df['start_time']).dt.strftime('%H:%M:%S,%f').str[:-3]
    sub_df['end_time'] = pd.to_datetime(sub_df['end_time']).dt.strftime('%H:%M:%S,%f').str[:-3]

    sub_df['seq_num'] = [str(i) for i in list(range(1, len(sub_df)+1))]

    sub_df['srt_time'] = sub_df['start_time'] + ' --> ' + sub_df['end_time']
    sub_df['srt'] = sub_df['seq_num'] + '\n' + sub_df['srt_time'] + '\n' + sub_df['sentence'] + '\n\n'

    srt = sub_df.srt.copy()
    
    srt_path = writepath + filename + '_subtitle.srt'
    srt.to_csv(srt_path, header=None, mode='w', index=False)

 
    with open(srt_path, 'r', encoding='utf-8') as file:
         filedata = file.read()
         
    filedata = filedata.replace('"','')
    
    with open(srt_path, 'w', encoding='utf-8')as file:
        file.write(filedata)
        
    return 'mysite/static/request/' + filename + '_subtitle.srt'