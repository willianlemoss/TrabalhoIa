class Cidades:
    def __init__(self, nome, x, y):
        self.nome = nome
        self.x = x
        self.y = y
        self.visitada = False
        self.distancia = {nome: []}

    def adicionarDistancia(self,cidade, distancia):
        self.distancia[self.nome].append([cidade, distancia])

    def mostrarDistancia(self):
        for i in self.distancia[self.nome]:
            print('Distancia da ' + self.nome + ' para ', end= '' )
            print(i[0].nome, end= '  ')
            print(i[1])

    def cidadeMaisProxima(self):
        maiorDistancia = 99999
        cidadeEscolhida = None
        for i in self.distancia[self.nome]:
            if i[1] < maiorDistancia and i[1] > 0 and i[0].visitada == False:
                maiorDistancia = i[1]
                cidadeEscolhida = i[0]
        return cidadeEscolhida

    def cidadeMaisDistante(self):
        menorDistancia = -99999
        cidadeEscolhida = None
        for i in self.distancia[self.nome]:
            if i[1] > menorDistancia and i[0].visitada == False:
                menorDistancia = i[1]
                cidadeEscolhida = i[0]
        return cidadeEscolhida, menorDistancia

    def retornaDistancia(self, cidade):
        for i in self.distancia[self.nome]:
            if cidade == i[0]:
                return i[1]

