import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import os
from graph import Graph


class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho 02 - Teoria dos Grafos (CSI466)")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.botaoCarregarImagem = tk.Button(
            self.frame, text="Carregar Pasta com BMP", command=self.carregarImagem
        )
        self.botaoCarregarImagem.pack(side=tk.LEFT, fill=tk.X)

        self.frameImagens = tk.Frame(root)
        self.frameImagens.pack()

        self.labelImagens = []
        self.grafo = None

        self.grafoDef = []

        self.pastaImagens = ""

    def carregarImagem(self):
        """
        Carrega imagens para exibição.

        Esta função solicita ao usuário que selecione um diretório contendo imagens BMP.
        Em seguida, carrega todas as imagens BMP encontradas no diretório e as exibe na interface gráfica.
        """
        self.pastaImagens = filedialog.askdirectory()
        if self.pastaImagens:
            imagens = []
            for arquivo in os.listdir(self.pastaImagens):
                if arquivo.lower().endswith(".bmp"):
                    caminhoImagem = os.path.join(self.pastaImagens, arquivo)
                    imagem = Image.open(caminhoImagem)
                    imagens.append((imagem, caminhoImagem))

            self.mostrarImagens(imagens)

    def mostrarImagens(self, imagens):
        """
        Mostra imagens na interface gráfica.

        Parâmetros:
        - imagens: Uma lista contendo tuplas de imagens e seus caminhos.

        Esta função limpa o frame de imagens existente e, em seguida, exibe as imagens fornecidas na interface gráfica.
        """
        for widget in self.frameImagens.winfo_children():
            widget.destroy()

        for idx, (imagem, caminhoImagem) in enumerate(imagens):
            frameImagem = tk.Frame(self.frameImagens)
            frameImagem.pack(side=tk.LEFT, padx=10, pady=10)

            if imagem.size[0] > imagem.size[1]:
                imagemBranca = Image.new("RGB", (1000, 500), "white")
            else:
                imagemBranca = Image.new("RGB", (450, 450), "white")

            draw = ImageDraw.Draw(imagemBranca)

            grafo = Graph()
            grafo.criaGrafo(caminhoImagem)

            self.grafo = grafo

            for pixel in grafo.lista:
                x, y, numPisos = (
                    pixel
                )

                if len(imagens) != 1:
                    self.grafoDef.append(
                        (x, y, idx)
                    )

                centroX = (x + 0.5) * 19
                centroY = (y + 0.5) * 19
                raio = 0.4 * 19
                if pixel in grafo.areasVerdes:
                    draw.ellipse(
                        [
                            centroX - raio,
                            centroY - raio,
                            centroX + raio,
                            centroY + raio,
                        ],
                        outline="black",
                        fill=(0, 255, 0),
                    )
                elif pixel in grafo.areasVermelhas:
                    draw.ellipse(
                        [
                            centroX - raio,
                            centroY - raio,
                            centroX + raio,
                            centroY + raio,
                        ],
                        outline="black",
                        fill=(255, 0, 0),
                    )
                elif pixel in grafo.cinzasEscuros:
                    draw.ellipse(
                        [
                            centroX - raio,
                            centroY - raio,
                            centroX + raio,
                            centroY + raio,
                        ],
                        outline="black",
                        fill="#808080",
                    )
                elif pixel in grafo.cinzasClaros:
                    draw.ellipse(
                        [
                            centroX - raio,
                            centroY - raio,
                            centroX + raio,
                            centroY + raio,
                        ],
                        outline="black",
                        fill="#c4c4c4",
                    )
                elif pixel in grafo.pixelsPretos:
                    draw.ellipse(
                        [
                            centroX - raio,
                            centroY - raio,
                            centroX + raio,
                            centroY + raio,
                        ],
                        outline="black",
                        fill="black",
                    )
                else:
                    draw.ellipse(
                        [
                            centroX - raio,
                            centroY - raio,
                            centroX + raio,
                            centroY + raio,
                        ],
                        outline="black",
                        fill="white",
                    )

            if len(imagens) == 1:
                menorCaminho = None
                menorDistancia = float("inf")
                pred = self.grafo.dijkstra(self.grafo.areasVermelhas)

                for pixelFinal in self.grafo.areasVerdes:
                    caminho = self.grafo.reconstruirCaminho(pixelFinal, pred)
                    distancia = len(caminho)
                    if distancia < menorDistancia:
                        menorDistancia = distancia
                        menorCaminho = caminho

                self.desenharCaminho(imagemBranca, menorCaminho, 19)
                imagemBrancaTk = ImageTk.PhotoImage(imagemBranca)
                label = tk.Label(frameImagem, image=imagemBrancaTk)
                label.imagem = imagemBrancaTk
                label.pack()
            else:
                self.conectaGrafos(grafo, imagem)
                menorCaminho = None
                menorDistancia = float("inf")
                pred = grafo.dijkstraForMultiplasImagens([(13, 18, 0)], grafo.lista)

                for pixelFinal in grafo.areasVerdes:
                    caminho = grafo.reconstruirCaminho(pixelFinal, pred)

                    distancia = len(caminho)
                    if distancia < menorDistancia:
                        menorDistancia = distancia
                        menorCaminho = caminho

                # Não consegui desenhar o caminho encontrado. 
                # Construí o grafo de cada uma das imagens subidas, juntei elas em um só grafo,
                # ligando com arestas de peso 5 entre eles, porém ao buscar o caminho os predecessores
                # não davam certo.

                # self.desenharCaminho(imagemBranca, menorCaminho, 19)

                imagemBrancaTk = ImageTk.PhotoImage(imagemBranca)
                label = tk.Label(frameImagem, image=imagemBrancaTk)
                label.imagem = imagemBrancaTk
                label.pack()

    def desenharCaminho(self, imagem, caminho, espacamento):
        """
        Desenha o caminho encontrado na imagem.

        Parâmetros:
        - imagem: A imagem na qual o caminho será desenhado.
        - caminho: Uma lista de coordenadas representando o caminho a ser desenhado.
        - espacamento: O espaçamento entre os pixels na imagem.

        Esta função desenha o caminho fornecido na imagem especificada.
        """
        draw = ImageDraw.Draw(imagem)

        for x, y, _ in caminho:
            centroX = (x + 0.5) * espacamento
            centroY = (y + 0.5) * espacamento
            raio = 0.4 * espacamento
            if (x, y, _) in self.grafo.areasVerdes:
                draw.ellipse(
                    [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                    outline="black",
                    fill=(0, 255, 0),
                )
            elif (x, y, _) in self.grafo.areasVermelhas:
                draw.ellipse(
                    [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                    outline="black",
                    fill=(255, 0, 0),
                )
            else:
                draw.ellipse(
                    [
                        centroX - raio,
                        centroY - raio,
                        centroX + raio,
                        centroY + raio,
                    ],
                    outline="black",
                    fill=(0, 0, 255),
                )

    def conectaGrafos(self, grafo, imagem):
        """
        Conecta grafos de imagens diferentes.

        Parâmetros:
        - grafo: O grafo a ser conectado com outros grafos.
        - imagem: A imagem utilizada para determinar a conectividade dos pixels.

        Esta função conecta o grafo da imagem com outros grafos, considerando os pixels não pretos.
        """
        for pixel in self.grafoDef:
            x, y, idx = pixel
            cor = imagem.getpixel((x, y))

            if cor != (0, 0, 0):
                grafo.adicionaNo(pixel)

                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    novoX, novoY, novoIdx = x + dx, y + dy, idx
                    novoPixel = (novoX, novoY, novoIdx)

                    if novoPixel in self.grafoDef and imagem.getpixel(
                        (novoX, novoY)
                    ) != (0, 0, 0):
                        if cor == (128, 128, 128):
                            grafo.adicionaAresta(
                                pixel, novoPixel, 4
                            )
                        elif cor == (196, 196, 196):
                            grafo.adicionaAresta(
                                pixel, novoPixel, 2
                            )
                        elif cor == (255, 0, 0):
                            self.grafo.areasVermelhas.append(pixel)
                        elif cor == (0, 255, 0):
                            self.grafo.pixelFinal = pixel
                            self.grafo.areasVerdes.append(pixel)
                        else:
                            grafo.adicionaAresta(
                                pixel, novoPixel, 1
                            )
                for novoIdx in [idx - 1, idx + 1]:
                    novoPixel = (x, y, novoIdx)
                    if novoPixel in self.grafoDef and imagem.getpixel((x, y)) != (
                        0,
                        0,
                        0,
                    ):
                        grafo.adicionaAresta(pixel, novoPixel, 5)


root = tk.Tk()
interface = InterfaceGrafica(root)
root.mainloop()
