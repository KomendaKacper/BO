import numpy as np
from copy import copy
def metoda_wegierska(koszty):
    #1: Redukcja całkowita
    koszty = redukcja_calkowita(koszty)
    print (koszty)
    #2: Inicjalizacja
    n = len(koszty)
    count_zero_lines = 0

    #3: Wykonanie iteracji, dopóki nie zostaną wybrane wszystkie elementy
    while count_zero_lines < n:
        zaznaczone_wiersze, zaznaczone_kolumny = wykreslanie_zer_min_linii(koszty)
        print (zaznaczone_wiersze)
        print (zaznaczone_kolumny)
        count_zero_lines = len(zaznaczone_wiersze) + len(zaznaczone_kolumny)

        if count_zero_lines < n:
            koszty = adjust_matrix()
        else:
            rozwiazanie = znajdz_zerowy_element(koszty)
    return rozwiazanie


def redukcja_calkowita(matrix):
    # Zmniejszenie macierzy szukając najmniejszej wartości w wierszu nastepnie w kolumnie
    # Zmniejszenie wiersza
    m = copy(matrix)

    for row in m:
        if 0 not in row:
            smallestElement = min(row)
            for idx, element in enumerate(row):
                row[idx] = element - smallestElement
    m = m.T
    for row in m:
        if 0 not in row:
            smallestElement = min(row)
            for idx, element in enumerate(row):
                row[idx] = element - smallestElement

    return m.T

def znajdz_zerowy_element(zero_mat):
    mark_zero = []
    # Iterujemy, dopóki istnieją zera w macierzy
    while np.count_nonzero(zero_mat) > 0:
        min_row = [99999, -1]

        # Znajdujemy wiersz z najmniejszą ilością zer
        for row_num in range(zero_mat.shape[0]):
            count_zeros = np.sum(zero_mat[row_num] == 0)
            if count_zeros > 0 and min_row[0] > count_zeros:
                min_row = [count_zeros, row_num]

        # Jeśli znajdujemy wiersz z zerami
        if min_row[1] != -1:
            zero_index = np.where(zero_mat[min_row[1]] == 0)[0][0]
            mark_zero.append((min_row[1], zero_index))
            # Oznaczamy wiersz i kolumnę zawierającą zero jako użyte
            zero_mat[min_row[1], :] = True
            zero_mat[:, zero_index] = True
        else:
            break  # Jeśli nie ma już zer do wyznaczenia, przerywamy pętlę

    return mark_zero[0], mark_zero

def adjust_matrix(mat, cover_rows, cover_cols):
    cur_mat = np.copy(mat)
    non_zero_elements = []

    # Znajdujemy najmniejszą wartość elementu nieoznaczonego w zaznaczonych wierszach/kolumnach
    for row in range(cur_mat.shape[0]):
        if row not in cover_rows:
            for col in range(cur_mat.shape[1]):
                if col not in cover_cols:
                    non_zero_elements.append(cur_mat[row, col])

    min_num = min(non_zero_elements)

    # Odejmujemy od wszystkich wartości nieoznaczonych wierszy/kolumn
    for row in range(cur_mat.shape[0]):
        if row not in cover_rows:
            for col in range(cur_mat.shape[1]):
                if col not in cover_cols:
                    cur_mat[row, col] -= min_num

    # Dodajemy do wszystkich wartości oznaczonych wierszy/kolumn
    for row in cover_rows:
        for col in cover_cols:
            cur_mat[row, col] += min_num

    return cur_mat

def wykreslanie_zer_min_linii(koszty):
    # Krok 1: Znalezienie minimum w każdym wierszu
    min_wierszy = [min(wiersz) for wiersz in koszty]
    
    # Krok 2: Znalezienie minimum w każdej kolumnie
    min_kolumn = [min(koszty[i][j] for i in range(len(koszty))) for j in range(len(koszty[0]))]
    
    # Krok 3: Inicjalizacja tablicy zaznaczeń dla wierszy i kolumn
    zaznaczone_wiersze = [False] * len(koszty)
    zaznaczone_kolumny = [False] * len(koszty[0])
    
    # Krok 4: Zaznaczanie zer, które pokrywają się z minimalnymi wartościami z Kroków 1 i 2
    for i in range(len(koszty)):
        for j in range(len(koszty[i])):
            if koszty[i][j] == min_wierszy[i] and koszty[i][j] == min_kolumn[j]:
                zaznaczone_wiersze[i] = True
                zaznaczone_kolumny[j] = True
    
    # Krok 5: Inicjalizacja tablicy rzędów i kolumn
    rzedy_do_wykreslenia = [i for i, zaznaczony in enumerate(zaznaczone_wiersze) if not zaznaczony]
    kolumny_do_wykreslenia = [j for j, zaznaczony in enumerate(zaznaczone_kolumny) if zaznaczony]
    
    return rzedy_do_wykreslenia, kolumny_do_wykreslenia

# Przykładowe użycie:
koszty = [
    [3, 0, 2],
    [2, 1, 0],
    [1, 0, 0]
]

rzedy, kolumny = wykreslanie_zer_min_linii(koszty)
print("Rzędy do wykreślenia:", rzedy)
print("Kolumny do wykreślenia:", kolumny)

# Przykładowe użycie:
koszty = np.array([ [4,  6,  6,  5, 10,  6,  7],
                    [7, 13, 10,  9, 15, 12, 14],
                    [7, 13, 13, 13,  9, 12, 11],
                    [0, 10,  6,  8,  5,  6, 12],
                    [7,  4,  8, 15, 13, 11,  5],
                    [3,  3,  4,  4,  4,  5, 10],
                    [15, 12, 15, 14, 10, 12,  5]])

rzedy, kolumny = wykreslanie_zer_min_linii(koszty)
print("Rzędy do wykreślenia:", rzedy)
print("Kolumny do wykreślenia:", kolumny)