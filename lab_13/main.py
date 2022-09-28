import random
import numpy as np
from cmath import inf
from copy import copy

def reduction(M):
    # redukcja macierzy:
    # redukcja w rzędach (z pominięciem elementów inf):
    row = []
    for i in M:
        if np.min(i) != inf:
            row.append([np.min(i)])
        else:
            row.append([0])
    M = M - np.array(row)
    # redukcja w kolumnach (z pominięciem elementów inf):
    col = []
    for i in range(len(M)):
        if np.min(M[:,i])!= inf:
            col.append(np.min(M[:,i]))
        else:
            col.append(0)
    M = M - np.array(col)
    # zwrócenie macierzy i kosztu redukcji
    return M, np.sum(np.array(row))+np.sum(np.array(col))

def prune(M,path):
    # zabronienie podcykli:
    tab_popr = [-1 for i in range(len(M))]
    start = path[-1][1]
    koniec = start
    tab_naste = [-1 for i in range(len(M))]
    # mapowanie grafu do tablicy poprzedników i tablicy następników:
    for i in path:
        tab_popr[i[1]] = i[0]
        tab_naste[i[0]] = i[1]
    # poszukiwanie pierwszego elementu w sekwencji
    while tab_popr[start]!=-1:
            start = tab_popr[start]
    # poszukiwanie ostatniego elementu w sekwencji
    while tab_naste[koniec] != -1:
        koniec = tab_naste[koniec]
    # zabronienie domknięcia cyklu
    M[koniec,start] = inf
    return M

def matrix2x2case(M,path):
    # definicja kosztu (przy poprawnym wykonaniu algorytmu zawsze 0)
    cost = 0
    # wyszukanie wszystkich dozwolonych krawędzi i dodanie ich do sekwencji domykając cykl(lub nie):
    for n,i in enumerate(M):
        for t,j in enumerate(i):
            if M[t,n] < inf:
                path.append((t,n))
                cost += M[t,n]
                M[t,n] = inf
                M[n,t] = inf
                M[t,:] = inf
                M[:,n] = inf
    # jeżeli path<N => nie powstał cykl hamiltona cost = inf
    if len(path)!= len(M): return M,path,inf
    # zwróć path i eventualnie cost,
    # (macierz M zwracana w celach diagnostycznych powinna być to tablica samych inf)
    return M,path,cost
            


def marcin(M, path):
    # definicja zmiennych
    minimum = -1
    idx = [0,0]
    # redukcja macierzy na początku
    M, cost_t = reduction(M)
    # wyszukanie najbardziej optymalnej krawędzi do dołączenia
    for idx_x,i in enumerate(M):
        for idx_y,j in enumerate(i):
            if j == 0:
                min_temp_x = [l if n!=idx_y else inf for n,l in enumerate(M[idx_x,:])]
                min_temp_y = [l if n!=idx_x else inf for n,l in enumerate(M[:,idx_y])]
                if minimum< min(min_temp_x) + min(min_temp_y):
                    minimum = min(min_temp_x) + min(min_temp_y)
                    idx = [idx_x,idx_y]
    # dołączenie krawędzi, zabronienie podcyklu, 
    # wykreślenie odpowiednich kolumn i wierszy
    M[idx[0],:] = inf
    M[:,idx[1]] = inf
    M[idx[1],idx[0]] = inf
    path.append((idx[0],idx[1]))
    # KZ1
    if minimum == inf and len(path) != len(M)-2:
        return M,path,inf
    
    # Prunning macierzy problemu zrelaksowanego:
    # zabronienie podcykli
    if len(path)< len(M)-1:
        M = prune(M,path)
    
    # redukcja macierzy po pruningu i wykreśleniach
    M,cost = reduction(M)
    # osobny przypadek na macierz 2x2:
    if len(path)== len(M)-2:
        M,path,k = matrix2x2case(M,path)
        cost+=k
    # zwrócenie macierzy M, elementów ścierzki 
    # oraz poniesionego kosztu w wyniku operacji
    return M, path, cost +cost_t

def main_little(Matrix : np.ndarray):
    # inicjalizacja drzewa rozpatrywanych problemów
    lst = []
    Matrix , total_cost = reduction(Matrix)
    # inicjalizacja najlepszego LB
    lower_bound = inf
    # dołożenie do drzewa wyjściowego problemu
    lst.append((Matrix,[],total_cost))
    # zmienne pomocnicze
    final_path = []
    total_cost = 0
    # dopóki drzewo rozwiązań niepuste
    while lst!=[]:
        # znalezienie podproblemu o najmniejszym LB
        minimum = inf
        idx = 0
        advanced = 0
        for n,i in enumerate(lst):
            if minimum>i[2]:
                idx = n
                minimum = i[2]
                advanced = len(i[1])
            elif minimum == i[2] and advanced < len(i[1]):
                idx = n
                minimum = i[2]
                advanced = len(i[1])
        # odczyt i usunięcie danego problemu z drzewa rozwiązań
        temp,path,total_cost = lst[idx]
        lst.pop(idx)
        # przyspieszenie opróżniania drzewa
        # jeżeli nie zostanie spełniony warunek lower_bound>=total_cost
        # można wyjść z pętli
        if total_cost == inf:
            continue
        if lower_bound>=total_cost:
            M_prev = temp.copy()
            # wywołanie funkcji do rozwiązywania jednej iteracji podproblemu
            M, path, cost = marcin(temp.copy(),path)
            # aktualizacja koszt
            total_cost += cost
            ### kryteriium zamykania 3:
            if len(path) >= len(Matrix):
                if total_cost == inf:
                    continue
                # KZ3:
                if lower_bound > total_cost:
                    lower_bound = total_cost
                    final_path = path
                else:
                    continue
            # KZ1:
            if cost == inf:
                continue
            # KZ2
            if total_cost>lower_bound:
                continue
            # podział na podproblemy
            # wstawienie podproblemu P1 do drzewa rozwiązań
            lst.insert(0,(M.copy(),path.copy(),total_cost))
            # zabronienie wybranej ścierzki
            M_prev[path[-1][0],path[-1][1]] = inf
            # redukcja macierzy
            M_prev,cost = reduction(M_prev)
            # aktualizacja kosztu P2
            total_cost +=cost
            # wstawienie podproblemu P2 do drzewa rozwiązań
            lst.append((M_prev,path[:-1],total_cost))
        else:
            # zwrócenie wartości jeśli nie zostanie spełniony warunek lower_bound>=total_cost
            # KZ2 dla całego drzewa
            return final_path,lower_bound
    # zwrócenie wyniku jeśli zamknięte zostały wszystkie podproblemy
    return final_path,lower_bound

def get_path_parse(path):
    # stworzenie ścierzki z krawędzi:
    start = path[-1][1]
    # stworzenie i uzupełnienie tablicy poprzedników
    tab_popr = [-1 for i in range(len(path))]
    for i in path:
        tab_popr[i[1]] = i[0]
    # stworzenie ścierzki
    # po wartościach z tablicy poprzedników
    strr = f'{path[-1][1]}'
    temp = path[-1][1]
    for i in range(len(path)):
        temp = tab_popr[temp]
        strr = str(temp) + '->' + strr
    return strr

def main():
    M = np.array([[random.randint(3,9) if i!=j else inf for i in range(5)] for j in range(5)],dtype = float)
    # M = np.array([[inf,  10.,  8.,  19.,  12.],
    #                 [ 10., inf,  20.,  6.,  3.],
    #                 [ 8.,  20., inf,  4.,  2.],
    #                 [ 19.,  6.,  4., inf,  7.],
    #                 [ 12.,  3.,  2.,  7., inf]])
#     M = np.array([[inf,  6.,  3.,  7.,  7.],
#  [ 3., inf,  7.,  6.,  3.],
#  [ 9.,  7., inf,  9.,  6.],
#  [ 3.,  4.,  5., inf,  6.],
#  [ 4.,  6.,  8.,  9., inf]])
    #M = np.array([[inf,7,5,9,4],[7,inf,2,8,1],[5,2,inf,10,6],[9,8,10,inf,3],[4,1,6,3,inf]])
    print(M)
    path, cost = main_little(M)
    print(f"cost: {cost} \npath: {get_path_parse(path)}")#
    pass

if  __name__ == '__main__':
    main()