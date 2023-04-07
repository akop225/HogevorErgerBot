from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re


def remove_notes(s):
    notes = 'Նոտաներ'
    i = 0
    while i < len(s):
        el = s[i]
        #print(el, '---')
        if notes in el:
            s.remove(el)
        i += 1
    return '\n'.join(s).strip()


def remove_nums(s):
    i = 0
    while i < len(s):
        el = s[i].split()
        k = 0
        while k < len(el):
            el2 = el[k]
            if re.search(r'\d\.', el2) and len(el2.strip()) > 2:
                el.remove(el2)
            k += 1
        #print(' '.join(el), '---')
        s[i] = ' '.join(el)
        if re.search(r'\d{2}', s[i]):
            del s[i]
        i += 1
    return '\n'.join(s).strip()


def delete_extra(text):
    s = text.split()
    armenian_pattern = r'[(\u0561-\u0587\u0531-\u0556՛՜)]+'
    for el in s:
        if re.fullmatch(armenian_pattern, el):
            pass
        # if re.fullmatch(r'\d\.', el):
        #     print(el)
        #     print(len(el))
        # print(re.search(r'\(\d+\)', el))
        # if re.search(r'\(\d+\)', el):
        #     print(el)
        #     print(len(el))



i = '63_20'
# Define the URL of the website
url = f'http://www.ergaran.in/2016/01/{i}.html'

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
print(html_content)
div_tags = soup.find_all('div', {'dir': 'ltr', 'trbidi': 'on'})
s = str(div_tags[0])
print(s)
# print(s.split('<br/>'))
armenian_pattern = r"[(\d\.\u0561-\u0587\u0531-\u0556՛՜)]+|<br/>"#'<br/>\d+\.*|[(\u0561-\u0587\u0531-\u0556՛՜)]+|<br/>'
matches = re.findall(armenian_pattern, s)
print(matches)

text_of_song_not_clear = remove_notes(' '.join(matches).replace('<br/>', '\n').strip().split('\n'))
text_of_song = remove_nums(text_of_song_not_clear.split('\n'))
print(text_of_song)
with open(f'songs/{i}.txt', 'w') as f:
    f.write(text_of_song)
