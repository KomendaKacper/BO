import numpy as np
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

# def wykreslanie_zer_min_linii()

def redukcja_calkowita(matrix):
    # Zmniejszenie macierzy szukając najmniejszej wartości w wierszu nastepnie w kolumnie
    # Zmniejszenie wiersza
    row_mins = matrix.min(axis=1)
    row_reduced = matrix - row_mins.reshape(-1, 1)

    # Obrót macierzy i redukcja kolumn
    col_mins = row_reduced.min(axis=0)
    col_reduced = row_reduced - col_mins

    return col_reduced

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

    return mark_zero

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

koszty = np.array([
    [4,2,5,7],[8,3,10,8],[12,5,4,5],[6,3,7,14]
])

rozwiazanie = redukcja_calkowita(koszty)
print(rozwiazanie)

# rows, cols = wykreslanie_zer_min_linii(rozwiazanie)
# matrix = adjust_matrix(rozwiazanie, rows, cols)
# print (matrix)

koszty_przed_adjust = [[0,0,0,1],[3,0,4,1],[9,4,0,0],[1,0,1,7]]
rows = [0,2]
cols = [1]
koszty_po_adjust = (adjust_matrix(koszty_przed_adjust,rows, cols))

zera = znajdz_zerowy_element(koszty_po_adjust)
print (zera)