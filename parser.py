from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re


def remove_notes(s):
    notes = 'Նոտաներ'
    i = 0
    while i < len(s):
        el = s[i]
        if notes in el:
            s.remove(el)
        i += 1
    return '\n'.join(s).strip()


def remove_nums(s):
    i = 0
    while i < len(s):
        el = s[i]
        if re.search(r'\d', el) and not re.search(r'\d\.', el) or re.search(r'\.', el) and not re.search(r'\d\.', el):
            s.remove(el)
        i += 1
    return '\n'.join(s).strip()


for i in range(62, 661):
    # Define the URL of the website
    url = f'http://www.ergaran.in/2016/01/{i}.html'

    if i == 62:
        url = f'http://www.ergaran.in/2016/01/63_20.html'

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(html_content)
    div_tags = soup.find_all('div', {'dir': 'ltr', 'trbidi': 'on'})
    s = str(div_tags[0])

    armenian_pattern = r'[ (\d.\u0561-\u0587\u0531-\u0556՛՜)]+|<br/>'
    matches = re.findall(armenian_pattern, s)

    text_of_song_not_clear = remove_notes(' '.join(matches).replace('<br/>', '\n').strip().split('\n'))
    text_of_song = remove_nums(text_of_song_not_clear.split('\n'))
    with open(f'songs/{i}.txt', 'w') as f:
        f.write(text_of_song)
