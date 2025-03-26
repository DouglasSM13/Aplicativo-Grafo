import tkinter as tk  # Biblioteca para criação de janelas
from tkinter import simpledialog, messagebox  # São como os 'alert's do Javascript, mas em formato de janela
import networkx as nx  # Biblioteca para criar e manipular grafos e network
import matplotlib.pyplot as plt  # Biblioteca para criar visualizações estáticas, animadas e/ou interativas em Python
import numpy as np  # Essa é famosa para Data Science, mas tou usando aqui pra lidar com as matrizes
import random  # Isso aqui é para randomizar a cor dos nós


# ======================================= INÍCIO DO CÓDIGO =============================================================

# CLASSE PRINCIPAL DO APLICATIVO
class GrafoApp:
    def __init__(self):  # CRIANDO O CONSTRUTOR
        self.janela = tk.Tk()  # INSTANCIANDO O OBJETO
        self.janela.title("CONSTRUTOR DE GRAFOS - TRABALHO TEORIA DE GRAFOS")  # E DEFININDO O TÍTULO DA JANELA

        self.canvas = tk.Canvas(self.janela, width=1200, height=800,
                                bg="white")  # TAMANHO E COR DE FUNDO DA TELA DO DESENHO
        self.canvas.pack()  # CRIA O CANVAS (AREA DE DESENHO)

        # ==========  BOTÕES QUE APARECEM NO CANTO INFERIOR DA TELA: ==================================================

        # Mostrar Matriz do Grafo Desenhado ========================================
        self.botao_matriz = tk.Button(self.janela,
                                      text="Mostrar Matriz de Adjacência do Grafo",
                                      command=self.mostrar_matriz)
        self.botao_matriz.pack(side=tk.LEFT, padx=10, pady=10)

        # Criar Grafo a partir de uma Matriz ========================================
        self.botao_construir = tk.Button(self.janela,
                                         text="Criar Grafo a partir de uma Matriz",
                                         command=self.criar_grafo_da_matriz)
        self.botao_construir.pack(side=tk.LEFT, padx=10, pady=10)

        # Buscar Caminhos ===========================================================
        self.botao_caminhos = tk.Button(self.janela,
                                        text="Buscar Caminhos",
                                        command=self.buscar_caminhos)
        self.botao_caminhos.pack(side=tk.LEFT, padx=10, pady=10)

        # Mostrar Grafo ============================================================
        self.botao_mostrar_grafo = tk.Button(self.janela,
                                             text="Mostrar Grafo",
                                             command=self.mostrar_grafo)
        self.botao_mostrar_grafo.pack(side=tk.LEFT, padx=10, pady=10)

        # COMO USAR ================================================================
        self.botao_como_usar = tk.Button(self.janela,
                                         text="Como usar o aplicativo",
                                         command=self.mostrar_como_usar)
        self.botao_como_usar.pack(side=tk.RIGHT, padx=10, pady=10)

        # PERGUNTA ANTES DO DESENHO PARA SABER SE O GRÁFICO SERÁ OU NÃO ORIENTADO E SE SERÁ OU NÃO VALORADO :

        self.orientado = messagebox.askyesno("Grafo Orientado", "Deseja criar um grafo orientado?")
        self.valorado = messagebox.askyesno("Grafo Valorado", "O gráfico será valorado?")

        self.grafo = nx.DiGraph() if self.orientado else nx.Graph()  # GRAFO DIRECIONAL CASO ORIENTADO = TRUE, SENÃO, GRAFO NÃO DIRECIONADO
        self.nos = []  # CRIAÇÃO DA LISTA DE NÓS
        self.arestas = []  # CRIAÇÃO DA LISTA DE ARESTAS

        # Mapeia os eventos de clique para os métodos
        self.canvas.bind("<Button-1>", self.adicionar_no)  # Botão1 É O CLIQUE ESQUERDO DO MOUSE
        self.canvas.bind("<Button-3>", self.adicionar_aresta)  # Botão2 É O CLIQUE DIREITO DO MOUSE

    # CRIAÇÃO DA FUNÇÃO PARA CRIAR OS NÓS:
    def adicionar_no(self, evento):
        """Adiciona um nó ao clicar na tela."""

        light_colors = ['Yellow', 'Lightblue', 'Green', 'Orange', 'Pink', 'Aqua',
                        'White']  # CORES ALEATÓRIAS PARA OS NÓS
        x, y = evento.x, evento.y  # DEFINE A POSIÇÃO DO MOUSE DENTRO DO CANVA (A TELA DO APLICATIVO)
        id_no = len(self.nos) + 1  # ESSE É O NÚMERO QUE APARECE DENTRO DOS NÓS, É UM ID UNICO, UM INDEX
        self.nos.append((id_no, x,
                         y))  # ADICIONA UMA TUPLA NA LISTA (self.nos), com a informação das cordenadas do nó (x,y) e o index dele (id_no)
        self.grafo.add_node(id_no, pos=(
        x, y))  # ADICIONA A BOLINHA REPRESENTANDO O NÓ, COM O NÚMERO DENTRO DELA (ID_NO), NA POSIÇÃO (X,Y)

        self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=random.choice(
            light_colors))  # CRIA A BOLINHA NA POSIÇÃO INFORMADA, NA COR ALEATÓRIA, NO TAMANHO 15X15
        self.canvas.create_text(x, y, text=str(id_no), font=(
        "Comic Sans MS", 15, "bold"))  # BOTA O NÚMERO DENTRO DA BOLINHA, NESSA FONTE E TAMANHO 15PX

    # Criação da Função para criar as arestas:
    def adicionar_aresta(self, evento):
        """Adiciona uma aresta entre nós ao clicar com o botão direito."""

        peso = 0.0
        if len(self.nos) < 2:  # SE TIVER MENOS DE 2 NÓS DESENHADOS:
            return  # NÃO FAÇA NADA

        x, y = evento.x, evento.y  # CAPTURA A POSIÇÃO DOS CLIQUES COM O BOTÃO DIREITO
        distancia_minima = float(
            "infinity")  # Lê toda a tela de desenho e procura pelo nó mais próximo do clique com o botão direito
        no_mais_proximo = None  # Armazena o identificador do nó mais próximo do clique

        # ===== AQUI FICA UM POUCO MAIS COMPLEXO, VOU EXPLICAR LINHA A LINHA =====

        for no in self.nos:  # PERCORRE TODOS OS NÓS DESENHADOS, E EM CADA UM:
            dist = ((x - no[1]) ** 2 + (y - no[
                2]) ** 2) ** 0.5  # CALCULA A FUNÇÃO EUCLIDIANA (DISTANCIA ENTRE 2 PONTOS) E ATRIBUI ESSE VALOR À VARIÁVEL
            # ** 0.5 É A RAIZ QUADRADA PARA SABER A DISTÂNCIA REAL

            if dist < distancia_minima:  # SE A DISTÂNCIA FOR MENOR QUE A DISTÂNCIA MÍNIMA:
                distancia_minima = dist  # DISTÂNCIA MÍNIMA RECEBE O RESULTADO DA FUNÇÃO EUCLIDIANA
                no_mais_proximo = no[0]  # SALVA O ID DO NÓ MAIS PRÓXIMO NESSA VARIÁVEL

        if no_mais_proximo not in self.arestas:  # SE O NÓ MAIS PRÓXIMO *NÃO* ESTIVER NA LISTA "ARESTAS"
            if len(self.arestas) == 0:  # SE A LISTA ESTIVER VAZIA (NO PRIMEIRO CLIQUE), o nó mais próximo é registrado como origem potencial da aresta.
                self.arestas.append(no_mais_proximo)  # ADICIONA O "no_mais_proximo" na lista de arestas

            else:  # SE A LISTA *NÃO* ESTIVER VAZIA, OU SEJA, SE JÁ EXISTIR UM NÓ NA LISTA:
                origem = self.arestas.pop()  # O nó anteriormente registrado é considerado origem (Botão 1)
                destino = no_mais_proximo  # e o nó atual é o destino (Botão 2)

                if self.valorado:
                    peso = simpledialog.askinteger("Peso da aresta",
                                                   f"DIGITE O PESO DA ARESTA ENTRE O NÓ {origem} AO NÓ {destino}:",
                                                   parent=self.janela)  # Mensagem de peso da aresta
                    self.arestas.clear()  # Limpa a lista de arestas, após adicionada

                    self.grafo.add_edge(origem, destino, weight=peso)  # Adiciona o valor do peso na linha da aresta

                # Desenho da aresta considerando grafo orientado ou não
                x1, y1 = self.nos[origem - 1][1], self.nos[origem - 1][2]  # Pega as coordenadas de x e y do nó de origem
                x2, y2 = self.nos[destino - 1][1], self.nos[destino - 1][2]  # Pega as coordenadas de x e y do nó de destino

                #  SE O GRAFO FOR ORIENTADO, ADICIONA UMA SETA NO FIM DA LINHA, SE NÃO, NÃO ADICIONA A SETA:
                self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST) \
                    if self.orientado else self.canvas.create_line(x1, y1, x2, y2)

                if self.valorado:  # Exibe o peso no centro da aresta se o grafo for valorado
                    self.canvas.create_text((x1 + x2) // 2,  # No meio da linha horizontalmente
                                            (y1 + y2) // 2 - 10,  # No meio da linha, um pouco acima, verticalmente
                                            text=str(peso),
                                            font=("Times New Roman", 14, "bold"),
                                            fill="Red")

    def mostrar_matriz(self):
        """Exibe a matriz de adjacência do grafo em uma janela personalizada."""

        # Cria uma nova janela para exibir a matriz
        janela_matriz = tk.Toplevel(self.janela)
        janela_matriz.title("Matriz de Adjacência")
        janela_matriz.geometry("400x200")  # Define o tamanho da janela

        # Obtém a matriz de adjacência
        matriz = nx.to_numpy_array(self.grafo, nodelist=sorted(self.grafo.nodes()), dtype=int)

        # Cria um widget Text para exibir a matriz
        texto_matriz = tk.Text(janela_matriz, wrap=tk.WORD, font=("Courier New", 32))
        texto_matriz.pack(expand=True, fill=tk.BOTH)

        # Insere a matriz no widget Text
        texto_matriz.insert(tk.END, str(matriz))

        # Torna o widget apenas para leitura
        texto_matriz.config(state=tk.DISABLED)

        # Adiciona um botão para fechar a janela
        # botao_fechar = tk.Button(janela_matriz, text="Fechar", command=janela_matriz.destroy)
        # botao_fechar.pack(pady=10)

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

    def buscar_caminhos(self):
        """Exibe os caminhos possíveis, o menor e o maior caminho."""
        origem = simpledialog.askinteger("Origem", "Digite o nó de origem:", parent=self.janela)
        destino = simpledialog.askinteger("Destino", "Digite o nó de destino:", parent=self.janela)

        if origem not in self.grafo.nodes or destino not in self.grafo.nodes:
            messagebox.showerror("Erro", "Nó inválido!")
            return

        try:
            menor_caminho = nx.shortest_path(self.grafo, source=origem, target=destino, weight='weight')
            menor_peso = nx.shortest_path_length(self.grafo, source=origem, target=destino, weight='weight')
        except nx.NetworkXNoPath:
            menor_caminho, menor_peso = "Nenhum", "N/A"

        caminhos_possiveis = list(nx.all_simple_paths(self.grafo, origem, destino))
        maior_caminho = max(caminhos_possiveis, key=len, default="Nenhum")

        resultado = (f"Caminhos possíveis: {caminhos_possiveis}\n"
                     f"Menor caminho: {menor_caminho} (Peso: {menor_peso})\n"
                     f"Maior caminho: {maior_caminho}")

        messagebox.showinfo("Resultados", resultado)

    def mostrar_grafo(self):
        """Desenha o grafo atual."""
        pos = nx.spring_layout(self.grafo)  # Calcula a posição dos nós para desenhá-los
        nx.draw(
            self.grafo,
            pos,
            with_labels=True,  # Exibe os rótulos dos nós
            node_color="Yellow",  # Cor dos nós
            node_size=500,  # Tamanho dos nós
            font_weight='bold',  # Negrito nas labels
            arrows=self.orientado  # Exibe as setas caso o grafo seja orientado
        )

        # Obtém os rótulos das arestas baseados no peso
        edge_labels = nx.get_edge_attributes(self.grafo, 'weight')
        nx.draw_networkx_edge_labels(self.grafo, pos, edge_labels=edge_labels, font_size=12, font_color="Red")  # Exibe os rótulos das arestas
        plt.show()

        # Função para mostrar como usar o aplicativo

    def mostrar_como_usar(self):
        messagebox.showinfo("Como usar",
                            "COMO USAR:\n\n"
                            "1. Clicando com o botão esquerdo do mouse você desenha os nós do grafo\n\n"

                            "2. Após definir os nós, clique com o botão direito do mouse do nó 1 (Nó de origem) "
                            "ao nó 2 (Nó de destino) para desenhar uma aresta entre eles. (Caso você tenha optado por "
                            "um grafo VALORADO, após definir o nó de destino será apresentado uma caixa para adicionar "
                            "o peso (Rótulo) da aresta!\n\n"

                            "3. Após desenhado o gráfico, você pode escolher uma das opções inferiores para brincar com esse gráfico! \n\n"
                            "Sinta-se a vontade para explorar!"
                            )

    def iniciar(self):
        self.janela.mainloop()


if __name__ == "__main__":
    app = GrafoApp()
    app.iniciar()
