import random
import sys
import time

def valid(c):
    return -50 <= c <= 50

def loop_version(readings):
    result = []
    for c in readings:
        if valid(c):
            result.append(c * 9 / 5 + 32)
    return result

def comprehension_version(readings):
    return [c * 9 / 5 + 32 for c in readings if valid(c)]

def map_filter_version(readings):
    return list(map(lambda c: c * 9 / 5 + 32,
                    filter(lambda c: valid(c), readings)))

def alarm_minutes(readings):
    return [minute for minute, c in enumerate(readings) if c < 2 or c > 8]

def converted_dictionary(readings):
    return {minute: c * 9 / 5 + 32
            for minute, c in enumerate(readings) if valid(c)}

def unique_converted_values(readings):
    return {c * 9 / 5 + 32 for c in readings if valid(c)}

def experiment():
    random.seed(7)
    for n in (10000, 100000, 1000000):
        data = [random.uniform(-60, 60) for _ in range(n)]
        results, timings = [], []
        for function in (loop_version, comprehension_version, map_filter_version):
            start = time.perf_counter()
            results.append(function(data))
            timings.append(time.perf_counter() - start)
        print(f"n={n}: loop={timings[0]:.6f}s comprehension={timings[1]:.6f}s "
              f"map/filter={timings[2]:.6f}s identical={results[0] == results[1] == results[2]}")

    all_valid = [10.0, 0.0, -20.0, 50.0]
    all_invalid = [55.0, -51.0, 100.0]
    print("All valid:", comprehension_version(all_valid))
    print("All invalid:", comprehension_version(all_invalid))

    sample = [1.5, 3.0, 7.5, 9.2, 55, -60, 2.0, 8.5]
    print("Alarm minutes:", alarm_minutes(sample))
    print("Dictionary comprehension:", converted_dictionary(sample))
    print("Set comprehension:", unique_converted_values(sample))
    list_result = comprehension_version([1.0] * 100000)
    generator_result = (c * 9 / 5 + 32 for c in [1.0] * 100000 if valid(c))
    print("List result shallow size:", sys.getsizeof(list_result))
    print("Generator shallow size:", sys.getsizeof(generator_result))

if __name__ == "__main__":
    experiment()
    # Task 05 - Execution verified
