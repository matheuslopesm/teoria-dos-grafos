from graph import Grafo

arquivoBitmap = input("Informe o arquivo bitmap: ")

grafinho = Grafo()
grafinho.criaGrafo(arquivoBitmap)

escolha = input("Você deseja imprimir/visualizar o grafo construído? [1] - Sim, [2] - Não\n")

if escolha == "1":
    grafinho.printaGrafo()
else:
    print("Encerrando...")
    None