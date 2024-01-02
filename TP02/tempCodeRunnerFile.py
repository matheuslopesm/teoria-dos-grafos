import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageDraw
from graph import Grafo

class InterfaceGrafica:
    def __init__(self, root):
        self.root = root
        self.root.title("Busca em Largura - Teoria dos Grafos (CSI466)")

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.botaoCarregarImagem = tk.Button(self.frame, text="Carregar Arquivo", command=self.carregarImagem)
        self.botaoCarregarImagem.pack(side=tk.LEFT)

        self.botaoBuscarCaminho = tk.Button(self.frame, text="Buscar Caminho", command=self.realizarBuscaCaminho)
        self.botaoBuscarCaminho.pack(side=tk.LEFT)

        # Adicionei um range para dar zoom na imagem
        self.sliderZoom = ttk.Scale(self.frame, from_=0.1, to=40, orient=tk.HORIZONTAL, length=200, value=1, command=self.atualizarZoom)
        self.sliderZoom.pack(side=tk.LEFT, padx=10)

        self.labelImagem = tk.Label(root)
        self.labelImagem.pack()

        self.caminhoImagem = ""
        self.grafo = None
        self.espacamento = 0

    def carregarImagem(self):
        """
        Abre uma interface para carregar um arquivo de imagem BMP 
        e criar um grafo a partir dele.
        """
        self.caminhoImagem = filedialog.askopenfilename(filetypes=[("Imagens BMP", "*.bmp")])
        if self.caminhoImagem:
            grafo = Grafo()
            grafo.criaGrafo(self.caminhoImagem)
            self.grafo = grafo

    def realizarBuscaCaminho(self):
        """
        Realiza a busca em largura no grafo e desenha o caminho na imagem.
        A imagem é rotacionada e espelhada horizontalmente para ficar visualizada igual a
        imagem fornecida.
        """
        if self.grafo:
            zoom = self.sliderZoom.get()
            larguraTela = 600
            alturaTela = 400
            self.espacamento = min(larguraTela, alturaTela) / max(self.grafo.numNos, 1) * zoom

            imagemBranca = Image.new("RGB", (larguraTela, alturaTela), "white")
            draw = ImageDraw.Draw(imagemBranca)

            for i, pixel in enumerate(self.grafo.lista):
                x, y = pixel
                centroX = (x + 0.5) * self.espacamento
                centroY = (y + 0.5) * self.espacamento
                raio = 0.4 * self.espacamento
                draw.ellipse(
                    [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                    outline="black",
                    fill="white"
                )

            caminho = self.grafo.buscaLargura(self.grafo.pixelInicial, self.grafo.pixelFinal)

            self.desenharCaminho(imagemBranca, caminho, self.espacamento)

            imagemBranca = imagemBranca.rotate(-90, expand=True)
            imagemBranca = imagemBranca.transpose(Image.FLIP_LEFT_RIGHT)
            imagemBrancaTk = ImageTk.PhotoImage(imagemBranca)
            self.labelImagem.config(image=imagemBrancaTk)
            self.labelImagem.imagem = imagemBrancaTk

    def desenharCaminho(self, imagem, caminho, espacamento):
        draw = ImageDraw.Draw(imagem)
        corCaminho = (255, 0, 0)

        for pixel in caminho:
            x, y = pixel
            centroX = (x + 0.5) * espacamento
            centroY = (y + 0.5) * espacamento
            raio = 0.4 * espacamento
            draw.ellipse(
                [centroX - raio, centroY - raio, centroX + raio, centroY + raio],
                outline="black",
                fill=corCaminho
            )

    def atualizarZoom(self, _=None):
        self.realizarBuscaCaminho()

root = tk.Tk()
interface = InterfaceGrafica(root)
root.mainloop()
