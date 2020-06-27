#%%
def text_to_sentences(text):
    sentences = []
    pointer = 0
    for i,l in enumerate(text):
        if l == '.' or l == '?' or l == '!':
            sentences.append(text[pointer:i+1].strip(' '))
            pointer = i+1
    return sentences
def sentence_length_filter(text):
    sentences = text_to_sentences(text)
    if sentences == []:
        return None
    sentences_len = [len(sen.split(' ')) for sen in sentences]
    mean_len = sum(sentences_len) / len(sentences_len)
    if mean_len >= 3:
        return " ".join(sentences)
    else:
        return None
def remove_repeats(texts):
    def check_len(i,n):
        if i + 25 < n:
            return i + 25
        else:
            return n 
    texts = texts
    n_texts = len(texts)
    # print(len(texts))
    indexes_for_remove = []
    for i in range(len(texts)):
        # print(i)
        if i in indexes_for_remove:
            # print(i)
            continue
        text = texts[i]
        for j in range(i,check_len(i,n_texts)):
            if j == i:
                continue
            if j in indexes_for_remove:
                continue
            if texts[j] in text:
                # print(i,j)
                indexes_for_remove.append(j)
    # print(indexes_for_remove)
    result = []
    for i in range(len(texts)):
        if i not in indexes_for_remove:
            result.append(texts[i])
    f_result = [result[0]]
    for i in range(1,len(result)):
        try:
            result[:i].index(result[i])
        except:
            f_result.append(result[i])       
    return f_result
#%%
def check_text(text):
    data = text
    last_text = ''
    filtered_text = []
    for text in data:
        text = sentence_length_filter(text)
        if text is not None:
            if text not in last_text:
                last_text = text
                if '\n' in text:
                    for i in text.split('\n'):
                        i = i.replace('\xa0', '').replace('\t','')
                        if i.strip() is not '':
                            i = sentence_length_filter(i)
                            if i is not None:
                                filtered_text.append(i)
                else:
                    text = text.replace('\xa0','').replace('\t','')
                    filtered_text.append(text)
    filtered_text = remove_repeats(filtered_text)
    return filtered_text
