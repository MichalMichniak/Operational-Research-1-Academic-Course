from cmath import inf
import numpy as np


def non_linear_PD(q,h,g,max_storage,min_storage,storage_start,storage_end):
    # deklaracja macierzy decyzji optymalnych i funkcji celu:
    tab = []
    # wyznaczenie ilości dopuszczalnych stanów
    state_len = max_storage - min_storage + 1
    # uzupełnianie ostatniego etapu:
    tab.append([[0 for i in range(state_len)],[0 for i in range(state_len)]])
    for k in range(state_len):
        f_min = inf
        x = 0
        # wyznaczenie zakresów decyzjnych:
        x_min = max(q[0] - k,0)
        x_max = max_storage+q[0] - k - min_storage
        x_max = min(len(g)-1,x_max)
        # pełne przeszukanie zbioru decyzji i znalezienie min funkcji celu
        for i in range(x_min,x_max+1):
            if f_min > ((g[i]+h[k+i-q[0]]) if k+i-q[0] == storage_end - min_storage else inf):
                f_min = g[i]+h[k+i-q[0]]
                x=i
        # przypisanie wartości optymalnych
        tab[0][0][k] = x
        tab[0][1][k] = f_min
        pass
    for i in range(1,len(q)):
        tab.append([[0 for i in range(state_len)],[0 for i in range(state_len)]])
        ## decyzje
        f_min = inf
        for k in range(state_len):
            f_min = inf
            x = inf
            # wyznaczenie zakresów decyzjnych:
            x_min = max(q[i] - k,0)
            x_max = max_storage+q[i] - k - min_storage
            x_max = min(len(g)-1,x_max)
            # pełne przeszukanie zbioru decyzji i znalezienie min funkcji celu
            for l in range(x_min,x_max+1):
                if f_min > g[l]+h[k+l-q[i]] + tab[i-1][1][k+l-q[i]]:
                    f_min = g[l]+h[k+l-q[i]] + tab[i-1][1][k+l-q[i]]
                    x=l
            # przypisanie wartości optymalnych
            tab[i][0][k] = x
            tab[i][1][k] = f_min
            pass
    # przepisanie macierzy aby można było ją wyświetlić
    tab_res = np.zeros((state_len,len(q)*2),dtype = int)
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            for k in range(len(tab[0][0])):
                tab_res[k,i*2+j] = tab[i][j][k]
    # obliczanie stanu początkowego:
    y = storage_start - min_storage
    i = len(q) - 1
    strr = ""
    # wyznaczanie strategii optymalnej
    while i != -1:
        strr += str(tab[i][0][y]) + "->"
        y = y + tab[i][0][y] - q[i]
        i-=1
    # zwrot macierzy decyzji i funkcji celu, strategii optymalnej, wartości funkcji celu dla strategii optymalnej
    return tab_res, strr[:-2], tab[len(q) - 1][1][storage_start - min_storage]
    pass


def main():
    # funkcja g(x) [zł] oznaczająca koszt produkcji x produktów w jednym miesiącu 
    production_cost = [3, 24, 26, 32, 36, 48, 57, 64, 71, 80]
    # maxymalna pojemność magazynu
    max_storage = 7
    # minimalna pojemność magazynu
    min_storage = 3
    # stan początkowy magazynu
    storage_start = 4
    # stan końcowy magazynu
    storage_end = 4
    # zapotrzebowanie na dany produkt w każdym z miesięcy w odwrotnej kolejności
    q = [7, 8, 1, 6, 4, 7, 3, 3, 9, 2, 0, 7]
    # h(yi) koszt przechowania yi produktów rozliczane pod koniec miesiąca
    storage_cost = [2,5,7,8,8]
    x, strr, cost = non_linear_PD(q,storage_cost,production_cost,max_storage,min_storage,storage_start,storage_end)
    print(f"path cost: {cost}")
    print("optimal strategy: "+strr)
    print("========================== macierz decyzji ===========================")
    gen = (i for i in range(min_storage,max_storage+1))
    for i in x:
        print(f"{next(gen)}:\t", end="")
        for n,j in enumerate(i):
            if n%2==0:
                print(f"{j}:",end=" ")
            else:
                print(f"{j} |",end=" ")
        print()
        
    pass


if __name__ == '__main__':
    main()