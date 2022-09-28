
from cmath import inf
from typing import Dict, List
import copy
import random

def renumber(G) -> Dict:
    # znajdź wierchołek początkowy
    Q = list(G.keys())
    for i in G.values():
        for j in i:
            if j[0] in Q:
                Q.remove(j[0])
    it = Q[0]
    # deklaracja słowników D - numeracja Grafu -> numeracja CPM, E - numeracjan CPM -> umeracja Grafu:
    D = {}
    E = {}
    numberator = (i for i in range(len(list(G.keys()))))
    stack = []
    D[it]=next(numberator)
    E[D[it]] = it
    # jeżeli wszystkie wierzchołki będą ponumerowane,(Q będzie zawierało wszystkie wierzchołki)
    while len(Q) != len(list(G.keys())):
        for i in G[it]:
            # sprawdź czy któraś krawędź z wierzchołka nie nalerzącego do Q (E.values()) wchodzi do przeglądanego wierzchołka
            # jeżeli nie -> odłuż wierzchołek do kolejki
            # jeżeli tak pomiń
            t = True
            for j in G.keys():
                for k in G[j]:
                    if (not (k[0]  in E.values())) and (i[0] in (list(zip(*G[k[0]]))[0] if G[k[0]] != [] else [])):
                        t = False
            if t:
                stack.append(i[0])
        #ściągnij z kolejki wierzchołek
        if not stack == []:
            it = stack[0]
        else: return E,D
        stack.remove(it)
        #dopisanie nowej wartości do słownika
        D[it]=next(numberator)
        E[D[it]] = it
    return E,D

### Struktura reprezentująca terminy
class Elem:
    def __init__(self):
        self.T_w = 0
        self.T_p = inf
        pass

    def __repr__(self):
            return f"{self.T_w},{self.T_p}"


def get_path(Time:List[Elem],decode:Dict):
    strr = f"{decode[0]}"
    for n,i in enumerate(Time[1:]):
        if i.T_p == i.T_w:
            strr += f"->{decode[n+1]}"
    return strr

def bind_time(Time,decode,encode,G : Dict):
    strr = ""
    for i in G.keys():
        for j in G[i]:
            strr += f"zadanie: {i}-{j[0]} czas wykonania: {Time[encode[i]].T_w} - {Time[encode[j[0]]].T_p}" 
            strr += f" zapas: {Time[encode[j[0]]].T_p-Time[encode[i]].T_w - j[1]} , czas trwania: {j[1]} \n"
    return strr



    

def CPM(G):
    G_prim : Dict = copy.deepcopy(G)
    # stworzenie tablic(słowników) przekodowań
    decode,encode = renumber(G_prim)
    # utworzenie listy terminów dla każdego wierzchołka
    Time = [Elem() for i in range(len(G_prim.keys()))]
    # nadanie najwcześniejszemu wierzchołkowi najwcześniejszego terminu = 0
    Time[0].T_w = 0
    # w kolejności od najmniejszego do największego względem przekodowania:
    for i in decode.keys():
        for j in G[decode[i]]:
            ## Tj(w) = max{Ti(w) + tij}
            Time[encode[j[0]]].T_w = max(j[1] + Time[i].T_w,Time[encode[j[0]]].T_w)
    # nadanie ostatniemu wierzchołkowi wartości najpóźnieszego terminu = termin najwcześniejszy dla ostatniego wierzchołka
    Time[-1].T_p = Time[-1].T_w
    # w kolejności od największego do najmniejszego względem przekodowania:
    for i in list(decode.keys())[::-1]:
        for j in G[decode[i]]:
            #Ti(w) = max{Tj(w) - tij}
            Time[i].T_p = min(Time[encode[j[0]]].T_p - j[1],Time[i].T_p)
    # zwróć całkowity czas, ścierzkę, informacje o poszczególnych elementach(do wykresu ganta)
    return Time[-1].T_w, get_path(Time, decode), bind_time(Time, decode, encode, G),encode
    pass




def PERT(G):
    pass


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
        T = [i for i in range(lenghtt)]
        random.shuffle(T)
        G = {i:[] for i in range(lenghtt)}
        for i in G.keys():
            for j in G.keys():
                #if i>j: continue
                if i!=j:
                    #if ((i in Q) and (j in Q)) or ((not (i in Q)) and (not (j in Q))):
                    if T.index(i)>T.index(j) and abs(T.index(i)-T.index(j))<4:
                        #if random.randint(3,11) >6:
                            weight = random.randint(1,11)
                            G[i].append((j, weight))
                            #G[j].append((i, weight))
    print(G)
    print("\n\n\n\n")
          
    for i in G.keys():
        for j in G[i]:
            print(f"{i} {j[0]} {j[1]}")


def main():
    graph = {1:[(6,2),(2,3)],
    2:[(5,6),(4,3)],
    3:[(4,1)],
    4:[],
    5:[(3,3),(4,2)],
    6:[(3,7),(5,1)]
    }
    graph = {
        0: [(3, 6), (7, 10), (8, 8)], 
        1: [(4, 2), (5, 2), (9, 8)], 
        2: [(0, 1), (6, 2), (8, 8)], 
        3: [], 
        4: [(2, 10), (5, 3), (9, 3)], 
        5: [(2, 8), (6, 11), (9, 1)], 
        6: [(0, 9), (7, 9), (8, 5)], 
        7: [(3, 11)], 
        8: [(3, 5), (7, 1)], 
        9: [(0, 8), (2, 8), (6, 5)]}
    time,path,rezerwa,decode = CPM(graph)
    print("czas wykonania: ",time)
    print("ścieżka krytyczna: ",path)
    print("przenumerowanie: ", decode)
    print(rezerwa)
    #to_graf(False)
    pass

if __name__ == '__main__':
    main()