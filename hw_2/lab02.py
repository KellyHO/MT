
# coding: utf-8

# In[1]:


from collections import defaultdict, Counter
import kenlm
import re
from math import log


# In[2]:


def prepro_edit(text):
    before_text = []
    after_text = []
    for token in text.split():
        if '>>' in token:
            before_text.append(' '.join(pure_word.findall(token.split('>>')[0])))
            after_text.append(' '.join(pure_word.findall(token.split('>>')[1])))
                
        elif token.startswith('[-'):
            before_text.append(' '.join(pure_word.findall(token)))
        elif token.startswith('{+'):
            after_text.append(' '.join(pure_word.findall(token)))
        else:
            before_text.append(token)
            after_text.append(token)
#             print(token)
    return before_text, after_text


# In[3]:


def count_edit(edit_dict, edit_text):
    for line in edit_text:
        count, edit_text = line.strip().split(' ',1)
    #     print(edit_text)
        before_text, after_text = prepro_edit(edit_text)
    #     print(' '.join(before_text), "|||", ' '.join(after_text), count)

        before_text = ' '.join(before_text)
        after_text = ' '.join(after_text)

        fir_score = KnModel.score(before_text, bos = False, eos = False)
        sec_score = KnModel.score(after_text, bos = False, eos = False)
        if fir_score > sec_score:
            count = int(count) * 0.5
            edit_dict[after_text][after_text] += count

        edit_dict[before_text][after_text] += int(count)
        
    return edit_dict
        
    
    


# In[4]:


def count_no_edit(edit_dict, no_edit_text):
    for line in no_edit_text:
        count, edit_text = line.strip().split(' ',1)
        edit_dict[edit_text][edit_text] += int(count)
        
    return edit_dict


# In[6]:


def show_result(edit_dict):
    
    for fir_k, item in edit_dict.items():
        total_fir_k = sum(item.values())
        for sec_k, count in item.items():

            if count == 0:
                pass
            else:
                print(fir_k, '|||' ,sec_k, '|||', log(count/total_fir_k))


# In[8]:


# ! python3 gen.ngram.no.edit.py ef.diff.simple.simple.txt | sort | uniq -c > ef_no_edit.txt
# ! python3 gen.ngram.edit.py ef.diff.simple.simple.txt | sort | uniq -c > ef_edit.txt

KnModel = kenlm.Model('../jjc/1b.bin')
pure_word = re.compile(r'\w+')

edit_text = open('./ef_edit.txt', 'r').readlines()
no_edit_text = open('./ef_no_edit.txt', 'r').readlines()

edit_dict = defaultdict(lambda: Counter())
edit_dict = count_no_edit(edit_dict, no_edit_text)
edit_dict = count_edit(edit_dict, edit_text)

show_result(edit_dict)


