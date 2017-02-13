from string import ascii_lowercase as abc
from bs4 import BeautifulSoup
import urllib

pages = []
num = 0
while num < 23000:
    pages.append(num)
    num += 100

url = 'http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&letter={}&start={}'
file = open('divisaosilabica_2.csv', 'w')
file.write('palavra,tipo,sílabas\n')

for letra in abc:
    for p in pages:
        r = urllib.request.urlopen(url.format(letra, p))
        data = r.read()
        soup = BeautifulSoup(data)
        rows = soup.find(id="rollovertable").findAll("tr")
        for row in rows:
            cells = row.findAll("td")
            if cells:
                palavra = cells[0].find('b').find('a').getText()
                tipo = cells[0].getText().split("(")[1].split(")")[0]
                divisaosilabica = cells[1].getText()
                file.write('{},{},{}\n'.format(palavra,
                                               tipo,
                                               divisaosilabica))
                print('{}'.format(palavra))

file.close()
