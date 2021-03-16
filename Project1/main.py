## Pedro Oliveira 89156

import numpy as np
from time import time
import random
import string
import sys
import csv

sys.setrecursionlimit(5000)
operation_count = 0
exec_times = []
op_counts = []

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def recursive_distance(seq1, seq2):
    global operation_count
    if len(seq1) == 0: 
        operation_count += 1
        return len(seq2)

    if len(seq2) == 0: 
        operation_count += 1
        return len(seq1)

    operation_count += 1
    cost = int(seq1[-1] != seq2[-1])

    operation_count += 4
    return np.min([
        recursive_distance(seq1[:-1], seq2) +1, 
        recursive_distance(seq1, seq2[:-1]) +1, 
        recursive_distance(seq1[:-1], seq2[:-1]) + cost
    ])


def memoization_distance(seq1, seq2, matrix=[]):
    if len(matrix) == 0: matrix = -1 * np.ones((len(seq1)+1, len(seq2)+1))

    global operation_count
    if matrix[len(seq1), len(seq2)] != -1: 
        operation_count += 1
        return matrix[len(seq1), len(seq2)]

    if len(seq1) == 0: 
        operation_count += 1
        dist = len(seq2)
    elif len(seq2) == 0: 
        operation_count += 1
        dist = len(seq1)
    else:
        operation_count += 5
        cost = int(seq1[-1] != seq2[-1])
        dist = np.min([
            memoization_distance(seq1[:-1], seq2, matrix) +1, 
            memoization_distance(seq1, seq2[:-1], matrix) +1, 
            memoization_distance(seq1[:-1], seq2[:-1], matrix) + cost
        ])

    operation_count += 1
    matrix[len(seq1), len(seq2)] = dist
    return dist

def dp_distance(seq1, seq2):
    global operation_count
    operation_count += 1
    seq1_size = len(seq1) + 1
    seq2_size = len(seq2) + 1
    matrix = np.zeros((seq1_size, seq2_size))

    operation_count += seq1_size + seq2_size
    matrix[:, 0] = np.arange(seq1_size)
    matrix[0, :] = np.arange(seq2_size)

    for i in range(1, seq1_size):
        letter1 = seq1[i-1]
        for j in range(1, seq2_size):
            operation_count += 6

            letter2 = seq2[j-1]
            cost = int(letter1 != letter2)
            
            matrix[i, j] = np.min([
                            matrix[i-1, j] +1,
                            matrix[i, j-1] +1,
                            matrix[i-1, j-1] + cost
            ])

    return matrix[-1,-1]

for i in range(12):
        rand_str1 = get_random_string(i)
        rand_str2 = get_random_string(i)
        time2 = time()
        recursive_distance(rand_str1, rand_str2)
        time3 = time()
        op_count1 = operation_count 
        operation_count = 0

        memoization_distance(rand_str1, rand_str2)
        op_count2 = operation_count
        time4 = time()
        operation_count = 0

        dp_distance(rand_str1, rand_str2)
        op_count3 = operation_count
        time5 = time()
        operation_count = 0

        exec_times.append(((time3-time2), (time4-time3), (time5-time4)))
        op_counts.append((op_count1, op_count2, op_count3))

        print("done with len", i)

for i in range(1,3):
    for j in [2, 5, 10]:
        rand_str1 = get_random_string(j*(10**i))
        rand_str2 = get_random_string(j*(10**i))
        
        time3 = time()
        memoization_distance(rand_str1, rand_str2)
        op_count2 = operation_count
        time4 = time()
        operation_count = 0

        dp_distance(rand_str1, rand_str2)
        op_count3 = operation_count
        time5 = time()
        operation_count = 0

        exec_times.append((0, (time4-time3), (time5-time4)))
        op_counts.append((0, op_count2, op_count3))

        print("done with len", j*(10**i))

with open("times.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Recursive", "Memoization", "Dynamic"])
    for elem in exec_times:
        writer.writerow(elem)

with open("op_count.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Recursive", "Memoization", "Dynamic"])
    for elem in op_counts:
        writer.writerow(elem)
