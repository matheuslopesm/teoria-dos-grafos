import time
from PIL import Image
import os
import heapq


class Graph:
    def __init__(self) -> None:
        self.lista = {}
        self.numNos = 0
        self.numArestas = 0
        self.pixelFinal = 0
        self.areasVerdes = []
        self.areasVermelhas = []
        self.cinzasClaros = []
        self.cinzasEscuros = []
        self.pixelsPretos = []

    def adicionaNo(self, pixel_info):
        """
        Adiciona nó ao grafo.

        Parâmetros:
        - pixel_info: O nó que será adicionado ao grafo.

        Essa função verifica se o nó já existe no grafo antes de fazer a adição. Após a adição
        ela itera o número de nós existentes no grafo.
        """
        try:
            if self.lista[pixel_info] != {}:
                return
        except KeyError:
            self.lista[pixel_info] = {}
            self.numNos += 1

    def adicionaAresta(self, u, v, pesoAresta):
        """
        Adiciona aresta ao grafo.

        Parâmetros:
        - u: O primeiro nó da aresta.
        - v: O segundo nó da aresta.
        - pesoAresta: O peso da aresta a ser adicionada.

        Esta função adiciona uma aresta entre os nós u e v no grafo, garantindo que ambos os nós existam previamente.
        Após a adição, incrementa o número de arestas do grafo.
        """
        self.adicionaNo(u)
        self.adicionaNo(v)
        self.lista[u][v] = pesoAresta
        self.numArestas += 1

    def carregaImagem(self, arquivoBitmap):
        """
        Carrega imagem do arquivo Bitmap.

        Parâmetros:
        - arquivoBitmap: O caminho do arquivo Bitmap a ser carregado.

        Esta função tenta carregar a imagem do arquivo Bitmap especificado e retorna a imagem carregada.
        Se ocorrer algum erro ao abrir a imagem, imprime uma mensagem de erro e retorna None.
        """
        try:
            imagem = Image.open(arquivoBitmap)
            return [imagem]
        except Exception as e:
            print("Erro ao abrir as imagens:", e)
            return None

    def criaGrafo(self, arquivoBitmap):
        """
        Cria o grafo a partir de uma imagem Bitmap.

        Parâmetros:
        - arquivoBitmap: O caminho do arquivo Bitmap a ser utilizado para criar o grafo.

        Esta função carrega a imagem do arquivo Bitmap especificado e cria um grafo com base nos pixels da imagem.
        Itera sobre os pixels da imagem, criando nós para representar cada pixel e adicionando-os ao grafo.
        Além disso, identifica diferentes regiões na imagem com base nas cores dos pixels e as marca para posterior análise.
        """
        pontosRelativos = [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, 1),
            (0, 0, -1),
        ]

        imagens = self.carregaImagem(arquivoBitmap)
        numPisos = len(imagens)

        if imagens is None:
            print("Arquivos não encontrados!")
            return

        for numPiso in range(numPisos):
            imagem = imagens[numPiso]
            base, altura = imagem.size

            for linha in range(altura):
                for coluna in range(base):
                    for dx, dy, dz in pontosRelativos:
                        novoU, novoV, novoT = linha + dx, coluna + dy, dz
                        if (
                            altura > novoU >= 0
                            and base > novoV >= 0
                            and numPisos > novoT >= 0
                        ):
                            pixel = (novoV, novoU, numPiso)

                            corDoPixel = imagem.getpixel((novoV, novoU))

                            if pixel not in self.lista:
                                self.adicionaNo(pixel)
                            elif corDoPixel == (0, 0, 0):
                                self.pixelsPretos.append(pixel)
                            elif corDoPixel == (255, 0, 0):
                                if pixel not in self.areasVermelhas:
                                    self.areasVermelhas.append(pixel)
                            elif corDoPixel == (0, 255, 0):
                                if pixel not in self.areasVerdes:
                                    self.pixelFinal = pixel
                                    self.areasVerdes.append(pixel)
                            elif corDoPixel == (128, 128, 128):
                                if pixel not in self.cinzasEscuros:
                                    self.cinzasEscuros.append(pixel)
                            elif corDoPixel == (196, 196, 196):
                                if pixel not in self.cinzasClaros:
                                    self.cinzasClaros.append(pixel)
        self.conectaVizinhos(base, altura, numPisos, imagem)

    def conectaVizinhos(self, base, altura, profundidade, imagem):
        """
        Conecta os vizinhos no grafo.

        Parâmetros:
        - base: A largura da imagem em pixels.
        - altura: A altura da imagem em pixels.
        - profundidade: A profundidade do grafo, representando o número de andares.
        - imagem: A imagem utilizada para determinar a conectividade dos pixels.

        Esta função percorre os pixels da imagem e adiciona arestas entre os pixels vizinhos no grafo,
        considerando apenas os pixels que não são pretos. O peso das arestas é determinado com base na cor do pixel.
        """
        for linha in range(altura):
            for coluna in range(base):
                # Obtém a cor do pixel atual
                corDoPixelAtual = imagem.getpixel((coluna, linha))

                # Verifica se o pixel não é preto
                if corDoPixelAtual != (0, 0, 0):
                    # Adiciona o pixel como nó no grafo
                    pixel = (coluna, linha, 0)
                    self.adicionaNo(pixel)

                    # Verifica os vizinhos nas direções vertical e horizontal
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        novoU, novoV, novoT = linha + dy, coluna + dx, 0
                        if (
                            0 <= novoU < altura
                            and 0 <= novoV < base
                            and 0 <= novoT < profundidade
                        ):
                            vizinho = (novoV, novoU, novoT)

                            if vizinho in self.lista:
                                peso = 1

                                if corDoPixelAtual == (128, 128, 128):
                                    peso = 4  # Peso 4 para pixels cinza escuro
                                elif corDoPixelAtual == (196, 196, 196):
                                    peso = 2  # Peso 2 para pixels cinza claro

                                if novoT != 0:
                                    peso = 5  # Peso 5 se o vizinho estiver em um piso diferente

                                self.adicionaAresta(pixel, vizinho, peso)

    def dijkstra(self, areasVermelhas, grafo=None):
        """
        Executa o algoritmo de Dijkstra em um grafo.

        Parâmetros:
        - areasVermelhas: Uma lista de pontos da saída do caminho no grafo.
        - grafo: O grafo no qual o algoritmo será executado. Se não for fornecido, será utilizado o grafo interno.

        Retorna:
        Um dicionário contendo os predecessores de cada nó no caminho mais curto até as áreas vermelhas especificadas.
        """
        if grafo is None:
            grafo = self.lista  # Use o grafo interno se nenhum grafo for fornecido

        dist = {no: float("inf") for no in grafo}
        pred = {no: None for no in grafo}

        Q = [(0, ponto) for ponto in areasVermelhas]

        for ponto in areasVermelhas:
            dist[ponto] = 0

        while Q:
            dist_u, u = heapq.heappop(Q)

            for v, peso in grafo[u].items():
                if dist[v] > dist_u + peso:
                    dist[v] = dist_u + peso
                    pred[v] = u
                    heapq.heappush(Q, (dist[v], v))

        return pred
    
    def dijkstraForMultiplasImagens(self, areasVermelhas, grafo=None):
        """
        Executa o algoritmo de Dijkstra em um grafo com múltiplos andares (imagens).

        Parâmetros:
        - areasVermelhas: Uma lista de pontos da saída do caminho no grafo.
        - grafo: O grafo no qual o algoritmo será executado. Se não for fornecido, será utilizado o grafo interno.

        Retorna:
        Um dicionário contendo os predecessores de cada nó no caminho mais curto até as áreas vermelhas especificadas,
        considerando a possibilidade de múltiplos andares.
        """
        if grafo is None:
            grafo = self.lista

        dist = {no: float("inf") for no in grafo}
        pred = {no: None for no in grafo}

        Q = [(0, ponto) for ponto in areasVermelhas]

        for ponto in areasVermelhas:
            dist[ponto] = 0

        while Q:
            dist_u, u = heapq.heappop(Q)

            # print(f"Explorando nó {u}, distância atual: {dist_u}")

            x, y, z = u

            # Verificar vizinhos em todos os andares
            for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, -1), (0, 0, 1)]:
                novoX, novoY, novoZ = x + dx, y + dy, z + dz
                novoPonto = (novoX, novoY, novoZ)

                if novoPonto in grafo:
                    peso = 1
                    if dz != 0:
                        peso = 5

                    if dist[novoPonto] > dist_u + peso:
                        dist[novoPonto] = dist_u + peso
                        pred[novoPonto] = u
                        heapq.heappush(Q, (dist[novoPonto], novoPonto))
                        # print(f"   Atualizado nó {novoPonto}, nova distância: {dist[novoPonto]}, predecessor: {u}")
        return pred

    def reconstruirCaminho(self, pixelFinal, pred):
        """
        Reconstrói o caminho a partir do pixel final e dos predecessores.

        Parâmetros:
        - pixelFinal: O pixel final do caminho.
        - pred: Um dicionário contendo os predecessores de cada nó no caminho.

        Retorna:
        Uma lista contendo as coordenadas do caminho reconstruído a partir do pixel final.
        """
        caminho = []
        atual = pixelFinal

        while atual is not None:
            caminho.insert(0, atual)
            atual = pred[atual]

        return caminho
