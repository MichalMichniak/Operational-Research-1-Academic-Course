from typing import Tuple,Dict,List
from cmath import inf

def DPA(G : Dict, s):
    # suma ← 0
    sum = 0
    # A ← Ø
    A = []
    """ 
    dla każdego u ∈ V
        alfa[u] ← 0
        beta[u] ← ∞
    """
    # alfa[u]: poprzednik wierzchołka u w MST
    alpha = [0 for i in G.keys()]
    # beta[u]: waga krawędzi łączącej u z MST (z wierzchołkiem alfa[u])
    beta = [inf for i in G.keys()]

    # Q: zbiór wierzchołków nienależących do MST
    # Q ← V
    Q : List= list(G.keys())
    # beta[s] ← 0
    beta[s] = 0
    # Q ← Q-{s}
    Q.remove(Q.index(s))
    # u_prim: ostatnio wybrany wierzchołek (w algorytmie jako u*)
    # u* ← s
    u_prim = s
    # dopóki Q ≠ Ø
    while Q != []:
        # dla każdego (u ∈ Q i u ∈ N[u*])
        for u in G[u_prim]:
            # jeśli a[u,u*]<beta[u] to alfa[u] ← u*; beta[u] ← a[u,u*]
            if (u[0] in Q) and (u[1]<beta[u[0]]):
                alpha[u[0]] = u_prim
                beta[u[0]] = u[1]
        # dla każdego u ∈ Q:
        #   u* ← arg min(beta[u])
        temp = inf
        for u in Q:
            if temp > beta[u]:
                u_prim = u
                temp = beta[u]
        # 
        if temp == inf: return "graf niespójny"
        # Q ← Q-{u*}
        Q.remove(u_prim)
        # A ← A+{alfa[u*],u*}
        A.append((alpha[u_prim],u_prim))
        # suma ← suma + a[alfa[u*],u*]
        sum += G[alpha[u_prim]][[i[0] for i in G[alpha[u_prim]]].index(u_prim)][1]
    # zwróć (A, suma)
    return A, sum
    pass

def is_directed(G : Dict):
    # Dla wszystkich krawędzi
    for v,e in G.items():
        for i in e:
            # Czy istnieje taka sama krawędź odpowiednio przypisana w drugą stronę
            if not ((v,i[1]) in G[i[0]]):
                return "skierowany"
    return "nieskierowany"

# lista sąsiedztwa
graf_list = {0:[(1,2),(2,1),(3,4),(4,3)] , 1:[(0,2),(3,3),(6,5)], 2:[(0,1),(3,7),(4,1),(5,2)], 3:[(0,4),(1,3),(2,7),(5,4),(6,4)], 4:[(0,3),(2,1),(5,3)], 5:[(2,2),(3,4),(4,3),(6,3)], 6:[(1,5),(3,4),(5,3)]}
graf_list = {   0:[(1,1),(2,5)],
                1:[(0,1),(3,3),(4,7)],
                2:[(0,5),(3,4),(5,9)],
                3:[(1,3),(2,4),(4,1),(5,2),(7,10)],
                4:[(1,7),(3,1)],
                5:[(2,9),(3,2),(6,6),(8,2)],
                6:[(5,6),(7,1),(9,2)],
                7:[(3,10),(6,1),(9,5)],
                8:[(5,2),(9,1)],
                9:[(6,2),(7,5),(8,1)]
            }
graf_list = {   0:[(1,1),(2,5)],
                1:[(0,1),(3,3),(4,7)],
                2:[(0,5),(3,4)],
                3:[(1,3),(2,4),(4,1)],
                4:[(1,7),(3,1)],
                5:[(6,6),(8,2)],
                6:[(5,6),(7,1),(9,2)],
                7:[(6,1),(9,5)],
                8:[(5,2),(9,1)],
                9:[(6,2),(7,5),(8,1)]
            }
graf_list = {   0:[(1,1),(2,5)],
                1:[(0,1),(3,3),(4,7)],
                2:[(0,5),(3,4),(5,9)],
                3:[(1,3),(2,4),(4,1),(5,2),(7,10)],
                4:[(1,7),(3,1)],
                5:[(2,9),(3,2),(6,6),(8,2)],
                6:[(5,6),(7,1),(9,2)],
                7:[(3,10),(6,1),(9,5)],
                8:[(5,2)],
                9:[(6,2),(7,5),(8,1)]
            }

print(is_directed(graf_list))
print(DPA(graf_list,0))
