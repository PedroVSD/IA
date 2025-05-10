def heuristica_Manhattan(estado):
  distancia = 0
  for i in range(3):
    for j in range(3):
      valor = estado[i][j]
      if valor != 0:
        linha_obj, col_obj = divmod(valor -1, 3)
        distancia += abs(i - linha_obj) + abs(j - col_obj)
  return distancia

def h(no):
    return heuristica_Manhattan(no.estado)

"""# Busca gulosa"""

def bfs_gulosa(root):
    inicio_tempo = time.time()

    fronteira = []
    contador = count()
    heapq.heappush(fronteira, (h(root), next(contador), root))

    visitado = set()
    visitado.add(tuple(map(tuple, root.estado)))

    nodes_expanded = 0
    fringe_size = 1
    max_fringe_size = 1
    search_depth = 0
    max_search_depth = 0

    while fronteira:
        _, _, node = heapq.heappop(fronteira)
        nodes_expanded += 1

        if chegou_objetivo(node.estado):
            tempo_decorrido = time.time() - inicio_tempo
            memoria_uso = psutil.Process().memory_info().rss / (1024 * 1024)
            return node, nodes_expanded, len(fronteira), max_fringe_size, search_depth, max_search_depth, tempo_decorrido, memoria_uso

        for filho in expandir(node):
            filho_tupla = tuple(map(tuple, filho.estado))
            if filho_tupla not in visitado:
                visitado.add(filho_tupla)
                heapq.heappush(fronteira, (h(filho), next(contador), filho))

                fringe_size = len(fronteira)
                max_fringe_size = max(max_fringe_size, fringe_size)
                search_depth = filho.custo
                max_search_depth = max(max_search_depth, search_depth)


    memoria_uso = psutil.Process().memory_info().rss / (1024 * 1024)
    return None, nodes_expanded, len(fronteira), max_fringe_size, search_depth, max_search_depth, time.time() - inicio_tempo, memoria_uso