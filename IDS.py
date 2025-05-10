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