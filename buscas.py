from collections import deque


def expande(problema, node):

    filhos = []
    s = node.stade
    for acao in problema.acao(s):
        s_linha = problema.resultado(s, acao)
        custo = node.custo_caminho + problema.acao_custo(s, acao, s_linha)
        filhos = node(estado = s_linha, pai = node, acao = acao, custo_caminho = custo)

    return filhos

def bfs(problema):
    root = Node(problema.inicial)

    fronteira = deque[root]
    alcancado = set([root.estado])
