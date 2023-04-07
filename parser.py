import time
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import re

exceptions = {
    62: '63_20',
    94: '094',
    95: '095',
    96: '096',
}


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
        el = s[i].split()
        k = 0
        while k < len(el):
            el2 = el[k]
            if re.search(r'\d\.', el2) and len(el2.strip()) > 2:
                el.remove(el2)
            k += 1
        # print(' '.join(el), '---')
        s[i] = ' '.join(el)
        if re.search(r'\d{2}', s[i]):
            del s[i]
        i += 1
    return '\n'.join(s).strip()


for i in range(100, 661):
    # Define the URL of the website
    url = f'http://www.ergaran.in/2016/01/{i}.html'

    if i in exceptions:
        url = f'http://www.ergaran.in/2016/01/{exceptions[i]}.html'

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(html_content)
    div_tags = soup.find_all('div', {'dir': 'ltr', 'trbidi': 'on'})
    #print(div_tags)
    s = str(div_tags[0])
    # print(s)
    armenian_pattern = r"[(\d\.\u0561-\u0587\u0531-\u0556՛՜)]+|<br/>"
    matches = re.findall(armenian_pattern, s)
    # print(matches)

    text_of_song_not_clear = remove_notes(' '.join(matches).replace('<br/>', '\n').strip().split('\n'))
    text_of_song = remove_nums(text_of_song_not_clear.split('\n'))
    with open(f'songs/{i}.txt', 'w') as f:
        f.write(text_of_song)
    print('SUCCESSFULLY -', i)
    print(text_of_song)
    print('-----' * 10)
    time.sleep(1)

