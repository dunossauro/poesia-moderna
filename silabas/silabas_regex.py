import re

r = re.compile("""
(?:[bcdfgpotl][hlr]|[^aiueo])?[aiueo]+
(?:
(?=[bcdfgpotl][hlr])
|
[aeiou][^aeiou]
|
[^aiueo][^aiueo](?=[^aiueo][^aiueo]|[^aiueo])
|
[^aiueo](?=[^aiueo]|\Z)
)?
""", re.X)

texto = "Amor e como eu palmilhasse vagamente chamado uma\
estrada de Minas pedregosa e no fecho da tarde um sino rouco"

for word in texto.split(" "):
    print(r.findall(word))
