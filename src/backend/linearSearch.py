import time
import random

def linear_search(arr, element):
    for x in range(len(arr)):
        if (arr[x] == element):
            return

# Pick a random element to find
def get_random_element(arr):
    return random.choice(arr)


def get_time(arr):
    element = get_random_element(arr)

    start = time.time()
    linear_search(arr, element)
    end = time.time()

    return end - start


