#include <iostream>
#include <queue>
#include <vector>
#include <set>
#include <map>
#include <algorithm>

using namespace std;

struct Node{
    vector<vector<int>> estado;
    Node* pai;
    string acao;
    int custo;

    Node(vector<vector<int>> s, Node* p = nullptr, string a = "", int c = 0) : estado(s), pai(p), acao(a), custo(c) {}
};

vector<pair<int, int>> movimentos = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
vector<string> direcao = {"cima","direita","baixo","esquerda"};

bool chegou_objetivo(int estado, int objetivo);
pair<int, int> encontrar_zero(vector<vector<int>> estado);
void imprimir_caminho(Node* node);


Node* bfs(Node* node);

vector<vector<int>> objetivo_final = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

int main(){

    vector<string> path_to_go = {};
    int cost_of_path = 0;
    int search_depth = 0;
    int nodes_expanded = 0;
    int fringe_size = 0;
    int max_fringe_size = 0;
    int max_search_depth = 0;
    float running_time = 0;
    float memory_usage = 0;

    return 0;
}

Node* bfs(Node* root){
    queue<Node*> fronteira;
    set<vector<vector<int>>> visitado;

    fronteira.push(root);
    visitado.insert(root->estado);


    while(!fronteira.empty()){
        Node* node = fronteira.front();
        fronteira.pop();


        if(chegou_objetivo(node->estado)){
            return node;
        }

        for (Node* filho : expandir(node)) {
            if (visitado.find(filho->estado) == visitado.end()) {
                visitado.insert(filho->estado);
                fronteira.push(filho);
            }
        }
    }

    return NULL;
}

bool chegou_objetivo(const vector<vector<int>>& estado){
    return estado == objetivo_final;
}

vector<Node*> expandir(Node* node) {
    vector<Node*> filhos;
    pair<int, int> pos = encontrar_zero(node->estado);
    int x = pos.first, y = pos.second;

    for (int i = 0; i < 4; i++) {
        int nx = x + movimentos[i].first;
        int ny = y + movimentos[i].second;

        if (nx >= 0 && nx < 3 && ny >= 0 && ny < 3) {
            vector<vector<int>> novo_estado = node->estado;
            swap(novo_estado[x][y], novo_estado[nx][ny]);
            filhos.push_back(new Node(novo_estado, node, direcao[i], node->custo + 1));
        }
    }
    return filhos;
}


pair<int, int> encontrar_zero(vector<vector<int>> estado){
    for(int i = 0; i < 3; i++){
        for(int j = 0; j < 3; j++){
            if(estado[i][j] == 0){
                return {i, j};
            }
        }
    }
    return {-1, -1};
}

void imprimir_caminho(Node* node) {
    if (node == nullptr) return;
    vector<string> caminho;
    while (node->pai != nullptr) {
        caminho.push_back(node->acao);
        node = node->pai;
    }
    reverse(caminho.begin(), caminho.end());
    cout << "Caminho da solução:\n";
    for (string acao : caminho) {
        cout << acao << " ";
    }
    cout << "\n";
}