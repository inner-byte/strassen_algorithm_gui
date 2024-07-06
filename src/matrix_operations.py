# matrix_operations.py

import numpy as np
from concurrent.futures import ThreadPoolExecutor

def next_power_of_2(x):
    return 1 if x == 0 else 2**(x - 1).bit_length()

def pad_matrix(matrix):
    n = len(matrix)
    m = next_power_of_2(n)
    if n == m:
        return matrix
    else:
        padded_matrix = np.zeros((m, m))
        padded_matrix[:n, :n] = matrix
        return padded_matrix

def add_matrix(A, B):
    return np.add(A, B)

def subtract_matrix(A, B):
    return np.subtract(A, B)

def strassen(A, B):
    n = len(A)
    if n == 1:
        return A * B
    else:
        mid = n // 2

        A11 = A[:mid, :mid]
        A12 = A[:mid, mid:]
        A21 = A[mid:, :mid]
        A22 = A[mid:, mid:]

        B11 = B[:mid, :mid]
        B12 = B[:mid, mid:]
        B21 = B[mid:, :mid]
        B22 = B[mid:, mid:]

        with ThreadPoolExecutor() as executor:
            M1 = executor.submit(strassen, add_matrix(A11, A22), add_matrix(B11, B22)).result()
            M2 = executor.submit(strassen, add_matrix(A21, A22), B11).result()
            M3 = executor.submit(strassen, A11, subtract_matrix(B12, B22)).result()
            M4 = executor.submit(strassen, A22, subtract_matrix(B21, B11)).result()
            M5 = executor.submit(strassen, add_matrix(A11, A12), B22).result()
            M6 = executor.submit(strassen, subtract_matrix(A21, A11), add_matrix(B11, B12)).result()
            M7 = executor.submit(strassen, subtract_matrix(A12, A22), add_matrix(B21, B22)).result()

        C11 = add_matrix(subtract_matrix(add_matrix(M1, M4), M5), M7)
        C12 = add_matrix(M3, M5)
        C21 = add_matrix(M2, M4)
        C22 = add_matrix(subtract_matrix(add_matrix(M1, M3), M2), M6)

        C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
        return C