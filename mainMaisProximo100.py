import math
import sys
import svgwrite
import random as r
from svgwrite import mm
from Cidades import Cidades
from Caxeiro import Caxeiro

arq = open("ncit100.dat", 'r')
lines = arq.readlines()
quantCidades = int(lines[0])
cidades = []
quantCaxeiros = int(sys.argv[1])


def adicionarCidades():
    for i in range(quantCidades):
        localizacao = lines[i + 1].split('  ')
        x = int(localizacao[0])
        y = int(localizacao[1])
        cidade = Cidades('Cidade' + str(i), x, y)
        cidades.append(cidade)


def mostrarTodasDistancias():
    for i in cidades:
        i.mostrarDistancia()
        print()


def euclidiana(cidade1, cidade2):
    x = pow(cidade1.x - cidade2.x, 2)
    y = pow(cidade1.y - cidade2.y, 2)
    distancia = math.sqrt(x + y)
    cidade1.adicionarDistancia(cidade2, distancia)


def calcularDistancia():
    for i in cidades:
        for j in cidades:
            euclidiana(i, j)


def verificaCusto(vetor):
    i = 0
    custo = 0
    while len(vetor) - 1 > i:
        dist = vetor[i].retornaDistancia(vetor[i + 1])
        custo += dist
        i += 1
    return custo


def corAleatoria():
    hexadecimal = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    cor_aleatoria = "#"
    for i in range(6):
        posarray = r.randint(0, len(hexadecimal) - 1)
        cor_aleatoria += hexadecimal[posarray]
    print(cor_aleatoria)
    return cor_aleatoria


def two_opt(route):
    best = route
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1: continue  # changes nothing, skip then
                new_route = route[:]
                new_route[i:j] = route[j - 1:i - 1:-1]  # this is the 2woptSwap
                if verificaCusto(new_route) < verificaCusto(best):  # what should cost be?
                    best = new_route
                    improved = True
        route = best
    return best


def basic_shapes(nome, vetor, dwg, posi, custo):
    cor = corAleatoria()
    hlines = dwg.add(dwg.g(id='hlines', stroke=cor))
    shapes = dwg.add(dwg.g(id='shapes', fill='red'))
    i = 0
    while i < len(vetor) -1:
        hlines.add(dwg.line(start=((vetor[i].x/10) * mm, (vetor[i].y/10) * mm),
                            end=((vetor[i + 1].x/10) * mm, (vetor[i + 1].y/10) * mm)))
        circle = dwg.circle(center=((vetor[i].x/10) * mm, (vetor[i].y/10) * mm), r='0.5mm', stroke='blue')
        shapes.add(circle)
        text = dwg.text(vetor[i].nome, insert=((vetor[i].x/10 - 3) * mm, (vetor[i].y/10 + 3) * mm))
        shapes.add(text)
        i += 1
    text = dwg.text(nome, insert=(posi * mm, 220 * mm), fill = cor, font_size=15)
    shapes.add(text)
    custo = round(custo, 2)
    dia = round((custo/600), 2)
    dinheiro = round((custo / 600) * 150, 2)
    text = dwg.text(str(custo), insert=(posi * mm, 230 * mm), fill=cor, font_size=15)
    shapes.add(text)
    text = dwg.text(str(dia), insert=(posi * mm, 240 * mm), fill=cor, font_size=15)
    shapes.add(text)
    text = dwg.text(str(dinheiro), insert=(posi * mm, 250 * mm), fill=cor, font_size=15)
    shapes.add(text)
    return custo, dia, dinheiro

def total(dwg, nome1, nome2, nome3, nome4, posi):
    shapes = dwg.add(dwg.g(id='shapes', fill='black'))
    text = dwg.text(nome1, insert=(posi * mm, 220 * mm), font_size=15)
    shapes.add(text)
    text = dwg.text(nome2, insert=(posi * mm, 230 * mm), font_size=15)
    shapes.add(text)
    text = dwg.text(nome3, insert=(posi * mm, 240 * mm), font_size=15)
    shapes.add(text)
    text = dwg.text(nome4, insert=(posi * mm, 250 * mm), font_size=15)
    shapes.add(text)

adicionarCidades()
calcularDistancia()

vetorResultado = []
cidadeInicial = cidades[0]
vetorResultado.append(cidadeInicial)
cidadeInicial.visitada = True
cidadesFaltamPercorrer = cidades.copy()
cidadesFaltamPercorrer.remove(cidadeInicial)
caxeiros = []
idCaxeiro = 0

while cidadesFaltamPercorrer != []:
    i = 0
    caxeiro = Caxeiro('Caxeiro' + str(idCaxeiro))
    caxeiro.cidadePercorridas.append(cidadeInicial)
    cidadeAtual = cidadeInicial
    while i < ((quantCidades) / quantCaxeiros):
        cidadeEscolhida = cidadeAtual.cidadeMaisProxima()
        if cidadeEscolhida != None:
            cidadeEscolhida.visitada = True
            cidadeAtual = cidadeEscolhida
            vetorResultado.append(cidadeEscolhida)
            caxeiro.cidadePercorridas.append(cidadeEscolhida)
            cidadesFaltamPercorrer.remove(cidadeEscolhida)
        i += 1
    caxeiro.cidadePercorridas.append(cidadeInicial)
    caxeiros.append(caxeiro)
    idCaxeiro += 1

vetorResultado.append(cidadeInicial)


dwg = svgwrite.Drawing(filename='percuso' + str(quantCidades)  + str(quantCaxeiros)  + '.svg', size=(415 * mm, 255 * mm), debug=True)
posi = 30
total(dwg, '', 'Custo', 'Dia', 'Dinheiro', 10)
custo = 0
dia = 0
dinheiro = 0
for i in caxeiros:
    retorno = basic_shapes(i.nome, i.cidadePercorridas, dwg, posi, verificaCusto(i.cidadePercorridas))
    custo += retorno[0]
    dia += +retorno[1]
    dinheiro += retorno[2]
    posi += 30
total(dwg, 'Total', str(round(custo, 2)), str(round(dia, 2)), str(round(dinheiro, 2)), posi)
dwg.save()

for i in caxeiros:
    i.cidadePercorridas = two_opt(i.cidadePercorridas)

dwg = svgwrite.Drawing(filename='percusoT' + str(quantCidades) + str(quantCaxeiros)  + '.svg', size=(415 * mm, 255 * mm), debug=True)
posi = 30
total(dwg, '', 'Custo', 'Dia', 'Dinheiro', 10)
custo = 0
dia = 0
dinheiro = 0
for i in caxeiros:
    retorno = basic_shapes(i.nome, i.cidadePercorridas, dwg, posi, verificaCusto(i.cidadePercorridas))
    custo += retorno[0]
    dia += +retorno[1]
    dinheiro += retorno[2]
    posi += 30

total(dwg, 'Total', str(round(custo, 2)), str(round(dia, 2)), str(round(dinheiro, 2)), posi)

dwg.save()
