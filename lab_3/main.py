from math import inf
from typing import Dict, List
from copy import deepcopy

def belman_ford(G : Dict, s):
    # tablica przekodowań
    tab_encode = [i for i in G.keys()]
    """
    dla każdego wierzchołka v w V[G] wykonaj
    d[v] = nieskończone
     poprzednik[v] = niezdefiniowane
    """
    d = [inf for i in G.keys()]
    p = [-1 for i in G.keys()]
    # d[s] = 0
    d[tab_encode.index(s)] = 0
    # dla i od 1 do |V[G]| - 1 wykonaj + dla sprawdzenia cykli ujemnych
    for i in range(len(G.keys())):
        d_prev = deepcopy(d)
        # dla każdej krawędzi (u,v) w E[G] wykonaj
        for j in G.keys():
            for k in G[j]:
                # jeżeli d[v] > d[u] + w(u,v) to
                if d[tab_encode.index(k[0])] > d[tab_encode.index(j)] + k[1]:
                    # d[v] = d[u] + w(u,v)
                    d[tab_encode.index(k[0])] = d[tab_encode.index(j)] + k[1]
                    # poprzednik[v] = u
                    p[tab_encode.index(k[0])] = j
        # wcześniejsze zakończenie algorytmu z uwagi na brak zmian
        if d_prev == d:
            break
    else:
        # zmiany były w n- tym kroku algorytmu:
        raise ValueError("ujemne cykle")
    return d,p

def dijkstra(G : Dict[int , List], s):
    # tablica przekodowań
    tab_encode = [i for i in G.keys()]
    """
    dla każdego u ∈ V
    d[u] ← ∞
    p[u] ← 0
    """
    d = [inf for i in G.keys()]
    p = [0 for i in G.keys()]
    # Q ← V
    Q = list(G.keys())
    # Q ← Q-{s}
    Q.remove(s)
    #p[s] ← -1
    #d[s] ← 0
    p[tab_encode.index(s)] =  -1
    d[tab_encode.index(s)] = 0
    # u* ← s
    u_prim = s
    # dopóki Q ≠ Ø
    while Q != []:
        # dla każdego (u ∈ Q i u ∈ N[u*])
        for u in Q:
            if u in (list(zip(*G[u_prim]))[0] if G[u_prim] != [] else []):
                # jeśli d[u*]+a(u*,u)<d[u] to d[u] ← d[u*]+a(u*,u); p[u] ← u*
                if d[tab_encode.index(u_prim)] + G[u_prim][list(zip(*G[u_prim]))[0].index(u)][1] < d[tab_encode.index(u)]:
                    d[tab_encode.index(u)] = d[tab_encode.index(u_prim)] + G[u_prim][list(zip(*G[u_prim]))[0].index(u)][1]
                    p[tab_encode.index(u)] = u_prim
        # dla każdego u ∈ Q
        u_prim = Q[0]
        for u in Q:
            # u* ← arg min (d[u])
            if d[tab_encode.index(u)]<d[tab_encode.index(u_prim)]:
                u_prim = u
        # Q ← Q-{u*}
        Q.remove(u_prim)
    # zwróć (dla każdego u ∈ V: d[u])
    return d,p


def johson(G):
    G_copy = deepcopy(G)
    # dodaj wierzchołek 0 z połączeniami o koszcie 0 z pozostałymi wierzchołkami
    G_copy[0] = [[i,0]for i in G.keys()]
    try:
        # wyznaczenie wag wierzchołków z alg belmana forda
        d,_ = belman_ford(G_copy,0)
    except ValueError as msg:
        # obsługa ujemnych cykli
        return msg
    # usunięcie wierzchołka 0 z grafu
    G_copy.pop(0)
    tab_encode = [i for i in G.keys()]
    # modyfikacja wag krawędzi
    d = d[:-1]
    for index,k in enumerate(G.keys()):
        for i in range(len(G[k])):
            # Obliczamy dla każdej krawędzi modyfikację wag
            G_copy[k][i][1] +=  d[tab_encode.index(k)] - d[tab_encode.index(G[k][i][0])]
    # słownik rozwiązań dijkstry dla wszystkich wierzchołków startowych
    rozw = {}
    for i in G_copy.keys():
        # dijkstra
        rozw[i] = dijkstra(G_copy,i)
    return rozw

def get_path(G,G_johnsosn, begin, end):
    # encode
    tab_encode = [i for i in G.keys()]
    # tab krotka zawierająca ścierzki z punktu początkowego
    tab = G_johnsosn[begin]
    # sprawdzenie warunku na istnienie ścieżki
    if tab[0][tab_encode.index(end)] == inf: return "sciezka nie istnieje"
    # liczenie kosztu ścierzki w razie gdyby był ujemny oraz zapis ścieżki w strr
    strr = f'{end}'
    # temp kolejne kawałki ścierzki w odwrotnej kolejności
    temp = end
    sum = 0
    while temp != begin:
        sum += G[tab[1][tab_encode.index(temp)]][list(zip(*G[tab[1][tab_encode.index(temp)]]))[0].index(temp)][1]
        temp = tab[1][tab_encode.index(temp)]
        strr = f'{temp}->' + strr
    # zwrot ścierzki, koszt nieujemny (minimalnie 0), koszt rzeczywisty (możliwość wystąpienia kosztu ujemnego)
    return strr , tab[0][tab_encode.index(end)], sum


G = { 1:[[2,-1],[5,-2],[7,4],[11,2]],
2:[[8,3],[6,4],[9,-3],[7,0]],
3:[[4,-5],[8,-4],[7,-2]],
4:[[2,9],[5,6]],
5:[[3,2]],
6:[[9,8]],
7:[[4,3]],
8:[[7,6]],
9:[[11,5]],
10:[[3,1],[1,2]],
11:[[10,-1]]
}

G = {
1: [[2,-2]],
2: [[3,-1]],
3: [[1,4],[4,2],[5,-3]],
4: [],
5: [],
6: [[4,1],[5,-4]]
}
#G[0] = [[i,0]for i in G.keys()]
G_dikstra = {
1:[[2,4]],
2:[[3,11],[4,9]],
3:[[1,8]],
4:[[5,2],[6,6]],
5:[[2,8],[7,7],[8,4]],
6:[[3,1],[5,5]],
7:[[8,14],[9,9]],
8:[[6,2],[9,10]],
9:[]
}
#print(dijkstra(G_dikstra,1))


##  ujemny cykl
G = { 1:[[2,-1],[5,-2],[7,4],[11,2]],
2:[[6,4],[8,3],[9,-3],[7,0]],
3:[[4,-5],[8,-4],[7,-2]],
4:[[1,4],[2,9],[5,6]],
5:[[3,2]],
6:[[9,8]],
7:[[4,3]],
8:[[7,6]],
9:[[11,5]],
10:[[3,1],[1,2]],
11:[[10,-1]]
}
## niespojny
G = { 1:[[2,-1],[5,-2],[7,4]],
2:[[8,3],[7,0]],
3:[[4,-5],[8,-4],[7,-2]],
4:[[2,9],[5,6]],
5:[[3,2]],
6:[[9,8]],
7:[[4,3]],
8:[[7,6]],
9:[[11,5]],
10:[[3,1],[1,2]],
11:[]
}
## normalne
G = { 1:[[2,-1],[5,-2],[7,4],[11,2]],
2:[[6,4],[8,3],[9,-3],[7,0]],
3:[[4,-5],[8,-4],[7,-2]],
4:[[2,9],[5,6]],
5:[[3,2]],
6:[[9,8]],
7:[[4,3]],
8:[[7,6]],
9:[[11,5]],
10:[[3,1],[1,2]],
11:[[10,-1]]
}

##
temp = johson(G)
print(temp)
if type(temp) == dict:
    print(f"     nr v początkowego    =========== koszt ==================|================ poprzedniki =========")
    for k,v in temp.items():
        print(f"            {k}            : {v}")

    print(get_path(G, temp, 6, 11))
