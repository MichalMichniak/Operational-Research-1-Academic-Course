from cmath import inf
import random
import copy
def NEARIN(G, s):
    if G == {}: return [],0
    # wybrany początek drogi wstawienie do path
    path = [s,s]
    V = list(G.keys())
    #wierzchołki nie znajdujące się w sekwencji
    Q = copy.deepcopy(V)
    Q.remove(s)
    # wykonuj aż wszystkie wierzchołki nie będą w sekwencji (sekwencja ma mieć długość |V| + 1)
    while len(path) <= len(V):
        # wybierz najbliższy wierzchołek v (wierzhołek najbliższy od wierzchołków rozwiązania)
        v = Q[0]
        cost = inf
        for i in path:
            for j in G[i]:
                if cost>j[1] and (j[0] in Q):
                    cost = j[1]
                    v = j[0]
        # update wierzchołków nie w sekwencji
        Q.remove(v)
        # znadź miejsce pomiędzy którymi wierzchołkami koszt dołączenia nowo wybranego wierzchołka do sekwencji jest najtańszy
        next = path[1]
        cost = inf
        for i in range(len(path)-1):
            if (path[i+1] in list(zip(*G[v]))[0]) and (v in list(zip(*G[path[i]]))[0]):
                if cost > (x := G[path[i]][list(zip(*G[path[i]]))[0].index(v)][1] + G[v][list(zip(*G[v]))[0].index(path[i+1])][1]
                 - (G[path[i]][list(zip(*G[path[i]]))[0].index(path[i+1])][1] if path[i+1] in list(zip(*G[path[i]]))[0] else 0)):
                    
                    cost = x
                    next = i+1
                    pass
        # dołącz wierzchołek do sekwencji w najtańszym miejscu
        path.insert(next, v)
    # obliczenie całkowitego kosztu drogi
    total_cost = 0
    for i in range(len(path)-1):
        try:
            total_cost += G[path[i]][list(zip(*G[path[i]]))[0].index(path[i+1])][1]
        except:
            return path,"ścierzka nie istnieje"
    return path, total_cost

def to_graf( from_file : bool = True , lenghtt = 10):
    G = {}
    
    for i in range(lenghtt):
        G[i] = []
    Q = list(G.keys())[:len(G.keys())//2]
    if from_file:
        with open("graph.txt") as file:
            for i in file.readlines():
                G[int(i[0])].append((int(i[2]), int(i[4])))
    else:
        for i in G.keys():
            for j in G.keys():
                if i>j: continue
                if i!=j:
                    #if ((i in Q) and (j in Q)) or ((not (i in Q)) and (not (j in Q))):
                    if random.randint(3,11) >6:
                        weight = random.randint(3,11)
                        G[i].append((j, weight))
                        G[j].append((i, weight))
    print(G)
    print("\n\n\n\n")
          
    for i in G.keys():
        for j in G[i]:
            print(f"{i} {j[0]} {j[1]}")
    


def main():
    # negative weights
    graf_list = {0: [(1, 7), (2, -3), (3, 4), (4, -5), (5, 0), (6, -2), (7, 5), (8, 9), (9, -1)], 
                1: [(0, 7), (2, 7), (3, 4), (4, 5), (5, -4), (6, 3), (7, 4), (8, 5), (9, -4)], 
                2: [(0, -3), (1, 7), (3, 5), (4, -5), (5, 6), (6, 11), (7, -5), (8, 10), (9, 4)], 
                3: [(0, 4), (1, 4), (2, 5), (4, 8), (5, -4), (6, 8), (7, 1), (8, -2), (9, 1)], 
                4: [(0, -5), (1, 5), (2, -5), (3, 8), (5, 9), (6, 2), (7, 0), (8, -5), (9, -3)], 
                5: [(0, 0), (1, -4), (2, 6), (3, -4), (4, 9), (6, 11), (7, -5), (8, -3), (9, 9)], 
                6: [(0, -2), (1, 3), (2, 11), (3, 8), (4, 2), (5, 11), (7, 8), (8, 7), (9, 8)], 
                7: [(0, 5), (1, 4), (2, -5), (3, 1), (4, 0), (5, -5), (6, 8), (8, -1), (9, 4)], 
                8: [(0, 9), (1, 5), (2, 10), (3, -2), (4, -5), (5, -3), (6, 7), (7, -1), (9, 3)], 
                9: [(0, -1), (1, -4), (2, 4), (3, 1), (4, -3), (5, 9), (6, 8), (7, 4), (8, 3)]}

    # full graph       
    graf_list = {0: [(1, 2), (2, 9), (3, 8), (4, 10), (5, 4), (6, 10), (7, 7), (8, 4), (9, 1)], 
                1: [(0, 2), (2, 6), (3, 2), (4, 3), (5, 8), (6, 3), (7, 7), (8, 9), (9, 10)], 
                2: [(0, 9), (1, 6), (3, 6), (4, 3), (5, 10), (6, 1), (7, 5), (8, 11), (9, 10)], 
                3: [(0, 8), (1, 2), (2, 6), (4, 4), (5, 11), (6, 8), (7, 4), (8, 6), (9, 1)], 
                4: [(0, 10), (1, 3), (2, 3), (3, 4), (5, 4), (6, 3), (7, 8), (8, 5), (9, 11)], 
                5: [(0, 4), (1, 8), (2, 10), (3, 11), (4, 4), (6, 2), (7, 2), (8, 6), (9, 11)], 
                6: [(0, 10), (1, 3), (2, 1), (3, 8), (4, 3), (5, 2), (7, 3), (8, 8), (9, 9)], 
                7: [(0, 7), (1, 7), (2, 5), (3, 4), (4, 8), (5, 2), (6, 3), (8, 11), (9, 2)], 
                8: [(0, 4), (1, 9), (2, 11), (3, 6), (4, 5), (5, 6), (6, 8), (7, 11), (9, 4)], 
                9: [(0, 1), (1, 10), (2, 10), (3, 1), (4, 11), (5, 11), (6, 9), (7, 2), (8, 4)]}
    # directed
    graf_list = {0: [(1, 4), (2, 5), (3, 10), (4, 8), (6, 8), (7, 4), (9, 11)], 
                1: [(0, 4), (2, 8), (3, 6), (6, 5), (7, 5), (8, 10)], 
                2: [(0, 5), (1, 7), (3, 9), (5, 11), (7, 6), (8, 9), (9, 3)], 
                3: [(0, 8), (1, 9), (2, 10), (4, 11), (5, 5), (6, 4), (7, 10), (9, 9)], 
                4: [(0, 10), (1, 8), (2, 10), (3, 10), (5, 8), (8, 11)], 
                5: [(1, 8), (3, 11), (4, 5), (6, 9), (8, 4), (9, 8)], 
                6: [(0, 4), (1, 9), (2, 8), (3, 11), (4, 6), (5, 3), (8, 4), (9, 9)], 
                7: [(0, 5), (2, 10), (4, 5), (6, 11), (8, 3), (9, 8)], 
                8: [(0, 4), (1, 4), (2, 4), (3, 3), (4, 4), (5, 8), (6, 6), (7, 4), (9, 3)], 
                9: [(0, 7), (1, 7), (2, 11), (3, 3), (4, 4), (5, 6), (6, 9), (7, 9), (8, 8)]}
    # niespojna
    graf_list = {0: [(1, 6), (2, 3), (3, 5), (4, 8)], 
                1: [(0, 3), (2, 3), (3, 10), (4, 6)], 
                2: [(0, 4), (1, 4), (3, 11), (4, 10)], 
                3: [(0, 10), (1, 5), (2, 3), (4, 7)], 
                4: [(0, 4), (1, 4), (2, 5), (3, 6)], 
                5: [(6, 9), (7, 3), (8, 10), (9, 3)], 
                6: [(5, 3), (7, 4), (8, 4), (9, 8)], 
                7: [(5, 5), (6, 10), (8, 10), (9, 4)], 
                8: [(5, 11), (6, 9), (7, 7), (9, 6)], 
                9: [(5, 8), (6, 6), (7, 8), (8, 4)]}
    # wierzchołek rozpinający
    graf_list = {0: [(1, 6), (2, 3), (3, 5), (4, 8)], 
                1: [(0, 3), (2, 3), (3, 10), (4, 6)], 
                2: [(0, 4), (1, 4), (3, 11), (4, 10)], 
                3: [(0, 10), (1, 5), (2, 3), (4, 7),(5,4)], 
                4: [(0, 4), (1, 4), (2, 5), (3, 6)], 
                5: [(3,4),(6, 9), (7, 3), (8, 10), (9, 3)], 
                6: [(5, 3), (7, 4), (8, 4), (9, 8)], 
                7: [(5, 5), (6, 10), (8, 10), (9, 4)], 
                8: [(5, 11), (6, 9), (7, 7), (9, 6)], 
                9: [(5, 8), (6, 6), (7, 8), (8, 4)]}
    # graf rzadki
    graf_list = {0: [(3, 4), (4, 7), (6, 10), (7, 4), (8, 9)], 
                1: [(4, 10), (5, 10), (6, 4), (7, 9), (8, 5)], 
                2: [(4, 11), (6, 7), (8, 10)], 3: [(0, 4), (7, 8)], 
                4: [(0, 7), (1, 10), (2, 11), (6, 3), (7, 6), (8, 3), (9, 10)], 
                5: [(1, 10), (9, 3)], 
                6: [(0, 10), (1, 4), (2, 7), (4, 3), (7, 3), (8, 11)], 
                7: [(0, 4), (1, 9), (3, 8), (4, 6), (6, 3), (8, 9)], 
                8: [(0, 9), (1, 5), (2, 10), (4, 3), (6, 11), (7, 9), (9, 6)], 
                9: [(4, 10), (5, 3), (8, 6)]}
    for i in range(10):
        print(f"dla wierzchołka startowego {i} rozwiązanie:",NEARIN(graf_list, 0))
    to_graf(False)
    pass

if __name__ == "__main__":
    
    main()