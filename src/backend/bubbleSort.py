import time

def bubble_sort(arr):
    l = len(arr)

    for i in range(l):
        for j in range(0, l - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


def get_time(arr):
    start = time.time()
    bubble_sort(arr)
    end = time.time()
    print(arr)

    return end - start


