import bubbleSort
import mergeSort
import insertionSort
import quickSort
import radixSort
import linearSearch

import random

#test = [1,5,62,7,3,2,6,7,84,2,6126,236,6,36,26362,62,62,36]

# Parameter one: list of bools. We use this to determin what algorithms we are running
# [bubble sort, merge sort, insertion sort, quick sort, radix sort, linear search]


# Parameter two: Random array size. Generate a random array based of the size. IF SIZE == -1, the user has manually inputed an array


# Parameter three: Manual input array. Self explanitory


# End result is an array of times. ex: [0.0052, 0.00013, 0, 0.0042, 0] where 0 is a algorithm that was not ran
def get_times(algos: list[bool], size: int, arr) -> list[int]:
    times = []
    if (size == -1):
        elements = arr
    else:
        # Get a random array based on size:
        elements = [random.randint(10,9999) for _ in range(size)]

    # Get times
    for i in range(len(algos)):
        if algos[i] == True:
            match i:
                case 0:
                    times.append(int(bubbleSort.get_time(elements)*(1000000)))
                case 1:
                    times.append(int(mergeSort.get_time(elements)*(1000000)))
                case 2:
                    times.append(int(insertionSort.get_time(elements)*(1000000)))
                case 3:
                    times.append(int(quickSort.get_time(elements)*(1000000)))
                case 4:
                    times.append(int(radixSort.get_time(elements)*(1000000)))
                case 5:
                    times.append(int(linearSearch.get_time(elements)*(1000000)))
                case _:
                    print("An error has occured")
        else:
            times.append(0)

    print(times)

algos = [True, True, True, True, True, True]
get_times(algos, -1, [5, 52, 6, 20, 521, 5251, 0])
