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
    704: '705',
    705: '705_21',
    712: '713',
    713: '713_21',
    734: '733_23',
    751: '752',
    752: '752_24',
    909: '910',
    910: '910_30',
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
        el = s[i]
        if re.search(r'\d', el) and not (re.search(r'\d\.', el) or re.search(r'\.', el) or re.search(r'\(\d\)', el)):
            s.remove(el)
        i += 1
    return '\n'.join(s).strip()


for i in range(243, 661):
    # Define the URL of the website
    if 1 <= i <= 660:
        url = f'http://www.ergaran.in/2016/01/{i}.html'
    elif 661 <= i <= 940:
        url = f'http://www.ergaran.in/2018/07/{i}.html'
    elif 941 <= i <= 1000:
        url = f'http://www.ergaran.in/2018/08/{i}.html'

    if i in exceptions:
        if 1 <= i <= 660:
            url = f'http://www.ergaran.in/2016/01/{exceptions[i]}.html'
        elif 661 <= i <= 940:
            url = f'http://www.ergaran.in/2018/07/{exceptions[i]}.html'
        elif 941 <= i <= 1000:
            url = f'http://www.ergaran.in/2018/08/{exceptions[i]}.html'

    # Send a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    # print(html_content)
    div_tags = soup.find_all('div', {'dir': 'ltr', 'trbidi': 'on'})
    #print(div_tags)
    s = str(div_tags[0])
    # print(s)
    armenian_pattern = r"[(\d\.\u0561-\u0587\u0531-\u0556՛՜՞)]+|<br/>"
    matches = re.findall(armenian_pattern, s)
    # print(matches)

    text_of_song_not_clear = remove_notes(' '.join(matches).replace('<br/>', '\n').strip().split('\n'))
    text_of_song = remove_nums(text_of_song_not_clear.split('\n'))
    if text_of_song.find('1.') != -1:
        k = list(text_of_song)
        k.insert(text_of_song.find('1.'), '\n')
        text_of_song = ''.join(k)

    with open(f'songs/{i}.txt', 'w') as f:
        f.write(text_of_song)
    print('SUCCESSFULLY -', i)
    print(text_of_song)
    print('-----' * 10)
    # time.sleep(1)

