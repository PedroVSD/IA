import time
import psutil
import os
from collections import deque

process = psutil.Process(os.getpid())

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

class EightPuzzleProblem:
    def __init__(self, initial, goal):
        self.initial = tuple(initial)
        self.goal = tuple(goal)

    def is_goal(self, state):
        return state == self.goal

    def actions(self, state):
        index = state.index(0)
        row, col = divmod(index, 3)
        moves = []
        if row > 0: moves.append('up')
        if row < 2: moves.append('down')
        if col > 0: moves.append('left')
        if col < 2: moves.append('right')
        return moves

    def result(self, state, action):
        index = state.index(0)
        new_state = list(state)
        swap_index = index

        if action == 'up': swap_index = index - 3
        elif action == 'down': swap_index = index + 3
        elif action == 'left': swap_index = index - 1
        elif action == 'right': swap_index = index + 1

        new_state[index], new_state[swap_index] = new_state[swap_index], new_state[index]
        return tuple(new_state)

    def action_cost(self, state, action, result):
        return 1

def expand(problem, node):
    children = []
    for action in problem.actions(node.state):
        s_prime = problem.result(node.state, action)
        cost = node.path_cost + problem.action_cost(node.state, action, s_prime)
        child = Node(state=s_prime, parent=node, action=action, path_cost=cost, depth=node.depth + 1)
        children.append(child)
    return children

def breadth_first_search(problem):
    start_time = time.time()
    root = Node(problem.initial)
    frontier = deque([root])
    reached = set([root.state])

    stats = {
        "nodes_generated": 1,
        "fringe_size": 1,
        "max_fringe_size": 1,
        "max_search_depth": 0
    }

    while frontier:
        stats["max_fringe_size"] = max(stats["max_fringe_size"], len(frontier))
        node = frontier.popleft()
        if problem.is_goal(node.state):
            return node, finalize_stats(stats, start_time)
        for child in expand(problem, node):
            stats["nodes_generated"] += 1
            stats["max_search_depth"] = max(stats["max_search_depth"], child.depth)
            if child.state not in reached:
                reached.add(child.state)
                frontier.append(child)
                stats["fringe_size"] = len(frontier)

    return None, finalize_stats(stats, start_time)

def depth_first_search(problem, limit=None):
    start_time = time.time()
    root = Node(problem.initial)
    stack = [root]
    reached = set([root.state])

    stats = {
        "nodes_generated": 1,
        "fringe_size": 1,
        "max_fringe_size": 1,
        "max_search_depth": 0
    }

    while stack:
        stats["max_fringe_size"] = max(stats["max_fringe_size"], len(stack))
        node = stack.pop()
        if problem.is_goal(node.state):
            return node, finalize_stats(stats, start_time)
        if limit is None or node.depth < limit:
            for child in reversed(expand(problem, node)):
                if child.state not in reached:
                    reached.add(child.state)
                    stack.append(child)
                    stats["nodes_generated"] += 1
                    stats["max_search_depth"] = max(stats["max_search_depth"], child.depth)
                    stats["fringe_size"] = len(stack)

    return None, finalize_stats(stats, start_time)

def iterative_deepening_search(problem, max_depth=100):
    start_time = time.time()
    total_nodes = 0
    max_depth_reached = 0
    max_fringe = 0
    final_solution = None

    for depth in range(max_depth + 1):
        result, stats = depth_first_search(problem, limit=depth)
        total_nodes += stats.get("nodes_generated", 0)
        max_depth_reached = max(max_depth_reached, stats.get("max_search_depth", 0))
        max_fringe = max(max_fringe, stats.get("max_fringe_size", 0))
        if result:
            stats["nodes_generated"] = total_nodes
            stats["max_search_depth"] = max_depth_reached
            stats["max_fringe_size"] = max_fringe
            return result, finalize_stats(stats, start_time)

    stats = {
        "nodes_generated": total_nodes,
        "fringe_size": 0,
        "max_fringe_size": max_fringe,
        "max_search_depth": max_depth_reached
    }
    return None, finalize_stats(stats, start_time)

def finalize_stats(stats, start_time):
    stats["running_time"] = time.time() - start_time
    stats["memory_usage"] = process.memory_info().rss / 1024 / 1024
    return stats

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def print_solution(node):
    if not node:
        print("Falha na busca.")
        return
    path = []
    while node:
        path.append(node)
        node = node.parent
    print(f"Solução encontrada em {len(path) - 1} passos:")
    for step in reversed(path):
        print_state(step.state)

def print_stats(stats):
    print(f"Tempo: {stats['running_time']:.4f}s")
    print(f"Nódos gerados: {stats['nodes_generated']}")
    print(f"Tamanho final da fronteira: {stats.get('fringe_size', 0)}")
    print(f"Tamanho máximo da fronteira: {stats['max_fringe_size']}")
    print(f"Profundidade máxima atingida: {stats['max_search_depth']}")
    print(f"Uso de memória: {stats['memory_usage']:.2f} MB")

# =============================
# 🚀 EXEMPLO DE USO
# =============================
if __name__ == "__main__":
    initial = [1, 3, 6, 5, 0, 2, 4, 7, 8]

#[1, 3, 6, 5, 0, 2, 4, 7, 8]
#[7, 4, 0, 1, 2, 5, 6, 8, 3]
#[0, 5, 1, 6, 4, 3, 8, 2, 7]
#[8, 7, 6, 5, 4, 3, 2, 1, 0]

    goal = [1, 2, 3,
            4, 5, 6,
            7, 8, 0]

    problem = EightPuzzleProblem(initial, goal)

    print("=== BFS ===")
    bfs_solution, bfs_stats = breadth_first_search(problem)
    print_solution(bfs_solution)
    print_stats(bfs_stats)

    print("\n=== DFS (com pilha) ===")
    dfs_solution, dfs_stats = depth_first_search(problem, limit=20)
    print_solution(dfs_solution)
    print_stats(dfs_stats)

    print("\n=== IDS ===")
    ids_solution, ids_stats = iterative_deepening_search(problem, max_depth=20)
    print_solution(ids_solution)
    print_stats(ids_stats)







    import time
import psutil  # Biblioteca para medir uso de memória
from collections import deque

class Node:
    def __init__(self, estado, pai=None, acao="", custo=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

# Direções e movimentos possíveis
movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
direcao = ["cima", "baixo", "esquerda", "direita"]

# Estado objetivo final
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

# DFS com pilha (iterativa)
def dfs(root, limite=100):
    inicio = time.time()
    pilha = [root]
    visitado = set()
    visitado.add(tuple(map(tuple, root.estado)))

    nodes_expanded = 0
    max_search_depth = 0

    while pilha:
        node = pilha.pop()
        nodes_expanded += 1

        if chegou_objetivo(node.estado):
            tempo = time.time() - inicio
            memoria = psutil.Process().memory_info().rss / (1024 * 1024)
            return node, nodes_expanded, max_search_depth, tempo, memoria

        if node.custo < limite:
            filhos = expandir(node)
            for filho in reversed(filhos):
                filho_estado = tuple(map(tuple, filho.estado))
                if filho_estado not in visitado:
                    visitado.add(filho_estado)
                    pilha.append(filho)
                    max_search_depth = max(max_search_depth, filho.custo)

    tempo = time.time() - inicio
    memoria = psutil.Process().memory_info().rss / (1024 * 1024)
    return None, nodes_expanded, max_search_depth, tempo, memoria

# IDS com DFS limitada
def dls(root, limite):
    return dfs(root, limite)[0]  # Retorna apenas o node

def ids(root):
    inicio = time.time()
    profundidade_maxima = 100
    memoria = 0
    for limite in range(profundidade_maxima):
        resultado = dls(root, limite)
        memoria = psutil.Process().memory_info().rss / (1024 * 1024)
        if resultado:
            tempo = time.time() - inicio
            return resultado, limite, tempo, memoria
    return None, profundidade_maxima, time.time() - inicio, memoria

# Tabuleiro de entrada
tabuleiro = [
    [8, 7, 6],
    [5, 4, 3],
    [2, 1, 0]
]


raiz = Node(tabuleiro)

# Execução da BFS
solucao, nodes_expanded, fringe_size, max_fringe_size, search_depth, max_search_depth, tempo_decorrido, memoria_uso = bfs(raiz)

# Execução da DFS
solucao_dfs, nodes_expanded_dfs, max_depth_dfs, tempo_dfs, memoria_dfs = dfs(raiz)

# Execução da IDS
solucao_ids, profundidade_ids, tempo_ids, memoria_ids = ids(raiz)

# Impressão dos resultados
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

    print("\n=== Solução por DFS (com pilha iterativa) ===")
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
