import bubbleSort
import mergeSort
import insertionSort
import quickSort
import radixSort

test = [1,5,62,7,3,2,6,7,84,2,6126,236,6,36,26362,62,62,36]

val = radixSort.get_time(test)
valformated = f"{val:.6f}"

print(valformated)
