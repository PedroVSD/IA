# IA - 8-Puzzle Solver

Repositório de algoritmos de busca para o problema do 8-Puzzle.

## Estrutura

```
IA/
├── eight_puzzle/          # Projeto principal
│   ├── core/              # Estado, Node, Problem (domínio)
│   ├── search/            # Algoritmos: BFS, DFS, IDS, Gulosa, A*
│   ├── heuristics.py      # Manhattan, etc.
│   ├── utils.py           # Helpers de impressão e métricas
│   └── experiments/       # Scripts de execução/benchmark
├── tests/                 # Testes automatizados
├── legacy/                # Código original arquivado
└── requirements.txt
```

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
# Rodar benchmark com todos os algoritmos
python -m eight_puzzle.experiments.run_all

# Rodar um caso específico
python -m eight_puzzle.experiments.run_all --initial 1,3,6,5,0,2,4,7,8

# Rodar testes
pytest -q
```

## Algoritmos

- **BFS** - Busca em Largura (ótima, completa)
- **DFS** - Busca em Profundidade (com limite)
- **IDS** - Aprofundamento Iterativo (ótima com baixa memória)
- **Greedy** - Busca Gulosa (heurística Manhattan)
- **A*** - A Estrela (f = g + h, ótima com heurística admissível)
