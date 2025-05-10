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