from models.function.NLP import *
import pandas as pd

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = ['','ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']


def load_sentence(filepath, writepath, filename):
    
    ####
    # NLP 처리부분
    ####
    f=open(filepath + filename + '_sentence.txt')   #문장조합
    text = f.read()
    temp=list(text.split('\n'))
    del temp[-1]

    nlp=NLP()
    ans=[]    #l을 담을 전체 리스트
    l=[]   #각 문장의 단어, 형태소, 첫, 끝시간 포함 리스트
    for data in temp:
        word, st, et = data.split('|')
        l=list(nlp.relocateMorpheme(word))
        l.append(float(et)-float(st))
    #     l.append(round(float(et)-float(st),1))
    #     l.append(st)
    #     l.append(et)
        ans.append(l)
    f.close()
    
    return ans
    
    
    
def word_process(ans):
    
    ####
    # 띄어쓰기 제거, 숫자 처리 부분
    ####
    
    words_list=[]  #단어
    gram_list=[]  #품사
    for i in range(len(ans)):
        words=[]
        for j in ans[i][0]:
            aa=j.replace(" ","")   #'5 '이렇게 띄어쓰기가 존재하여 빈칸을 제거해줌 -> '5' 이렇게 되도록 만듦
            words.append(aa)
        words_list.append(words)
        gram_list.append(ans[i][1])   

    num_list=[]   #'숫자' index 넣을 공간
    a=0  #행
    for i in gram_list:
        b=0   #열
        for j in i:
            if j=='숫자':
                num_list.append([a,b])
            b+=1
        a+=1
    
    words_list_new=[]
    for i in range(len(words_list)):
        words_new=[]
        for j in range(len(words_list[i])):
            if [i,j] in num_list:                                       #숫자이면
                number = []
                number.extend(words_list[i][j])
                while number:
                    num = number.pop(0)
                    if num=='0':
                        continue
                    elif len(number) == 4:
                        words_new.append(num)
                        words_new.append('10000')
                    elif len(number) == 3:
                        words_new.append(num)
                        words_new.append('1000')
                    elif len(number) == 2:
                        words_new.append(num)
                        words_new.append('100')
                    elif len(number) == 1:
                        words_new.append(num)
                        words_new.append('10')
                    elif len(number) == 0:
                        words_new.append(num)
            else:                                                       #숫자아니면
                    words_new.append(words_list[i][j])
        words_list_new.append(words_new)
        
    words_list_new2=[]

    highlev_language = ["자바","Java","java","JS",
                    "javascript","python","Python",
                    "파이선","파이썬","시언어","씨언어",
                    "C언어","C++","씨쁠쁠","시쁠쁠",
                    "파스칼","자연어","장고","django"]

    library_language = ["API","opencv","Opencv",
                        "오픈씨브이","cv2","numpy",
                        "pandas","seaborn","sklearn",]

    module_language = ["함수","클래스","class","function",
                    "사용자함수"]

    command_language = ["pip","install","if",
                        "for","input","as","from"]

    for i in words_list_new:
        l=[]
        for j in i:
            if j in highlev_language:
                j='고수준언어'
            elif j in library_language:
                j='라이브러리'
            elif j in module_language:
                j='모듈'
            elif j in command_language:
                j='명령'
            l.append(j)
        words_list_new2.append(l) 
        
    return words_list_new2
        

def devidePhon(korean_word):
    r_lst = []
    for w in list(korean_word.strip()):
        ## 영어인 경우 구분해서 작성함.
        if '가' <= w <= '힣':
            ## 588개 마다 초성이 바뀜.
            ch1 = (ord(w) - ord('가')) // 588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588 * ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588 * ch1) - 28 * ch2
            r_lst.append(CHOSUNG_LIST[ch1])
            r_lst.append(JUNGSUNG_LIST[ch2])
            r_lst.append(JONGSUNG_LIST[ch3])

        else:
            r_lst.append([w])
            
    for i in r_lst:    #종성에 ''있는것 제거하고자 내가 걍 추가해줌
        if i=='':
            r_lst.remove(i)
            
    return r_lst



def mapping(words_list_new):
    import os

    df= pd.read_csv(os.getcwd() + '/models/function/crawling/data_crawl_ver3.csv')

    ## 단어 유사도 측정
    from difflib import get_close_matches
    words = df['kor']
    # url=df['url']
    url = df['video_link']

    link= []
    for i in words_list_new:
        u=[]   #url담을 공간
        close = []    #단어 담을 공간
        for j in i:
            word=j
            candidates=words
            n=1  #최대 문자 매칭 개수 
            cutoff=0.5  #유사도 하한
            close_matches = get_close_matches(word, candidates, n, cutoff)  #유사한것이 매칭된 리스트  (빈것도 포함되어있음)
    #         print(close_matches)
            
            if not close_matches:       #빈것이 있다면 지화수어로 변경해 close 리스트에 담기 
                none=devidePhon(j)
                for no in none:
                    close.append(no)
            else:                       #매칭되는게 있다면 그대로 close 리스트에 담기 
                close.append(close_matches.pop(0))
                    
        for k in close:
            ind=df.index[df['kor'] == k].tolist()
    #             print(ind)
            indd=ind[0]  #동음의의어 있어서 일단 젤 앞에 있는 숫자 추출하도록
            href=url[indd]
            u.append(os.getcwd() + '/videos/' + href)

        link.append(u)
        
    return link