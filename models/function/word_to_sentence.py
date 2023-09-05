def word_to_sentence(filepath, writepath, filename):
    f = open(filepath + filename + '_script.txt')
    text = f.read()
    temp = list(text.split('\n'))
    del temp[-1]

    end_word = ['했다', '이다', '었다', '니다', '한다', '았다', '혔다', '됐다', '졌다',
            '된다', '였다', '하다', '는다', '왔다', '렸다', '났다', '인다', '온다',
            '진다', '냈다']

    words = []
    start_time , end_time = 0, 0
    flag = 0

    text_path = filepath + filename + '_sentence.txt'
    text_file = open(text_path, 'w')

    for data in temp:
        word, _, st, _, et = data.split(' ')
        if start_time == 0:
            start_time = st
        words.append(word)
        end_time = et
        
        
        if len(word) == 1:
            if word in ['요', '까']:
                flag = 1
        else:
            if word[-2:] in end_word or word[-1] in ['요', '까']:
                flag = 1
                
        
        if flag == 1:
            sentence = ' '.join(words)
            
            words = []
            
            flag = 0
            text_file.write('%s'%sentence)
            text_file.write('|%s'%(start_time))
            text_file.write('|%s'%(end_time))
            text_file.write('\n')
            start_time, end_time = 0, 0
    
    text_file.close()        
    f.close()