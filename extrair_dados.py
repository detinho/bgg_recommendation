import re
import urllib
import sys
import codecs
from bs4 import BeautifulSoup

REXP_LINHAS_NOTAS = re.compile("row_\d+")

class Jogo(object):
    def __init__(self, jogo, nota):
        self.jogo = jogo
        self.nota = float(nota)
    
    def __str__(self):
        return "%s: %d" % (self.jogo, self.nota)

def get_total_jogos(soup):
    regxp_totais = re.compile("\d+ to \d+ of \d+")
    regxp_valores = re.compile("\d+")
    
    totais = soup.find_all("span", {"class": "geekpages"})[0].text
    totais = regxp_totais.findall(totais)[0]
    
    return int(regxp_valores.findall(totais)[-1])

def get_listagem_usuario(usuario, pagina):
    url = "http://www.boardgamegeek.com/collection/user/%s?rated=1&subtype=boardgame&ff=1&pageID=%d" % (usuario, pagina)
    tentativas = 0
    while tentativas < 5:
        try:
            pagina = urllib.urlopen(url)
            return pagina.read()
        except:
            tentativas+=1
    
    return []
    
def get_notas(usuario):
    ret = []
    
    pagina = 1
    total_jogos = None
    while True:
        if total_jogos is not None and len(ret) >= total_jogos:
            break
    
        print "Carregando pagina %d..." % pagina
        html = get_listagem_usuario(usuario, pagina)
        soup = BeautifulSoup(html)
        rows = soup.find_all(id=REXP_LINHAS_NOTAS)
        
        if total_jogos is None:
            total_jogos = get_total_jogos(soup)
        
        if not rows:
            break
    
        for row in rows:
            div_nota = row.findAll("div", {"class": "ratingtext"})
            if (len(div_nota) != 0):
                div_nota = div_nota[0]
                jogo = row.find("a")
                nota = div_nota.text
                
                if (jogo is not None):
                    jogo = jogo["href"]
                    ret.append(Jogo(jogo, nota))
        
        pagina+=1
    
    return ret
    
def get_usuarios_jogo(id_jogo, arq_saida):
    ret = []
    numero_pagina = 1
    
    while True:
        print "Usuarios: pagina %d. Total ate o momento: %d" % (numero_pagina, len(ret))
        url = "http://www.boardgamegeek.com/collection/items/boardgame/%d/page/%d?rated=1" % (id_jogo, numero_pagina)
        pagina = urllib.urlopen(url)
        html = pagina.read()
    
        soup = BeautifulSoup(html)
        usuarios = soup.find_all("div", {"class": "avatarblock js-avatar "})
        if not usuarios:
            break

        for user_div in usuarios:
            user_name = user_div["data-username"]
            ret.append(user_name)
            arq_saida.write(user_name + "\n")
        
        numero_pagina += 1
        
        if len(ret) % 100 == 0:
            arq_saida.flush()
    
def get_notas_usuarios(arq_usuarios, usuario_inicial):
    arq_saida = open("notas.txt", "w")
    importar = False
    if usuario_inicial == "":
        importar = True
        
    for usuario in open(arq_usuarios):
        usuario = usuario.replace("\n", "")
        print "Carregando jogos do usuario %s..." % usuario
        
        if not importar:
            if usuario == usuario_inicial:
                importar = True
        
        if importar:
            jogos = get_notas(usuario)
            for jogo in jogos:
                arq_saida.write("%s;%s;%d\n" % (usuario, jogo.jogo, jogo.nota))
            arq_saida.flush()
        
    arq_saida.close()

if __name__ == "__main__":

    if sys.argv[1] == "teste":
        notas = get_notas("Sorrellbo")
        print notas[0]
        print len(notas)
    elif sys.argv[1] == "usuarios":
        arq_saida = codecs.open("usuarios.txt", "w", "utf-8")
        get_usuarios_jogo(68448, arq_saida)
        get_usuarios_jogo(124742, arq_saida)
        arq_saida.flush()
        arq_saida.close()
    elif sys.argv[1] == "notas":
        usuario_inicial = ""
        if len(sys.argv) > 3:
            usuario_inicial = sys.argv[3]
        get_notas_usuarios(sys.argv[2], usuario_inicial)

