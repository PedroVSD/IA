import time
import psutil  # Biblioteca para medir uso de memória
from collections import deque

class Node:
    def __init__(self, estado, pai=None, acao="", custo=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

# Direções e movimentos que podem ser feitas no tabuleiro, claro se houver a possibilidade
movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
direcao = ["cima", "direita", "baixo", "esquerda"]

# Como deve ficar o tabuleiro no final
objetivo_final = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def chegou_objetivo(estado):
    return estado == objetivo_final

def encontrar_zero(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j
    return -1, -1

def expandir(node):
    filhos = []
    x, y = encontrar_zero(node.estado)

    for i in range(4):
        nx, ny = x + movimentos[i][0], y + movimentos[i][1]
        if 0 <= nx < 3 and 0 <= ny < 3:
            novo_estado = [linha[:] for linha in node.estado]  # Copia a matriz
            novo_estado[x][y], novo_estado[nx][ny] = novo_estado[nx][ny], novo_estado[x][y]
            filhos.append(Node(novo_estado, node, direcao[i], node.custo + 1))
    return filhos

#Aqui é feita a BFS
def bfs(root):
    inicio_tempo = time.time()

    fronteira = deque([root])
    visitado = set()
    visitado.add(tuple(map(tuple, root.estado)))

    
    nodes_expanded = 0
    fringe_size = 1
    max_fringe_size = 1
    search_depth = 0
    max_search_depth = 0

    while fronteira:
        node = fronteira.popleft()
        nodes_expanded += 1

        if chegou_objetivo(node.estado):
            tempo_decorrido = time.time() - inicio_tempo
            memoria_uso = psutil.Process().memory_info().rss / (1024 * 1024)
            return node, nodes_expanded, fringe_size, max_fringe_size, search_depth, max_search_depth, tempo_decorrido, memoria_uso

        for filho in expandir(node):
            filho_tupla = tuple(map(tuple, filho.estado))
            if filho_tupla not in visitado:
                visitado.add(filho_tupla)
                fronteira.append(filho)

                fringe_size = len(fronteira)
                max_fringe_size = max(max_fringe_size, fringe_size)
                search_depth = filho.custo
                max_search_depth = max(max_search_depth, search_depth)

    memoria_uso = psutil.Process().memory_info().rss / (1024 * 1024)
    return None, nodes_expanded, fringe_size, max_fringe_size, search_depth, max_search_depth, time.time() - inicio_tempo, memoria_uso

def imprimir_caminho(node):
    if node is None:
        return []
    caminho = []
    while node.pai is not None:
        caminho.append(node.acao)
        node = node.pai
    caminho.reverse()
    return caminho

#Aqui é feita a DFS recursiva em pré ordem

def dfs_preorder(node, visitado, stats, limite=50):
    if chegou_objetivo(node.estado):
        return node

    if node.custo > limite:
        return None

    stats['nodes_expanded'] += 1
    visitado.add(tuple(map(tuple, node.estado)))

    for filho in expandir(node):
        filho_estado = tuple(map(tuple, filho.estado))
        if filho_estado not in visitado:
            stats['max_search_depth'] = max(stats['max_search_depth'], filho.custo)
            resultado = dfs_preorder(filho, visitado, stats, limite)
            if resultado:
                return resultado

    return None




def dfs(root, limite = 50):
  visitado = set()
  stats = {
    'nodes_expanded': 0,
    'max_search_depth': 0
  }

  inicio = time.time()
  resultado = dfs_preorder(root, visitado, stats, limite)
  tempo = time.time() - inicio
  memoria = psutil.Process().memory_info().rss / (1024 * 1024)

  return resultado, stats['nodes_expanded'], stats['max_search_depth'], tempo, memoria 

#Aqui é feita a IDS

def dls(root, limite):
    visitado = set()
    stats = {
        'nodes_expanded': 0,
        'max_search_depth': 0
    }

    resultado = dfs_preorder(root, visitado, stats, limite)
    if resultado:
        return resultado
    else:
        return "Fora"

def ids(root):
    inicio = time.time()
    profundidade_maxima = 50
    memoria = 0
    for limite in range(profundidade_maxima):
        resultado = dls(root, limite)
        memoria = psutil.Process().memory_info().rss / (1024 * 1024)
        if resultado != "Fora":
            tempo = time.time() - inicio
            return resultado, limite, tempo, memoria
    return None, profundidade_maxima, time.time() - inicio, memoria


# Abaixo é o tabuleiro a ser testado
tabuleiro = [
    [7, 4, 0],
    [1, 2, 5],
    [6, 8, 3]
]
# Abaixo alguns exemplos que testei
#[1, 3, 6, 5, 0, 2, 4, 7, 8]
#[7, 4, 0, 1, 2, 5, 6, 8, 3]
#[0, 5, 1, 6, 4, 3, 8, 2, 7]
#[8, 7, 6, 5, 4, 3, 2, 1, 0]


raiz = Node(tabuleiro)

#Execução da BFS
solucao, nodes_expanded, fringe_size, max_fringe_size, search_depth, max_search_depth, tempo_decorrido, memoria_uso = bfs(raiz)
#Execução da DFS
solucao_dfs, nodes_expanded_dfs, max_depth_dfs, tempo_dfs, memoria_dfs = dfs(raiz)
#Execução da IDS
solucao_ids, profundidade_ids, tempo_ids, memoria_ids = ids(raiz)

if solucao:
    path_to_go_bfs = imprimir_caminho(solucao)
    cost_of_path_bfs = solucao.custo

    print("\n=== Solução por BFS ===")
    print(f"Caminho da solução: {' -> '.join(path_to_go_bfs)}")
    print(f"Custo da solução: {cost_of_path_bfs}")
    print(f"Nós expandidos: {nodes_expanded}")
    print(f"Tamanho da fronteira: {fringe_size}")
    print(f"Tamanho máximo da fronteira: {max_fringe_size}")
    print(f"Profundidade da busca: {search_depth}")
    print(f"Profundidade máxima da busca: {max_search_depth}")
    print(f"Tempo de execução: {tempo_decorrido:.6f} segundos")
    print(f"Uso de memória: {memoria_uso:.2f} MB")
else:
    print("Nenhuma solução encontrada utilizando BFS.")

if solucao_dfs:
    path_to_go_dfs = imprimir_caminho(solucao_dfs)
    cost_of_path_dfs = solucao_dfs.custo

    print("\n=== Solução por DFS (recursiva pré-ordem) ===")
    print(f"Caminho da solução: {' -> '.join(path_to_go_dfs)}")
    print(f"Custo da solução: {cost_of_path_dfs}")
    print(f"Nós expandidos: {nodes_expanded_dfs}")
    print(f"Profundidade máxima da busca: {max_depth_dfs}")
    print(f"Tempo de execução: {tempo_dfs:.6f} segundos")
    print(f"Uso de memória: {memoria_dfs:.2f} MB")
else:
    print("\nNenhuma solução encontrada utilizando DFS.")

if solucao_ids:
    path_to_go_ids = imprimir_caminho(solucao_ids)
    cost_of_path_ids = solucao_ids.custo

    print("\n=== Solução por IDS (Busca Iterativa em Profundidade) ===")
    print(f"Caminho da solução: {' -> '.join(path_to_go_ids)}")
    print(f"Custo da solução: {cost_of_path_ids}")
    print(f"Profundidade da solução: {profundidade_ids}")
    print(f"Tempo de execução: {tempo_ids:.6f} segundos")
    print(f"Uso de memória: {memoria_ids:.2f} MB")
else:
    print("\nNenhuma solução encontrada utilizando IDS.")


