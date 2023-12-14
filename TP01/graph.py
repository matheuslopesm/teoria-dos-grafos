from PIL import Image
import os


class Grafo:
    def __init__(self) -> None:
        self.lista = {}
        self.numNos = 0
        self.numArestas = 0

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
        Carrega a imagem bitmap informada pelo usuário.

        Parâmetros:
        - arquivoBitmap: Imagem bitmap a ser mapeada.

        Essa função pega o diretório atual deste arquivo e o caminho do arquivo informado pelo usuário,
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
                    novoU, novoV = linha + dx, coluna + dy  # S
                    if altura > novoU >= 0 and base > novoV >= 0:
                        novoNo = novoU, novoV
                        pixel = (novoV, novoU)
                        corDoPixel = imagem.getpixel(pixel)
                        if (novoNo) not in self.lista and corDoPixel != (0, 0, 0):
                            self.adicionaNo(novoNo)
                        if corDoPixel == (255, 0, 0):
                            pixelInicial = novoNo
                        if corDoPixel == (0, 255, 0):
                            pixelFinal = novoNo
        self.conectaVizinhos(base, altura)
        self.buscaLargura(pixelInicial, pixelFinal)

    def conectaVizinhos(self, base, altura):
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
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                novoU, novoV = linha + dx, coluna + dy
                if altura > novoU >= 0 and base > novoV >= 0:
                    vizinho = novoU, novoV
                    if vizinho in self.lista:
                        self.adicionaAresta(no, vizinho, 1)

    def buscaLargura(self, pixelInicial, pixelFinal):
        """
        Executa a busca em largura para encontrar o menor caminho entre dois pixels.

        Parâmetros:
        - pixelInicial: Pixel de início da busca.
        - pixelFinal: Pixel de destino da busca.

        Essa função utiliza a busca em largura para encontrar o menor caminho no grafo entre o pixelInicial
        e o pixelFinal. Ela mantém distâncias e predecessores para reconstruir o caminho percorrido e imprime
        o caminho encontrado.
        """
        dist = {no: float("inf") for no in self.lista}
        pred = {no: None for no in self.lista}
        Q = [pixelInicial]
        dist[pixelInicial] = 0

        while len(Q) != 0:
            u = Q.pop(0)
            for v in self.lista[u]:
                if dist[v] == float("inf"):
                    Q.append(v)
                    dist[v] = dist[u] + 1
                    pred[v] = u
        
        caminho = self.reconstruirCaminho(pixelFinal, pred)
        print("Caminho percorrido:")
        print(" ".join(str(seta) for seta in caminho))
        print(f"Pixel Inicial (Vermelho): {pixelInicial} | Pixel Final (Verde): {pixelFinal}\n")

    def reconstruirCaminho(self, pixelFinal, pred):
        """
        Reconstrói o caminho percorrido a partir dos predecessores.

        Parâmetros:
        - pixelFinal: Pixel de destino do caminho.
        - pred: Dicionário de predecessores.

        Retorna uma lista de direções representando o caminho percorrido.
        """
        caminho = [] # Usada para armazenar as direções do caminho
        atual = pixelFinal # Inicializa o nó com o pixelFinal, pois a reconstrução vai começar pelo final para ser mais performático.
        direcoes = {(0, -1): "←", (0, 1): "→", (-1, 0): "↑", (1, 0): "↓"}

        while atual is not None:
            anterior = pred[atual] # Pega o predecessor do nó atual

            if anterior is not None:
                direcao = direcoes[(atual[0] - anterior[0], atual[1] - anterior[1])] # Subtrai as coordenadas do nó atual e o predecessor dele, exemplo: (1, 11)-(1, 10) = (1-1, 11-10) = (0, 1)
                caminho.insert(0, direcao) # Insere a direção na lista caminho

            atual = anterior # Atualiza o nó atual como sendo o predecessor

        return caminho

    def printaGrafo(self):
        for no, vizinhos in self.lista.items():
            print(f"Nó: {no}, Vizinhos: {list(vizinhos)}")
