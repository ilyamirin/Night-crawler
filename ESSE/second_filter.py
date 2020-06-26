import re
#%%

MAX_WORDS = 280
MIN_WORDS = 150
MIN_OCC = 3

#%%
def words_occur(text,cliches):
    text = text.lower()
    line = "|".join(cliches)
    pattern = re.compile(line)
    enters = len(re.findall(pattern,text))
    return enters

def opinion_part_filter(text,main): 
    for c in main:
        if c in text[:2* len(text) // 3].lower():
            return True
        else:
            continue
    return False

def conclusion_filter(text,conclusion):
    #Фильтр заключению. Необходимо наличие клише в конце текста, но не в начале
    for c in conclusion:
        if c in text[:len(text) // 2].lower():
            return False
        if c in text[-len(text) // 3:].lower():
            return True
        else:
            continue
    return False

def words_filter(texts,cliches,conclusion,main):
    filtered_texts = []
    def get_text(indexes, texts):
        text = ''
        for i in indexes:
            text += texts[i]
        return text
    current_text_ind = []
    i = 0
    ind = 0
    while i < 100000:
        i += 1
        current_text_ind.append(ind)
        ind += 1
        try:
            text = get_text(current_text_ind, texts)
        except:
            break # выход индекса за предел длины списка
        words_num = len(text.split(' '))
        if words_num > MAX_WORDS:
            ind = current_text_ind[0] + 1
            current_text_ind = []
            continue
        elif words_num < MIN_WORDS:
            continue
        else:
            occur = words_occur(text,cliches)
            if occur > MIN_OCC: # Текст прошёл фильтрацию на количество слов
                if opinion_part_filter(text,main) and conclusion_filter(text, conclusion):
                    filtered_texts.append(text)
                    ind = current_text_ind[-1] + 1
                    current_text_ind = []
                continue
            else:
                continue
    if filtered_texts != []:
        return filtered_texts
    else:
        return None

def repetition_delete(texts):
    last = ''
    new_texts = []
    for name,link,text in texts:
        if last.endswith(text):
            continue
        else:
            new_texts.append((name,link,text))
        last = text
    return new_texts
#%%
with open('data/cliches.txt', 'r') as file:
    cliches = file.read().split('\n')
while True:
    try:
        cliches.remove('')
    except:
        break
with open('data/conclusion_cliches.txt', 'r') as file:
    conclusion = file.read().split('\n')
while True:
    try:
        conclusion.remove('')
    except:
        break
with open('data/opinion_cliches.txt', 'r') as file:
    opinion_cliches = file.read().split('\n')
while True:
    try:
        conclusion.remove('')
    except:
        break

def filter_one(text, cliches = cliches, conclusion = conclusion, opinion_cliches = opinion_cliches):
    return words_filter(text,cliches,conclusion,opinion_cliches)
