import time

def selection_sort(arr):
    n = len (arr)

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            if books[j][1] < books[min_index][1]:
                min_index = j


    books[i], books[min_index] = books[min_index], books[i]


def get_time(arr):
    start = time.time()
    selection_sort(arr)
    end = time.time()

    return end-start


