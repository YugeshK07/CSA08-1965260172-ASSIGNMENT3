import copy
import sys
import time

rows, cols = 3, 4
bad = [[0] * cols] * rows
bad[0][1] = 7

# TODO 1: make a separate row list for every row
good = [[0 for _ in range(cols)] for _ in range(rows)]
good[0][1] = 7

print("bad:", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])

stops = {
    (13.0827, 80.2707): "Chennai Central",
    (13.0418, 80.2341): "T. Nagar"
}
print(stops[(13.0418, 80.2341)])
try:
    invalid = {[13.0418, 80.2341]: "T. Nagar"}
except TypeError as error:
    print("List key error:", error)

# Shallow copy, deep copy and aliasing
original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
slice_copy = original[:]
deep = copy.deepcopy(original)
shallow[0][0] = 99
print("Original after copy.copy nested change:", original)
slice_copy[1][1] = 77
print("Original after slicing-copy nested change:", original)
deep[1][0] = 88
print("Deep copy (independent nested lists):", deep)

# A list contained inside a tuple can still be modified.
tuple_with_list = ([1, 2], [3, 4])
tuple_with_list[0].append(5)
print("Tuple containing changed list:", tuple_with_list)

def memory_test():
    values = list(range(1_000_000))
    tuple_values = tuple(values)
    print("List shallow size:", sys.getsizeof(values))
    print("Tuple shallow size:", sys.getsizeof(tuple_values))

def timing_test():
    values_list = list(range(1_000_000))
    start = time.perf_counter()
    list_values = [x for x in values_list]
    list_create = time.perf_counter() - start
    start = time.perf_counter()
    tuple_values = tuple(values_list)
    tuple_create = time.perf_counter() - start
    start = time.perf_counter()
    for _ in range(100000):
        _ = list_values[500000]
    list_index = time.perf_counter() - start
    start = time.perf_counter()
    for _ in range(100000):
        _ = tuple_values[500000]
    tuple_index = time.perf_counter() - start
    print(f"Creation: list={list_create:.6f}s tuple={tuple_create:.6f}s")
    print(f"Indexing: list={list_index:.6f}s tuple={tuple_index:.6f}s")

if __name__ == "__main__":
    memory_test()
    timing_test()
