from string import ascii_lowercase as abc

from bs4 import BeautifulSoup
import urllib

url = 'http://www.portaldalinguaportuguesa.org/index.php?action=syllables&act=list&letter='

for letra in abc:
    r = urllib.request.urlopen(url + letra)
    data = r.read()
    soup = BeautifulSoup(data)
    rows = soup.find(id="rollovertable").findAll("tr")
    for row in rows:
        cells = row.findAll("td")
        if cells:
            with open('divisaosilabica.csv', 'a') as file:
                palavra = cells[0].find('b').find('a').getText()
                tipo = cells[0].getText().split("(")[1].split(")")[0]
                divisaosilabica = cells[1].getText()
                file.write('{},{},{}'.format(palavra, tipo, divisaosilabica))
