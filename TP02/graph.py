from PIL import Image
import os
import heapq

class Grafo:
    def __init__(self) -> None:
        self.lista = {}
        self.numNos = 0
        self.numArestas = 0
        self.pixelInicial = 0
        self.pixelFinal = 0
        self.areasVerdes = []
        self.cinzasClaros = []
        self.cinzasEscuros = []
        self.pixelsPretos = []

    def adicionaNo(self, no: any) -> None:
        """
        Adiciona nó ao grafo.

        Parâmetros:
        - no: O nó que será adicionado ao grafo.

        Essa função verifica se o nó já existe no grafo antes de fazer a adição. Após a adição
        ela itera o número de nós existentes no grafo.
        """
        try:
            if self.lista[no] != {}:
                return
        except KeyError:
            self.lista[no] = {}
            self.numNos += 1

    def adicionaAresta(self, u, v, pesoAresta):
        """
        Adiciona aresta entre 2 nós do grafo.

        Parâmetros:
        - u: Nó que será ligado a u.
        - v: Nó que será ligado a v.
        - pesoAresta: Peso da aresta que será adicionada entre os nós u e v.

        Essa função adiciona uma aresta (ligação) entre dois nós u e v com o peso informado e
        itera o número de arestas existentes no grafo.
        """
        self.adicionaNo(u)
        self.adicionaNo(v)
        self.lista[u][v] = pesoAresta
        self.numArestas += 1

    def carregaImagem(self, arquivoBitmap):
        """
        Carrega a imagem bitmap que está dentro da pasta fornecida pelo usuário.

        Parâmetros:
        - arquivoBitmap: Imagem bitmap a ser mapeada.

        Essa função pega o diretório atual do arquivo e o caminho do arquivo informado pelo usuário (que está dentro da pasta),
        utiliza o módulo "Image" da biblioteca PIL e faz tratamento de exceções para importar o arquivo com sucesso.
        """
        diretorioAtual = os.path.dirname(os.path.abspath(__file__))
        caminhoArquivo = os.path.join(diretorioAtual, arquivoBitmap)

        try:
            imagem = Image.open(caminhoArquivo)
            return imagem
        except FileNotFoundError:
            print(f"Arquivo {caminhoArquivo} não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao abrir a imagem {e}")
            return None

    def criaGrafo(self, arquivoBitmap):
        """
        Carrega a imagem bitmap informada pelo usuário e cria o grafo correspondente.

        Parâmetros:
        - arquivoBitmap: Caminho da imagem bitmap a ser mapeada.

        Essa função utiliza o módulo "Image" da biblioteca PIL para abrir e carregar a imagem bitmap
        especificada pelo usuário. Em seguida, percorre os pixels da imagem, adiciona os nós correspondentes
        ao grafo, identifica os nós inicial e final a partir das cores dos pixels e, finalmente, conecta
        os vizinhos no grafo. Por fim, realiza uma busca em largura para caminhos mínimos entre os nós inicial
        e final.
        """
        pontosRelativos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        imagem = self.carregaImagem(arquivoBitmap)

        if imagem is None:
            print("Arquivo não encontrado!")

        base, altura = imagem.size
        """
        Nesse trecho, peguei nó por linha (horizontal), cada nó por coluna (vertical) e somei
        eles à cada coordenada da lista "pontosRelativos": superior, inferior, esquerda, direita, 
        pois um nó pode ter 1 a 4 vizinhos dentro dos limites do grafo (base, altura).
        Utilizei condições para pegar esses nós e adicionar no grafo.
        Depois disso peguei as cores inicial (vermelho) e final (verde) identificadas no grafo.
        Por fim, chamei 2 funções: conectaVizinhos e buscaLargura.
        """
        for linha in range(altura):
            for coluna in range(base):
                for dx, dy in pontosRelativos:
                    novoU, novoV = linha + dx, coluna + dy
                    if altura > novoU >= 0 and base > novoV >= 0:
                        novoNo = novoU, novoV
                        pixel = (novoV, novoU)
                        corDoPixel = imagem.getpixel(pixel)
                        if (novoNo) not in self.lista:
                            self.adicionaNo(novoNo)
                        if corDoPixel == (0, 0, 0):
                            self.pixelsPretos.append(novoNo)
                        if corDoPixel == (255, 0, 0):
                            self.pixelInicial = novoNo
                        if corDoPixel == (0, 255, 0):
                            self.pixelFinal = novoNo
                            self.areasVerdes.append(novoNo)
                        if corDoPixel == (128, 128, 128):
                            self.cinzasEscuros.append(novoNo)  # Sempre que encontrar uma área verde ela será adicionada na lista de áreas verdes.
                        if corDoPixel == (196, 196, 196):
                            self.cinzasClaros.append(novoNo)
        self.conectaVizinhos(base, altura, imagem, corDoPixel)

    def conectaVizinhos(self, base, altura, imagem, corDoPixel):
        """
        Conecta os nós vizinhos no grafo.

        Parâmetros:
        - base: Largura da imagem.
        - altura: Altura da imagem.

        Essa função percorre todos os nós do grafo e, para cada nó, verifica os vizinhos nas direções
        superior, inferior, esquerda e direita. Se um vizinho estiver dentro dos limites da imagem e existir
        no grafo, adiciona uma aresta entre o nó atual e o vizinho.
        """
        for no in self.lista:
            linha, coluna = no
            corDoPixelAtual = imagem.getpixel((coluna, linha))

            if corDoPixelAtual != (0, 0, 0):
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    novoU, novoV = linha + dx, coluna + dy
                    if altura > novoU >= 0 and base > novoV >= 0:
                        vizinho = novoU, novoV
                        corDoVizinho = imagem.getpixel((novoV, novoU))

                        if vizinho in self.lista and corDoVizinho != (0, 0, 0):
                            # Define um peso base
                            peso = 1

                            # Se o vizinho for um pixel não branco, torna a ligação menos favorável
                            if corDoVizinho != (255, 255, 255):
                                peso *= 1.5

                            if corDoPixelAtual == (128, 128, 128):
                                peso *= 2  # Aumenta o peso para pixels cinza escuro
                            elif corDoPixelAtual == (196, 196, 196):
                                peso *= 1.5  # Aumenta o peso para pixels cinza claro

                            self.adicionaAresta(no, vizinho, peso)

        self.printaGrafoNoConsole()

    def dijkstra(self, pixelInicial):
        dist = {no: float("inf") for no in self.lista}
        pred = {no: None for no in self.lista}
        dist[pixelInicial] = 0
        Q = [(dist[pixelInicial], pixelInicial)]

        while Q:
            dist_u, u = heapq.heappop(Q)

            for v, peso in self.lista[u].items():
                if dist[v] > dist_u + peso:
                    dist[v] = dist_u + peso
                    heapq.heappush(Q, (dist[v], v))
                    pred[v] = u

        return pred

    def reconstruirCaminho(self, pixelFinal, pred):
        """
        Recria o caminho percorrido com base nas informações de predecessores mantidas durante a
        execução do algoritmo.

        Parâmetros:
        - pixelFinal: Pixel de destino do caminho.
        - pred: Dicionário de predecessores.

        Retorna uma lista de coordenadas representando o caminho percorrido.
        """
        caminho = []  # Usada para armazenar as coordenadas do caminho
        atual = pixelFinal  # Inicializa o nó com o pixelFinal, pois a reconstrução vai começar pelo final para ser mais performático.

        while atual is not None:
            caminho.insert(0, atual)  # Insere as coordenadas na lista caminho
            atual = pred[atual]  # Atualiza o nó atual como sendo o predecessor

        return caminho

    def printaGrafoNoConsole(self):
        """
        Printa o grafo com seus nós, arestas e os pesos de cada uma delas.
        Exemplo: "No: (19, 15), Arestas: [((18, 15), 1), ((19, 14), 1), ((19, 16), 1)]"
        """
        for no, vizinhos in self.lista.items():
            print(f"No: {no}, Arestas: {[(vizinho, peso) for vizinho, peso in vizinhos.items()]}")
