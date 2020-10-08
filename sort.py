import pickle
import time
import markdown
from PyDictionary import PyDictionary

abbr = \
    {
        'n.' : 'Noun',
        'pron.' : 'Pronoun',
        'v.' : 'Verb',
        'adj.' : 'Adjective',
        'adv.' : 'Adverb',
        'prep.' : 'Preposition',
        'conj.' : 'Conjunction',
        'sb.' : 'somebody',
        'sth.' : 'something'
    }

class Word:
    def __init__(self, lst):
        global abbr
        if not isinstance(lst, str):
            raise Exception('input must be a str')
        self.content = ''
        self.part = ''
        for i in lst.split():
            if not i.endswith('.'):
                self.content = i
                break
        for i in lst.split():
            if i.endswith('.') and i in abbr.keys():
                self.part = abbr[i]
                break

    def __eq__(self, other):
        if not isinstance(other, Word):
            return false
        return (self.content == other.content and self.part == other.part)

    def __lt__(self, other):
        if isinstance(other, Word):
            return self.content < other.content
        elif isinstance(other, Phrase):
            return self.content < other.content
        raise Exception()

    def defination(self):
        dictionary = PyDictionary()
        s = ''
        res = None
        st = time.time()
        while True:
            try:
                res = dictionary.meaning(self.content)[self.part]
            except:
                pass
            if isinstance(res, list) or isinstance(res, str):
                break
            if time.time() - st > 60:
                res = ''
                break
        if isinstance(res, str):
            return res + res
        for i in range(len(res)):
            s += ('%d: %s ' % ((i + 1), res[i]))
        return '  ' + s

class Phrase:
    def __init__(self, lst):
        self.content = lst
    
    def __eq__(self, other):
        if not isinstance(other, Phrase):
            return false
        return self.content == other.content

    def __lt__(self, other):
        if isinstance(other, Word):
            return self.content < other.content
        elif isinstance(other, Phrase):
            return self.content < other.content
        raise Exception()
    def defination(self):
        # dictionary = PyDictionary()
        # return dictionary.translate(self.content, 'zh')
        return ''

content = open('word_list.txt', 'r+').read()
output = ''

lst = list(content.split('\n'))
for i in range(len(lst)):
    if len(lst[i]) == 0:
        lst[i : i + 1] = []
    elif list(lst[i].split())[1] in abbr.keys():
        lst[i] = Word(lst[i])
    else:
        lst[i] = Phrase(lst[i])
lst.sort()
pickle.dump(lst, open('data.dat', 'wb'))

for i in range(len(lst)):
    print('now:', lst[i].content, type(lst[i]))
    if i == 0 or lst[i].content[0] != lst[i - 1].content[0]:
        output += '\n%s\n---\n\n' % lst[i].content[0]
    output += '<b>'
    output += lst[i].content
    output += r'</b>'
    if isinstance(lst[i], Phrase):
        output += ' (phrase)'
    if isinstance(lst[i], Word):
        output += (' %s ' % lst[i].part)
    output += lst[i].defination()
    output += '  \n'
    with open('output.html', 'w+', encoding = 'utf-8') as f:
        f.write(markdown.markdown(output))

html_output = markdown.markdown(output)
with open('output.html', 'w+', encoding = 'utf-8') as f:
    f.write(html_output)
