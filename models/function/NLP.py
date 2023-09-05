from konlpy.tag import Komoran
import os
komoran = Komoran(userdic=os.getcwd() + '/models/function/my_dict.txt')

class Morph:
    MORPH = {   # 명사
                'NNG': '명사', 'NNP': '명사', 'NNB': '명사','NF': '명사', 'NP': '명사',
                # 용언
                'VV': '용언', 'VA': '용언', 'VX': '용언', 'VCP': '용언','VCN': '용언', 'NV': '용언', 'XSV': '용언',
                # 관형사
                'MM': '관형사',
                # 부사
                'MAG': '부사', 'MAJ': '부사',
                # 감탄사
                'IC': '감탄사',
                # 조사/
                'JKS': '조사','JKC': '조사', 'JKG': '조사', 'JKO': '조사', 'JKB': '조사', 'JKV': '조사',
                'JKQ': '조사', 'JX': '조사', 'JC': '조사',
                # 어미
                'EP': '어미','EF': '어미','EC': '어미','ETN': '어미','ETM': '어미',
                # 접사
                'XPN': '접사','XSN': '접사','XSA': '접사', 'XR': '접사',
                # 부호
                'SF': '기호','SP': '기호','SS': '기호','SE': '기호','SO': '기호','SW': '기호',
                # 숫자, 수사
                'SN': '숫자', 'NR': '수사',
                # 영어
                'SL': '영어',
                # 한자 제외
                'SH': '없음',
                # 분석 불능 범주 제외
                'NA': '없음'
    }

    # 사용하는 관형사
    USE_DETER = ['저', '맨', '별', '무슨', '헌', '온', '온갖', '그', '동', '오랜', '모든', '그런', '양', '딴', '각', '어떤', '이런',
                 '몹쓸', '약', '옛', '어느', '한', '이러한']

    # 사용하는 조사
    USE_POST = ['랑', '에서', '서', '더러', '보다', '에게', '의', '로', '이라고', '에', '처럼', '께', '으로', '한테', '라고',  '게', '로서', # 격조사
                 '로써', '으로서', '으로써', '만치', '만큼', '보고', '보다', '서부터', '에서부터', '시여', '이시여', '아',# 격조사
                '이나', '든지', '부터', '도', '커녕', '마다', '밖에', '뿐', '만', '까지', '라도', '이라도', '라든지', '거나', '나', '나마', # 보조사
                '이나마', '는', '다가', '대로', '든가', '들', '따라', '라야', '란', '이란','로부터', '마는', '마저', '밖에', '부터', '뿐', # 보조사
                '야말로', '이야말로', '에는', '에다', '에다가', '은',  '이라야', '이야', '조차',# 보조사
                '과', '와', '이랑', '고', '이고', '며', '이며',# 접속조사
                '이니까', '이다', '야'  # 서술격 조사
                ]

    # 사용하는 어미
    USE_END = ['았', '었', 'ㅂ시다', '면서', '자', '지만', '던', '면', '러', '다오', 'ㅂ니까', '다가', '아라', '자',
               '고자', '예요', '고', '을까', '구나', '다면', '으면', '라고', '와', '느라고']

    # 수어사전에 없는 명사 있는 명사로 대체
    SPECIAL_NOUN = {'꺼': '것', '거': '것', '니': '너', '내': '나'}

    # 불규칙 어미
    SPECIAL_END = {'았': '끝', '었': '끝', '으면': '면', '다면': '면', '예요': '이다', '을까': 'ㅂ니까', '다면': '면'}

    # 서술격 조사 '이다'로 변경
    SPECIAL_POST = {'이': '이다'}

    # 불규칙 접사
    SPECIAL_AFFIX = {'스럽': '스럽다', '하': '하다', '어떠한': '어떤', '이러한': '이런', '그러한': '그런'}

    # 수어사전에 없는 부사 있는 부사로 대체
    SPECIAL_ADVERB = {'근데': '그런데', '각각': '각'}

    # 기호
    SPECIAL_MARK = {'?': 'ㅂ니까'}
    
class StopWord:
    def __init__(self):
        self.mp = Morph()

    def process_morph(self, morph, word):
        m = self.mp.MORPH[morph]
        FUN = {
            '명사': self.check_noun,  # 명사(noun)
            '용언': self.check_verb,  # 동사(verb)
            '관형사': self.default,  # 관형사(determinant)
            '부사': self.check_adverb,  # 부사(adverb)
            '감탄사': self.default,  # 감탄사(exclamation)
            '조사': self.ignore,  # 조사(post)
            '어미': self.check_end,  # 어미(end)
            '접사': self.check_affix,  #접사(affix)
            '숫자': self.check_number,  # 숫자(number),
            '수사': self.check_number,
            '기호': self.check_mark,  # 기호,
            '영어': self.ignore,
            '없음': self.ignore  # 무시해도 되는 품사들
        }
        fun = FUN[m]
        return fun(m, word)

    # 무조건 출력
    def default(self, morph, word):
        return 1, word, morph

    # 의미있는 명사 추출
    def check_noun(self, morph, word):
        if word in self.mp.SPECIAL_NOUN.keys():
            return 1, self.mp.SPECIAL_NOUN[word], morph
        else:
            return 1, word, morph

    # 의미있는 동사 추출
    def check_verb(self, morph, word):
        return 1, word+'다', morph

    def check_deter(self, morph, word):
        if word in self.mp.USE_DETER:
            return 1, word, morph
        else:
            return 0, '', ''

    # 의미있는 부사 추출
    def check_adverb(self, morph, word):
        if word in self.mp.SPECIAL_ADVERB.keys():
            return 1, self.mp.SPECIAL_ADVERB[word], morph
        else:
            return 1, word, morph

    # 의미있는 조사 추출
    def check_post(self, morph, word):
        if word in self.mp.USE_POST:
            if word in self.mp.SPECIAL_POST.keys():
                return 1, self.mp.SPECIAL_POST[word], morph
            else:
                return 1, word, morph
        else:
            return 0, '', ''

    # 의미있는 어미 추출
    def check_end(self, morph, word):
        if word in self.mp.USE_END:
            if word in self.mp.SPECIAL_END.keys():
                return 1, self.mp.SPECIAL_END[word], morph
            else:
                return 1, word, morph
        else:
            return 0, '', ''

    # 의미있는 접사 추출
    def check_affix(self, morph, word):
        if word in self.mp.SPECIAL_AFFIX.keys():
            return 1, self.mp.SPECIAL_AFFIX[word], morph
        else:
            return 1, word, morph

    # 숫자 표현(ex. 157 -> 100 50 7)
    def check_number(self, morph, word):
        if morph == '수사':
            return 1, word, morph
        else:
            number = int(word)
            # number의 자릿수
            cipher = len(word)
            text = ''
            for i in range(cipher):
                if word[i] == '0': continue
                text += str(int(word[i]) * (10 ** (cipher - 1 - i)))
                text += ' '
            return 1, text, morph

    # 기호 처리
    def check_mark(self, morph, word):
        if word in self.mp.SPECIAL_MARK.keys():
            return 1, self.mp.SPECIAL_MARK[word], morph
        else:
            return 0, '', ''

    # 무조건 제거
    def ignore(self, morph, word):
        return 0, '', ''
    
# 자막파일을 입력받아 수어에 사용되는 형태소를 재배치하는 함수를 가진 객체
class NLP:
    def __init__(self):
        self.komoran = komoran
        self.pr = StopWord()
        pass

    def splitLine(self, line):
        for i in range(len(line)):
            s = str(line[i])
#             print(s)
            s = s.replace('(', '')
            s = s.replace(')', '')
            s = s.replace("'", '')
            s = s.replace(" ", '')
#             print(s)
            s = s.split(',')
#             print(s)
            line[i] = s
#         print(line)
        return line

    # 수어에 사용되는 형태소를 재배치하는 함수
    def relocateMorpheme(self, subtitle_path):
        result=[]
        word_list=[]
        morph_list=[]

        line = self.komoran.pos(subtitle_path)
        line = self.splitLine(line)
        for w, m in line:
            r, word, morph = self.pr.process_morph(m, w)
            if r == 1:
                if (word == 'ㅂ니까') or (word == '하다') or (word == '끝'):
                    if len(result) == 0:
                        word_list.append(word)
                        morph_list.append(morph)
                    elif result[len(result) - 1][0] != word:
                        word_list.append(word)
                        morph_list.append(morph)
                else:
                    word_list.append(word)
                    morph_list.append(morph)
        result.append(word_list)
        result.append(morph_list)
        return result[0], result[1]