import java.util.ArrayList;

class Prog {
    static String DP(int[] waga,int[] zysk, int[] ilosc, int pojemnosc, ArrayList<ArrayList<Integer>> DP_table_decisions, 
    ArrayList<ArrayList<Integer>> DP_table_objective){
        // stworzenie macieczy o odpowiednim rozmiarze:
        for(int i = 0; i<=pojemnosc; i++){
            DP_table_decisions.add(new ArrayList<Integer>());
            DP_table_objective.add(new ArrayList<Integer>());
            for(int j = 0; j<waga.length; j++){
                DP_table_decisions.get(i).add(0);
                DP_table_objective.get(i).add(0);
            }
        }
        // uzupełnianie pierwszej kolumny tablicy programowania dynamicznego:
        // dla wszystkich możliwychg stanów:
        for(int j = 0; j<=pojemnosc; j++){
            // stwórz tablice możliwych do podjęcia decyzji:
            ArrayList<Integer> decisions = new ArrayList<Integer>();
            for(int k = 0; k<=j/waga[0] && k<=ilosc[0]; k++){
                decisions.add(k);
            }
            // pełny przegląd decyzji i wybranie najlepszej (o największej wartości funkcji celu):
            int x = 0;
            int max = 0;
            for(int k : decisions){
                if(max<zysk[0]*k){
                    max = zysk[0]*k;
                    x = k;
                } 
            }
            // wpisanie do tablicy 
            DP_table_decisions.get(j).set(0,x);
            DP_table_objective.get(j).set(0,max);
        }
        // uzupełnianie pozostałych kolumn tablicy programowania dynamicznego:
        // dla wszystkich etapów:
        for(int i = 1; i<waga.length; i++){
            // dla wszystkich stanów:
            for(int j = 0; j<=pojemnosc; j++){
                // wyznaczenie zbioru możliwych decyzji:
                ArrayList<Integer> decisions = new ArrayList<Integer>();
                for(int k = 0; (k<=j/waga[i] && k<=ilosc[i]); k++){
                    decisions.add(k);
                }
                // pełny przegląd decyzji i wybranie najlepszej(o największej wartości funkcji celu):
                int x = 0;
                int max = -1;
                for(int k : decisions){
                    if(max<zysk[i]*k + DP_table_objective.get(j-k*waga[i]).get(i-1)){
                        max = zysk[i]*k + DP_table_objective.get(j-k*waga[i]).get(i-1);
                        x = k;
                    } 
                }
                // uzupełnienie tabel o najlepszy możliwy wybór dla danego stanu:
                DP_table_decisions.get(j).set(i, x);
                DP_table_objective.get(j).set(i, max);
            }
        }
        // wybranie i zwrócenie najlepszej strategii:
        String strr = "";
        int start = pojemnosc;
        for(int i = waga.length -1 ; i>=0; i--){
            strr = String.valueOf(DP_table_decisions.get(start).get(i))+" "+strr;
            start -= DP_table_decisions.get(start).get(i)*waga[i];
        }
        return strr;
    }
    static public void main(String[] args){
        //definicja zadania:
        // wagi przedmiotów
        int[] waga = {1	,10,4,6,8,7,1,5,1,10};
        // zysk za jeden przedmiot
        int[] zysk = {2,30,2,7,3,5,12,3,4,5};
        // ilość dostępnych przedmiotów
        int[] ilosc = {4,1,5,6,1,4,5,3,2,7};
        // pojemność magazynu/plecaka:
        int pojemnosc = 20;
        // definicja macierzy do zwrotu
        ArrayList<ArrayList<Integer>> macierz_decyzji = new ArrayList<ArrayList<Integer>>();
        ArrayList<ArrayList<Integer>> macierz_wartosci = new ArrayList<ArrayList<Integer>>();
        // obsługa wyjścia:
        System.out.println("==== strategia ====");
        System.out.println(DP(waga,zysk,ilosc,pojemnosc,macierz_decyzji, macierz_wartosci));
        System.out.println("==== macierz decyzji każdego etapu ====");
        for(ArrayList<Integer> i:macierz_decyzji){
            System.out.println(i);
        }
        System.out.println("==== macierz wartości funkcji każdego etapu ====");
        for(ArrayList<Integer> i:macierz_wartosci){
            System.out.println(i);
        }
    }
    
}