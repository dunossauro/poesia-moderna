from sqlite3 import connect
con = connect('pt_base.db')
cur = con.cursor()


def busca(pal):
    res = cur.execute('SELECT sílabas FROM silabas WHERE palavra=?',
                      (pal,))

    for x in res:
        return x


for x in "o governo calmo caia muito".split():
    print(busca(x))


con.close()
