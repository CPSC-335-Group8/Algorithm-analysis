import time

def bubble_sort(arr):
    l = len(arr)

    for i in range(l):
        for j in range(0, l, - i - 1):
            if student[j][1] > students[j + 1][1]:
                students[j], students[j+1] = students[j+1], students [j]

def get_time(arr):
    start = time.time()
    bubble_sort(arr)
    end = time.time()

    return end - start


