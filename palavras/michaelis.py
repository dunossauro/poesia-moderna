
#-------------------------------------------------------------------------------

"""
Este script cria uma cópia local do dicionário online Michaelis.

A cópia é criada no mesmo diretório deste script, na forma de um arquivo de
texto chamado "michaelis.txt".
"""

#-------------------------------------------------------------------------------

import time
import os.path
import urllib.parse
import urllib.request
import urllib.error
import html.parser
import string

#-------------------------------------------------------------------------------

def busca_html(url):
    """
    busca_html(url) -> str

    Busca o código html de uma página da web. Em caso de erro no servidor,
    espera 10 segundos e refaz a requisição automaticamente.
    """

    #---------------------------------------------------------------------------

    while True:
        try:
            resposta = urllib.request.urlopen(url)
            break

        except urllib.error.HTTPError as erro:
            pass
            """
            codigo = str(erro.errno)

            if not codigo.startswith('5'):
                print('Problema com a url "%s".' % url)
                raise

            print('Erro %s no servidor.' % codigo)
            print('Refazendo a requisição em:')

            for segundo in range(10, 0, -1):
                print(segundo)
                time.sleep(1)
            """
    codificacao = resposta.headers.get_content_charset()

    pagina = resposta.read()
    pagina = pagina.decode(codificacao)

    return pagina

#-------------------------------------------------------------------------------

class ColetorDeLinks(html.parser.HTMLParser):
    """
    ColetorDeLinks() -> ColetorDeLinks

    Objeto para analisar o código HTML de uma página de índice do Michaelis e
    coletar os links para as páginas de palavra.
    """

    #---------------------------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        """
        handle_starttag(tag, attrs) -> None

        Manipula as tags de abertura.
        """

        #-----------------------------------------------------------------------

        if tag == 'div' and attrs:
            for (attr, val) in attrs:
                if (attr == 'id') and (val == 'idDivWordList'):
                    self.obtendo_links = True

                    return

        elif tag == 'a' and attrs:
            for (attr, val) in attrs:
                if (attr == 'href') and self.obtendo_links:
                    link = urllib.parse.quote(val)
                    self.links.append(link)

                    return

    #---------------------------------------------------------------------------

    def handle_endtag(self, tag):
        """
        handle_endtag(tag) -> None

        Manipula as tags de fechamento.
        """

        #-----------------------------------------------------------------------

        if self.obtendo_links:
            if tag == 'div':
                self.obtendo_links = False

    #---------------------------------------------------------------------------

    def coleta(self, html):
        """
        coleta(html) -> list

        Analisa o código HTML de uma página de índice do Michaelis e coleta os
        links para páginas de palavra.
        """

        #-----------------------------------------------------------------------

        self.links = []
        self.obtendo_links = False

        self.feed(html)

        links = ['http://michaelis.uol.com.br' + link for link in self.links]

        return links

#-------------------------------------------------------------------------------

class ColetorDeDados(html.parser.HTMLParser):
    """
    ColetorDeDados() -> ColetorDeDados

    Objeto para analisar o código HTML de uma página de palavra do Michaelis e
    coletar os dados a serem escritos no arquivo.
    """

    #---------------------------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        """
        handle_starttag(tag, attrs) -> None

        Manipula as tags de abertura.
        """

        #-----------------------------------------------------------------------

        if (tag != 'span') or (not attrs):
            return

        for (attr, val) in attrs:
            if attr == 'class':
                break
        else:
            return

        if val == 'palavra':
            self.lendo_palavra = True

            return

        if val == 'palavraComPontos':
            self.lendo_palavra_com_pontos = True

            return

        if val == 'descricao':
            self.lendo_descricao = True

    #---------------------------------------------------------------------------

    def handle_endtag(self, tag):
        """
        handle_endtag(tag) -> None

        Manipula as tags de fechamento.
        """

        #-----------------------------------------------------------------------

        if tag != 'span':
            return

        if self.lendo_palavra:
            self.lendo_palavra = False

            return

        if self.lendo_palavra_com_pontos:
            self.lendo_palavra_com_pontos = False

            return

        if self.lendo_descricao:
            self.lendo_descricao = False

    #---------------------------------------------------------------------------

    def handle_data(self, data):
        """
        handle_data(data) -> None

        Manipula os dados.
        """

        #-----------------------------------------------------------------------

        if self.lendo_palavra:
            self.palavra += data

            return

        if self.lendo_palavra_com_pontos:
            self.palavra_com_pontos += data

            return

        if self.lendo_descricao:
            self.descricao += data

            return

    #---------------------------------------------------------------------------

    def coleta(self, html):
        """
        coleta(html) -> str

        Analisa o código HTML de uma página de palavra do Michaelis e coleta os
        dados a serem escritos no arquivo. Escreve na saída padrão a palavra que
        está sendo processada para acompanhamento de progresso.
        """

        self.palavra = ''
        self.palavra_com_pontos = ''
        self.descricao = ''

        self.lendo_palavra = False
        self.lendo_palavra_com_pontos = False
        self.lendo_descricao = False

        self.feed(html)

        dados =  'palavra:' + self.palavra.lower() + '\n'
        dados += 'divisão:' + self.palavra_com_pontos.lower() + '\n'
        dados += 'descrição:' + self.descricao.lower() + '\n\n'

        print('processando: "%s"' % self.palavra.lower())

        return dados

#-------------------------------------------------------------------------------

coletor_de_links = ColetorDeLinks()
coletor_de_dados = ColetorDeDados()

base_url_indice = 'http://michaelis.uol.com.br/moderno/portugues/indice/'

diretorio = os.path.dirname(os.path.abspath(__file__))
for caractere in "U":

    arquivo = os.path.join(diretorio, (('%s.txt')%(caractere)))
    arquivo = open(arquivo, 'w')

    for letra in caractere:
        numero = 0

        while True:
            numero += 1

            if numero == 1:
                url = base_url_indice + letra + '.html'
            else:
                url = base_url_indice + letra + '-' + str(numero) + '.html'

            html = busca_html(url)

            links = coletor_de_links.coleta(html)

            if not links:
                break

            for link in links:
                html = busca_html(link)

                dados = coletor_de_dados.coleta(html)

                arquivo.write(dados)
                arquivo.flush()
                #time.sleep(0.5)

    arquivo.close()

    print(('Feito. %s')%(caractere))
