    def carregarImagem(self):
        """
        Abre uma interface para carregar um arquivo de imagem BMP
        e criar um grafo a partir dele.
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