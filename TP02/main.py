import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
from graph import Grafo
import os


class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Trabalho 02 - Teoria dos Grafos (CSI466)")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.botaoCarregarImagem = tk.Button(
            self.frame, text="Carregar Pasta com BMP", command=self.carregarImagem
        )
        self.botaoCarregarImagem.pack(side=tk.LEFT)

        # Adicionei um range para dar zoom na imagem
        self.sliderZoom = ttk.Scale(
            self.frame,
            from_=0.1,
            to=40,
            orient=tk.HORIZONTAL,
            length=200,
            value=1,
            command=self.atualizarZoom,
        )
        self.sliderZoom.pack(side=tk.LEFT, padx=10)

        self.labelImagem = tk.Label(root)
        self.labelImagem.pack()

        self.pastaImagem = ""
        self.grafo = None
        self.espacamento = 0

    def carregarImagem(self):
        """
        Abre uma interface para carregar uma pasta contendo uma imagem BMP
        e cria um grafo a partir dela.
        """
        self.pastaImagem = filedialog.askdirectory()
        if self.pastaImagem:
            arquivoBMP = next(
                (f for f in os.listdir(self.pastaImagem) if f.lower().endswith(".bmp")),
                None,
            )
            if arquivoBMP:
                caminhoImagem = os.path.join(self.pastaImagem, arquivoBMP)
                grafo = Grafo()
                grafo.criaGrafo(caminhoImagem)
                self.grafo = grafo

                # Chama a função para realizar a busca do caminho e desenhar na interface
                self.desenhaGrafo()

    def desenhaGrafo(self):
        if self.grafo:
            zoom = self.sliderZoom.get()
            larguraTela = 500
            alturaTela = 1000
            self.espacamento = (
                min(larguraTela, alturaTela) / max(self.grafo.numNos, 1) * zoom
            )

            imagemBranca = Image.new("RGB", (larguraTela, alturaTela), "white")
            draw = ImageDraw.Draw(imagemBranca)

            menorCaminho = None
            menorDistancia = float("inf")

            pred = self.grafo.dijkstra(self.grafo.areasVermelhas)

            for i, pixel in enumerate(self.grafo.lista):
                x, y = pixel
                centroX = (x + 0.5) * self.espacamento
                centroY = (y + 0.5) * self.espacamento
                raio = 0.4 * self.espacamento
                if pixel in self.grafo.areasVerdes:
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
                elif pixel in self.grafo.areasVermelhas:
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
                elif pixel in self.grafo.cinzasEscuros:
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
                elif pixel in self.grafo.cinzasClaros:
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
                elif pixel in self.grafo.pixelsPretos:
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

        for pixelFinal in self.grafo.areasVerdes:
            caminho = self.grafo.reconstruirCaminho(pixelFinal, pred)
            distancia = len(caminho)

            if distancia < menorDistancia:
                menorDistancia = distancia
                menorCaminho = caminho

        self.desenharCaminho(imagemBranca, menorCaminho, self.espacamento)

        imagemBranca = imagemBranca.rotate(-90, expand=True)
        imagemBranca = imagemBranca.transpose(Image.FLIP_LEFT_RIGHT)
        imagemBrancaTk = ImageTk.PhotoImage(imagemBranca)
        self.labelImagem.config(image=imagemBrancaTk)
        self.labelImagem.imagem = imagemBrancaTk

    def desenharCaminho(self, imagem, caminho, espacamento):
        draw = ImageDraw.Draw(imagem)

        for pixel in caminho:
            x, y = pixel
            centroX = (x + 0.5) * espacamento
            centroY = (y + 0.5) * espacamento
            raio = 0.4 * espacamento
            if pixel in self.grafo.areasVerdes:
                draw.ellipse(
                    [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                    outline="black",
                    fill=(0, 255, 0),
                )
            elif pixel in self.grafo.areasVermelhas:
                draw.ellipse(
                    [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                    outline="black",
                    fill=(255, 0, 0),
                )
            elif pixel:
                draw.ellipse(
                    [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                    outline="black",
                    fill=(0, 0, 255),
                )

    def atualizarZoom(self, _=None):
        self.desenhaGrafo()


root = tk.Tk()
interface = InterfaceGrafica(root)
root.mainloop()
