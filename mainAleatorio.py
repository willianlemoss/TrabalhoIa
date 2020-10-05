import math
from Cidades import Cidades
from Caxeiro import Caxeiro
import random as r
arq = open("ncit30.dat",'r')
lines = arq.readlines()
quantCidades = int(lines[0])
cidades = []

def adicionarCidades():
    for i in range(quantCidades):
        localizacao = lines[i + 1].split(' ')
        x = int(localizacao[0])
        y = int(localizacao[1])
        cidade = Cidades('Cidade'+ str(i),x,y)
        cidades.append(cidade)

def mostrarTodasDistancias():
    for i in cidades:
        i.mostrarDistancia()

def euclidiana(cidade1, cidade2):
    x = pow(cidade1.x - cidade2.x, 2)
    y = pow(cidade1.y - cidade2.y, 2)
    distancia = math.sqrt(x+y)
    cidade1.adicionarDistancia(cidade2, distancia)

def calcularDistancia():
    for i in cidades:
        for j in cidades:
            euclidiana(i, j)

def verificaCusto(vetor):
    i = 0
    custo = 0
    while len(vetor)-1 > i:
        dist = vetor[i].retornaDistancia(vetor[i+1])
        custo += dist
        i += 1
    return custo


adicionarCidades()
calcularDistancia()

# Aleatorio
vetorResultado =[]
cidadeInicial = cidades[0]
cidadesFaltamPercorrer = cidades.copy()
cidadesFaltamPercorrer.remove(cidadeInicial)
caxeiro = Caxeiro('Caxeiro1')
cidadeAtual = cidadeInicial
vetorResultado.append(cidadeInicial)

print(cidadeInicial.nome)

while cidadesFaltamPercorrer != []:
    cidadeEscolhida = cidadesFaltamPercorrer[r.randint(0, len(cidadesFaltamPercorrer) - 1)]
    distanciaPercorrida = cidadeAtual.retornaDistancia(cidadeEscolhida)
    caxeiro.distanciaPercorrida += distanciaPercorrida
    cidadeAtual = cidadeEscolhida
    vetorResultado.append(cidadeEscolhida)
    cidadesFaltamPercorrer.remove(cidadeEscolhida)
    # print(cidadeEscolhida.nome, end= ' ')
    # print(distanciaPercorrida)

caxeiro.distanciaPercorrida += cidadeAtual.retornaDistancia(cidadeInicial)
vetorResultado.append(cidadeInicial)

print('Aleatório')
print('distanciaPercorrida' , end= ' ')
print(caxeiro.distanciaPercorrida)

print('QUANT dias' , end= ' ')
print(caxeiro.distanciaPercorrida/600)

print('Valor' , end= ' ')
print(caxeiro.distanciaPercorrida/600*150)

import svgwrite
from svgwrite import mm

def basic_shapes(nome, vetor):
    dwg = svgwrite.Drawing(filename=nome, size=(150 * mm, 150 * mm), debug=True)
    hlines = dwg.add(dwg.g(id='hlines', stroke='black'))
    shapes = dwg.add(dwg.g(id='shapes', fill='red'))
    i = 0
    while i < len(vetor) -1:
        hlines.add(dwg.line(start=((vetor[i].x/100) * mm, (vetor[i].y/100) * mm),
                            end=((vetor[i + 1].x/100) * mm, (vetor[i + 1].y/100) * mm)))
        circle = dwg.circle(center=((vetor[i].x/100) * mm, (vetor[i].y/100) * mm), r='0.5mm', stroke='blue')
        shapes.add(circle)
        text = dwg.text(vetor[i].nome, insert=((vetor[i].x/100 - 3) * mm, (vetor[i].y/100 + 3) * mm))
        shapes.add(text)
        i += 1
    dwg.save()


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

vetorResultado = two_opt(vetorResultado)
basic_shapes('percusoA.svg', vetorResultado)
print(verificaCusto(vetorResultado))
print(verificaCusto(vetorResultado)/600)