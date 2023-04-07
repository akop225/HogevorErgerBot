from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re


def remove_notes(s):
    notes = 'Նոտաներ'
    i = 0
    while i < len(s):
        el = s[i]
        # print(el, '---')
        if notes in el:
            s.remove(el)
        i += 1
    return '\n'.join(s).strip()


def remove_nums(s):
    i = 0
    while i < len(s):
        el = s[i]
        if re.search(r'\d', el) and not (re.search(r'\d\.', el) or re.search(r'\.', el)):
            s.remove(el)
        i += 1
    return '\n'.join(s).strip()



i = 104
# Define the URL of the website
url = f'http://www.ergaran.in/2016/01/{i}.html'

# Send a GET request to the URL and get the HTML content
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')
# print(html_content)
div_tags = soup.find_all('div', {'dir': 'ltr', 'trbidi': 'on'})
print(div_tags)
s = str(div_tags[0])

armenian_pattern = r"[(\d\.\u0561-\u0587\u0531-\u0556՛՜՜)]+|<br/>"#'<br/>\d+\.*|[(\u0561-\u0587\u0531-\u0556՛՜)]+|<br/>'
matches = re.findall(armenian_pattern, s)
print(matches)

text_of_song_not_clear = remove_notes(' '.join(matches).replace('<br/>', '\n').strip().split('\n'))
print(text_of_song_not_clear)
text_of_song = remove_nums(text_of_song_not_clear.split('\n'))
if text_of_song.find('1.') != -1:
    k = list(text_of_song)
    k.insert(text_of_song.find('1.'), '\n')
    text_of_song = ''.join(k)
    print('YES')
with open(f'songs/{i}.txt', 'w') as f:
    print(text_of_song)
    f.write(text_of_song)
