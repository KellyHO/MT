import sys, nltk

problem_words = [ line.strip() for line in open('ldoce.problem.words.nvar.txt') ]

lm = nltk.WordNetLemmatizer()

def lemma(word):
    for pos in 'nvar':
        res = lm.lemmatize(word, pos)
        if res != word: return res
    return word
    
def with_problem_words(words):
    for word in words:
        if word in problem_words:
            return True
        if lemma(word) in problem_words:
            return True
    return False
    
def with_edit(words):
    for word in words:
        if (word.startswith('[') or word.startswith('{')) and (word.endswith(']') or word.endswith('}')): # and len(word) > 1:
            return True
    return False

    words = ' '.join(words)
    return ('-' in words or '+' in words)
    
def list_to_ngram(words, n, m, condition):
    return [words[i:i+k] for k in range(n, m+1) for i in range(len(words)-k) 
                if condition(words[i:i+n]) and with_problem_words(words[i:i+n]) ]

if __name__ == '__main__':
    
    for line in sys.stdin:
        #for ngram in list_to_ngram(line.strip().split(), 2, 4, lambda x: True):
        for ngram in list_to_ngram(line.strip().split(), 1, 4, lambda x: not with_edit(x)):
            print (' '.join(ngram))

    # time cat ef.diff.simple.txt | grep discuss | python gen.ngram.edit.py | sort | uniq -c | sort -k1nr | head -40

        

