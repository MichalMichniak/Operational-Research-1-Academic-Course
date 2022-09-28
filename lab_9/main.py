from cmath import inf
import numpy as np
from copy import deepcopy
from numpy.random import randint

def johnson2(N,forward_idx = 0,backward_idx = None, id = None):
    """algorytm Johnsona dla wyznaczania szeregowania zadań dla dwóch maszyn"""
    # definicja zbioru rozwiązań
    rozw = []
    # definicje zmiennych podstawowych jeżeli to nie jest wywołanie rekurencyjne funkcji:
    if backward_idx == None: backward_idx = len(N[0]) - 1
    if id == None: id = [i for i in range(len(N[0]))]
    # do czasu aż zostanie uzgodniona kolejność wszystkich detali:
    while forward_idx != backward_idx:
        idx = [0]
        forwardd = True
        min = inf
        # znajdź element najmniejszy:
        for i in range(2):
            for j in range(forward_idx, backward_idx+1):
                # ustaw element najmniejszy jako listę rozpatrywanych gałęzi rozwiązań
                if N[i,j] < min:
                    min = N[i,j]
                    # oznacz czy element najmniejszy idze na indeks tylni(False) czy na indeks przedni(True)
                    if i == 0:
                        idx = [(j,True)]
                    else:
                        idx = [(j,False)]
                # dodaj element na równi z elementem najmniejszym do listy rozpatrywanych gałęzi rozwiązania
                elif N[i,j] == min:
                    if i == 0:
                        idx.append((j,True))
                    else:
                        idx.append((j,False))
        # jeżeli istnieje wiele alternatywnych gałęzi rozwiązania:
        if len(idx)>1:
            # dla każdej gałęzi rozwiązań poza gałęzią zerową:
            for i in idx[1:]:
                # jeżeli należy dany detal wstawić na index tylni:
                if not i[1]:
                    # stwórz kopię gałęzi głównej
                    N_copy = deepcopy(N)
                    temp = deepcopy(N[:,i[0]])
                    temp2 = deepcopy(N[:,backward_idx])
                    id_copy = deepcopy(id)
                    # zamień odpowiednie elementy na kopi indentyfikatorów zadań
                    id_copy[i[0]], id_copy[backward_idx] =  id[backward_idx],id[i[0]]
                    # zamień odpowiednie elementy na kopi gałęzi rozwiązania
                    N_copy[:,i[0]], N_copy[:,backward_idx] = temp2,temp
                    # wywołaj rekurencyjnie nową instancję funkcji do obliczenia reszty rozwiązań z rozpatrywanej głęzi rozwiazań
                    t = johnson2(N_copy,forward_idx,backward_idx-1,id_copy)
                    # dodaj do rozwiązania każdy element nienależący do rozwiązania 
                    if rozw != []:
                        for n,a in enumerate(list(zip(*t))[1]):
                            temp = True
                            for s in list(zip(*rozw))[1]:
                                if s==a:
                                    temp = False
                            if temp:
                                rozw.append(t[n])
                    else:
                        rozw.extend(t)
                # jeżeli należy dany detal wstawić na index przedni:
                else:
                    # stwórz kopię gałęzi głównej
                    N_copy = deepcopy(N)
                    temp = deepcopy(N[:,i[0]])
                    temp2 = deepcopy(N[:,forward_idx])
                    id_copy = deepcopy(id)
                    # zamień odpowiednie elementy na kopi indentyfikatorów zadań
                    id_copy[i[0]], id_copy[forward_idx] =  id[forward_idx],id[i[0]]
                    # zamień odpowiednie elementy na kopi gałęzi rozwiązania
                    N_copy[:,i[0]], N_copy[:,forward_idx] = temp2,temp
                    # wywołaj rekurencyjnie nową instancję funkcji do obliczenia reszty rozwiązań z rozpatrywanej głęzi rozwiazań
                    t = johnson2(N_copy,forward_idx+1,backward_idx,id_copy)
                    # dodaj do rozwiązania  każdy element nienależący do rozwiązania
                    if rozw != []:
                        for n,a in enumerate(list(zip(*t))[1]):
                            temp = True
                            for s in list(zip(*rozw))[1]:
                                if s==a:
                                    temp = False
                            if temp:
                                rozw.append(t[n])
                    else:
                        rozw.extend(t)
            idx, forwardd= idx[0]
        else:
            idx, forwardd= idx[0]
        # rozpatrywanie głównej gałęzi rozwiązania:
        # jeżeli należy dany detal wstawić na index tylni:
        if not forwardd:
            temp = deepcopy(N[:,idx])
            temp2 = deepcopy(N[:,backward_idx])
            # zamień odpowiednie elementy indentyfikatorów zadań
            id[idx], id[backward_idx] =  id[backward_idx],id[idx]
            # zamień odpowiednie elementy gałęzi rozwiązania
            N[:,idx], N[:,backward_idx] = temp2,temp
            # zmniejsz index tylni
            backward_idx -= 1
        # jeżeli należy dany detal wstawić na index przedni:
        else:
            temp = deepcopy(N[:,idx])
            temp2 = deepcopy(N[:,forward_idx])
            # zamień odpowiednie elementy indentyfikatorów zadań
            id[idx], id[forward_idx] =  id[forward_idx],id[idx]
            # zamień odpowiednie elementy gałęzi rozwiązania
            N[:,idx], N[:,forward_idx] = temp2,temp
            # zmniejsz index przedni
            forward_idx += 1
    # dodaj do rozwiązania każdy element nienależący do rozwiązania 
    temp = True
    if rozw != []:
        for s in list(zip(*rozw))[1]:
            if s==id:
                temp = False
        if temp:
            rozw.append([N,id])
    else:
        rozw.append([N,id])
    return rozw

def CDS_time(M, id, show_time = False):
    """Wyznaczanie minimalnego czasu wykonywania czynności przy uszeregowaniu id"""
    M_copy = deepcopy(M)
    # zdefiniowanie poprzednika
    prev = id[0]
    # policzenie czasu zakończenia czynności 1 dla każdej maszyny
    for i in range(1,len(M_copy)):
        M_copy[i,prev] += M_copy[i-1,prev] 
    # dla każdej następnej czynności:
    for i in range(1,len(M[0])):
        # wyznaczanie czasu zakończenia przetwarzania i- tego zadania przez maszynę pierwszą w szergu
        M_copy[0,id[i]] += M_copy[0,id[i-1]]
        for j in range(1,len(M)):
            # czas zakończenia i-tego zadania na j-tej maszynie = 
            # max(czas zakończenia przetważania poprzedniego zadania na j-tej maszynie, 
            # czas zakończenia przetważania i-tego zadania na (j-1)-szej maszynie) + czas przetwarzania zadania
            M_copy[j,id[i]] += max(M_copy[j,id[i-1]],M_copy[j-1,id[i]])
        pass
    else:
        if not show_time:
            return M_copy[j,id[i]]
        else:
            return M_copy



def CDS(M):
    """Główna funkcja CDS"""
    # zadanie pomocnicze:
    Mr = []
    # konstrukcja n-1 zadań pomocniczych
    for r in range(len(M)-1):
        temp = [[],[]]
        for j in range(len(M[0])):
            # Mr[1,j] = suma od i = 1 do r po tij
            temp[0].append(np.sum(M[:r+1,j]))
            # Mr[2,j] = suma od i = n+1-r do n po tij
            temp[1].append(np.sum(M[len(M)-1-r:len(M)+1,j]))
        Mr.append(deepcopy(temp))
    # znalezienie rozwiązania metodą przeglądu zupełnego:
    minimum = inf
    idx = 0
    # dla wszystkich zadań pomocniczych wyznaczenie kolejności i minimalnego czasu wykonania wszystkich czynności przez maszyny:
    for i in Mr:
        # lista rozwiązań dla danego zadania pomocniczego:
        k = johnson2(np.array(i))
        for j,idd in k:
            # policzenie czasu minimalnego wykonywania zadań dla uszeregowania idd
            if (x:=CDS_time(M,idd)) < minimum:
                # zapis najmniejszych czasów i uszeregowań z przeliczonych rozwiązań
                idx = idd
                minimum = x
    # zwróć uszeregowanie i minimalny czas wykonywania czynności
    return idx,minimum

def in_order(N,idd):
    res = np.zeros(N.shape)
    for n,i in enumerate(idd):
        res[:,n] = N[:,i]
    return res


N = np.array([[randint(1,20) for i in range(10)],
            [randint(1,20) for i in range(10)],
            [randint(1,20) for i in range(10)],
            [randint(1,20) for i in range(10)]])

N = np.array([[15, 2, 13, 14, 10, 17, 16,  6,  4, 14],
            [3,  5, 13, 19, 15, 15, 8, 19, 6, 18],
            [9, 17, 4, 6, 18, 14, 12, 16, 7, 5],
            [11, 14, 8, 3, 1, 19, 11, 15, 11, 7]])

idd, t = CDS(N)

print(f"szeregowanie: {idd} \ncałkowity minimalny czas: {t}")
print("=================== uszeregowanie początkowe ===================")
print(f"zadanie:         ",end='')
for i in [i for i in range(len(idd))]:
    print(f"{i}  ", end= '')
print()
for n,i in enumerate(N):
    print(f"maszyna nr. {n}: {i}")


print("=================== czasy zakończeń ===================")
print(f"zadanie:         ",end='')
for i in [i for i in range(len(idd))]:
    print(f"{i}   ", end= '')
print()
for n,i in enumerate(CDS_time(N,idd,True)):
    print(f"maszyna nr. {n}: {i}")

temp = in_order(CDS_time(N,idd,True),idd)
print("=================== czasy zakończeń(uszeregowane) ===================")
print(f"zadanie:         ",end='')
for i in idd:
    print(f"{i}    ", end= '')
print()
for n,i in enumerate(temp):
    print(f"maszyna nr. {n}: {i}")