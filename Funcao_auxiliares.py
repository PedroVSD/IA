import heapq
import queue
from itertools import count
import time
import psutil
from collections import deque

class Node:
    def __init__(self, estado, pai=None, acao="", custo=0):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo


movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
direcao = ["cima", "baixo", "esquerda", "direita"]


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