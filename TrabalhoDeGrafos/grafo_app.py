''' Importação das bibliotecas necessárias '''
import tkinter as tk                            # Biblioteca para criação de janelas
from tkinter import simpledialog, messagebox    # São como os 'alert's do Javascript, mas em formato de janela
import networkx as nx                           # Biblioteca para criar e manipular grafos e network
import matplotlib.pyplot as plt                 # Biblioteca para criar visualizações estáticas, animadas e/ou interativas em Python
import numpy as np                              # Essa é famosa para Data Science, mas tou usando aqui para lidar com as matrizes
import random                                   # Isso aqui é para randomizar a cor dos nós

from networkx.drawing import spring_layout

# Fim da importação das bibliotecas
cor_dos_nos = ['Yellow', 'Lightblue', 'Green', 'Orange', 'Pink', 'Aqua', 'White']  # Lista de cores para os nós

'''Funções estáticas'''
# Configura a seta para não ficar dentro do nó, e sim em sua extremidade
def calcular_pontos_aresta(self, x1, y1, x2, y2, raio=15):
    dx = x2 - x1    # Calcula a diferença no eixo x (--) entre os dois pontos
    dy = y2 - y1    # Calcula a diferença no eixo Y (|) entre os dois pontos

    distancia = (dx ** 2 + dy ** 2) ** 0.5  # Calcula a distância direta entre os dois pontos

    # Se os dois pontos forem exatamente o mesmo, não dá pra ajustar, só retorna eles mesmos
    if distancia == 0:
        return x1, y1, x2, y2

    # Ajusta o primeiro ponto para fora do centro, indo até a borda do nó
    x1_ajustado = x1 + (dx * raio / distancia)
    y1_ajustado = y1 + (dy * raio / distancia)
    # Ajusta o segundo ponto também, mas vindo da outra direção
    x2_ajustado = x2 - (dx * raio / distancia)
    y2_ajustado = y2 - (dy * raio / distancia)

    # Retorna os dois novos pontos já ajustados
    return x1_ajustado, y1_ajustado, x2_ajustado, y2_ajustado

# Botão que ensina como usar o aplicativo.
def mostrar_como_usar():
    messagebox.showinfo("Como usar",
                        "COMO USAR:\n\n"
                        "1. Clique com o botão esquerdo para criar nós\n"
                        "2. Clique com o botão direito em dois nós para ligar com uma aresta\n"
                        "3. Clique em 'Desfazer' para apagar a última ação (Ou o atalho Ctrl + Z)\n"
                        "4. Explore os outros botões para brincar com seu grafo!")

class GrafoApp:
    #  Função inicial do aplicativo =====================================================================================
    def __init__(self):
        self.janela = tk.Tk()                                                   # Criando o construtor
        self.janela.title("CONSTRUTOR DE GRAFOS - TRABALHO TEORIA DE GRAFOS")   # Definindo o título da Janela
        self.janela.iconbitmap("Icones/icone_aplicativo.ico")                   # Definindo o ícone da Janela

        self.canvas = tk.Canvas(self.janela, width=1200, height=800, bg="white")    # Aqui estou definindo o tamanho e a cor de fundo da janela
        self.canvas.pack()                                                      # Aqui estou inicializando o canvas

        # Criação dos Botões inferiores ================================================================================

        self.botao_matriz = tk.Button(self.janela, text="Mostrar Matriz de Adjacência do Grafo",
                                      command=self.mostrar_matriz)
        self.botao_matriz.pack(side=tk.LEFT, padx=10, pady=10)


        self.botao_construir = tk.Button(self.janela, text="Criar Grafo a partir de uma Matriz",
                                         command=self.criar_grafo_da_matriz)
        self.botao_construir.pack(side=tk.LEFT, padx=10, pady=10)


        self.botao_caminhos = tk.Button(self.janela, text="Buscar Caminhos",
                                        command=self.buscar_caminhos)
        self.botao_caminhos.pack(side=tk.LEFT, padx=10, pady=10)


        self.botao_mostrar_grafo = tk.Button(self.janela, text="Mostrar Grafo",
                                             command=self.mostrar_grafo)
        self.botao_mostrar_grafo.pack(side=tk.LEFT, padx=10, pady=10)


        self.botao_como_usar = tk.Button(self.janela, text="Como usar o aplicativo",
                                         command=mostrar_como_usar)
        self.botao_como_usar.pack(side=tk.RIGHT, padx=10, pady=10)


        self.botao_desfazer = tk.Button(self.janela, text="Desfazer",
                                        command=self.desfazer_ultima_acao)
        self.botao_desfazer.pack(side=tk.RIGHT, padx=10, pady=10)


        # Mensagens que aparecerão assim que o aplicativo iniciar, perguntando a preferência
        self.orientado = messagebox.askyesno("Grafo Orientado", "Deseja criar um grafo orientado?")
        self.valorado = messagebox.askyesno("Grafo Valorado (Apenas Números Inteiros)", "O gráfico será valorado?\n(Somente números inteiros, por enquanto)")

        self.grafo = nx.DiGraph() if self.orientado else nx.Graph() # Cria o grafo: Orientado (DiGraph) ou não (Graph)
        self.nos = [] # Lista para armazenar os nós do grafo
        self.arestas = [] # Lista para armazenar as arestas do grafo
        self.historico = [] # Lista para armazenar as ações feitas (Para a função desfazer)

        # Definindo as ações de adicionar nó e adicionar aresta aos botões do mouse
        self.canvas.bind("<Button-1>", self.adicionar_no)   # Adicionar nó no botão esquerdo do mouse
        self.canvas.bind("<Button-3>", self.adicionar_aresta) # Adicionar aresta no botão direito do mouse
        self.janela.bind("<Control-z>", lambda event: self.desfazer_ultima_acao()) # Desfaz última ação com atalho Ctrl + Z

    #  ======================================= Função para desenhar os nós no canvas ============================================================================
    def adicionar_no(self, evento):
        x, y = evento.x, evento.y  # Pega as coordenadas do clique
        no_id = len(self.nos) + 1  # O ID do nó será baseado na quantidade de nós já existentes
        self.nos.append((no_id, x, y))  # Adiciona o nó com as coordenadas no array de nós
        self.grafo.add_node(no_id, pos=(x, y))  # Adiciona o nó ao grafo com a posição

        # Cria um círculo (representando o nó) no canvas
        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill = 'Yellow')
        self.canvas.create_text(x, y, text = str(no_id),
                                font = ("Comic Sans MS", 15, "bold"))  # Adiciona o ID do nó no canvas

        self.historico.append(("no", no_id))  # Adiciona a ação de adicionar nó ao histórico para desfazer

    #  ======================================= Função para adicionar uma aresta ao grafo ========================================================================
    def adicionar_aresta(self, evento):
        peso = 0.0  # Inicializa o peso da aresta como 0 (pode ser modificado se o grafo for valorado)
        if len(self.nos) < 2:  # Verifica se há pelo menos 2 nós para conectar
            return             # Não faça nada

        x, y = evento.x, evento.y  # Pega as coordenadas do clique
        distancia_minima = float("inf")  # Inicializa a variável como infinito positivo para guardar a distância mínima
        no_mais_proximo = None  # Variável para armazenar o nó mais próximo

        # Loop para encontrar o nó mais próximo do ponto clicado
        for no in self.nos:
            dist = ((x - no[1]) ** 2 + (y - no[2]) ** 2) ** 0.5  # Calcula a distância euclidiana (distância entre dois pontos) entre o clique e o nó
            # messagebox.showinfo("Essa é a distância:", dist)
            if dist < distancia_minima:  # Se encontrar uma distância menor, atualiza
                distancia_minima = dist
                no_mais_proximo = no[0]

        # Verifica se o nó mais próximo já está na lista de arestas
        if no_mais_proximo not in self.arestas:
            if len(self.arestas) == 0:
                self.arestas.append(no_mais_proximo)  # Se não houver aresta, adiciona o nó na lista de arestas
            else:
                origem = self.arestas.pop()  # Pega o nó anterior da lista de arestas
                destino = no_mais_proximo    # O nó atual se torna o destino

                # Se o grafo for valorado, pede o peso da aresta ao usuário
                if self.valorado:
                    peso = simpledialog.askinteger("Peso da aresta",
                                                   f"DIGITE O PESO DA ARESTA ENTRE O NÓ {origem} AO NÓ {destino}:",
                                                   parent=self.janela)
                self.grafo.add_edge(origem, destino, weight=peso)  # Adiciona a aresta ao grafo com peso

                self.historico.append(("aresta", (origem, destino)))  # Adiciona a ação de adicionar aresta ao histórico

                # Obtém as coordenadas dos dois nós
                x1, y1 = self.nos[origem - 1][1], self.nos[origem - 1][2]
                x2, y2 = self.nos[destino - 1][1], self.nos[destino - 1][2]
                x1, y1, x2, y2 = calcular_pontos_aresta(self, x1, y1, x2, y2)
                # Cria a linha (aresta) no canvas
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST if self.orientado else None)

                # Se o grafo for valorado, mostra o peso no meio da aresta
                if self.valorado:
                    self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2 - 10, text=str(peso),
                                            font=("Times New Roman", 14, "bold"), fill="Red")

    #  ======================================= Função para desfazer a última ação feita (nó ou aresta) ==========================================================
    def desfazer_ultima_acao(self):
        if not self.historico:  # Se não houver nada para desfazer
            messagebox.showinfo("Desfazer", "Nada para desfazer!")  # Exibe essa mensagem
            return

        acao, dados = self.historico.pop()  # Recupera a última ação feita

        if acao == "no":  # Se a ação foi de adicionar um nó
            no_id = dados
            self.nos = [no for no in self.nos if no[0] != no_id]  # Remove o nó da lista
            self.grafo.remove_node(no_id)  # Remove o nó do grafo
        elif acao == "aresta":  # Se a ação foi de adicionar uma aresta
            origem, destino = dados
            if self.grafo.has_edge(origem, destino):  # Verifica se a aresta existe no grafo
                self.grafo.remove_edge(origem, destino)  # Remove a aresta do grafo

        self.redesenhar_canvas()  # Redesenha o canvas para refletir as mudanças

    #  ======================================= Função para redesenhar o canvas, mostrando os nós e arestas atuais ===============================================
    def redesenhar_canvas(self):
        self.canvas.delete("all")  # Apaga tudo no canvas
        for no in self.nos:  # Para cada nó, desenha o círculo e o ID
            x, y = no[1], no[2]
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="Yellow")
            self.canvas.create_text(x, y, text=str(no[0]), font=("Comic Sans MS", 15, "bold"))

        for origem, destino in self.grafo.edges():  # Para cada aresta no grafo, desenha uma linha entre os nós
            x1, y1 = self.nos[origem - 1][1], self.nos[origem - 1][2]
            x2, y2 = self.nos[destino - 1][1], self.nos[destino - 1][2]
            peso = self.grafo[origem][destino].get('weight', '')  # Obtém o peso da aresta
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST if self.orientado else None)  # Cria a linha da aresta
            if self.valorado and peso != '':  # Se o grafo for valorado, desenha o peso na linha
                self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2 - 10, text=str(peso),
                                        font=("Times New Roman", 14, "bold"), fill="Red")

    #  ======================================= Função para mostrar a matriz de adjacência do grafo em uma caixa de mensagem =====================================
    def mostrar_matriz(self):
        matriz = nx.to_numpy_array(self.grafo, nodelist=sorted(self.grafo.nodes()), dtype=int)
        messagebox.showinfo("Matriz de Adjacência", str(matriz))

    #  ======================================= Função para criar um grafo a partir de uma matriz fornecida pelo usuário =========================================
    def criar_grafo_da_matriz(self):
        """Cria um grafo a partir de uma matriz de adjacência informada pelo usuário."""
        def obter_matriz_multilinha():
            top = tk.Toplevel(self.janela)
            top.title("Digite a matriz de adjacência")

            tk.Label(top, text="Digite a matriz de adjacência no seguinte modelo:\n Exemplo: \n\n 0 1 0\n1 0 1").pack()

            text = tk.Text(top, width=30, height=10)
            text.pack()

            resultado = []

            def confirmar():
                nonlocal resultado
                resultado = text.get("1.0", tk.END).strip().split("\n")
                top.destroy()

            tk.Button(top, text="Confirmar", command=confirmar).pack()
            top.grab_set()  # Foco no Toplevel até ser fechado
            self.janela.wait_window(top)

            return "\n".join(resultado) if resultado else None

        matriz_str = obter_matriz_multilinha()
        if not matriz_str:
            return

        self.grafo.clear()
        linhas = matriz_str.strip().split("\n")
        matriz = np.array([[int(num) for num in linha.split()] for linha in linhas])

        self.nos = []
        for i in range(len(matriz)):
            self.grafo.add_node(i + 1)
            self.nos.append((i + 1, 100 + i * 50, 200))

        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if matriz[i][j] > 0:
                    self.grafo.add_edge(i + 1, j + 1, weight=matriz[i][j])

        self.mostrar_grafo()

    #  ======================================= Função para buscar caminhos no grafo =============================================================================
    def buscar_caminhos(self):
        origem = simpledialog.askinteger("Origem", "Digite o nó de origem:", parent=self.janela)
        destino = simpledialog.askinteger("Destino", "Digite o nó de destino:", parent=self.janela)

        if origem not in self.grafo.nodes or destino not in self.grafo.nodes:  # Verifica se os nós existem
            messagebox.showerror("Erro", "Nó inválido!")  # Exibe erro caso algum nó seja inválido
            return

        try:
            # Calcula o menor caminho e o peso entre origem e destino
            menor_caminho = nx.shortest_path(self.grafo, source=origem, target=destino, weight='weight')
            menor_peso = nx.shortest_path_length(self.grafo, source=origem, target=destino, weight='weight')
        except nx.NetworkXNoPath:
            menor_caminho, menor_peso = "Nenhum", "N/A"  # Caso não haja caminho

        caminhos_possiveis = list(nx.all_simple_paths(self.grafo, origem, destino))  # Lista todos os caminhos possíveis
        maior_caminho = max(caminhos_possiveis, key=len, default="Nenhum")  # Encontra o maior caminho

        # Exibe o resultado
        resultado = (f"Caminhos possíveis: {caminhos_possiveis}\n\n"
                     f"Menor caminho: {menor_caminho} - (Peso: {menor_peso})\n"
                     f"Maior caminho: {maior_caminho}")

        messagebox.showinfo("Resultados", resultado)

    #  ======================================= Função para mostrar o grafo visualmente utilizando a biblioteca NetworkX =========================================
    def mostrar_grafo(self):
        """Mostra o grafo visualmente usando NetworkX."""
        pos = {no[0]: (no[1], no[2]) for no in self.nos}
        nx.draw(self.grafo,
                pos = pos,
                with_labels = True,
                node_color = "black", #random.choice(cor_dos_nos)
                node_size = 500,
                font_weight = "bold",
                font_color = "White",
                style = 'dashdot'
                )

        if self.valorado:
            edge_labels = nx.get_edge_attributes(self.grafo, "weight")
            nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels = edge_labels, font_color = "Blue", font_weight = "800", font_size = 14, font_family = "Times New Roman")

        plt.show()

    #  ======================================= Função principal que inicia a interface gráfica ==================================================================
    def iniciar(self):
        self.janela.mainloop()  # Inicia o loop da janela principal da interface gráfica