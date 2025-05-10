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
