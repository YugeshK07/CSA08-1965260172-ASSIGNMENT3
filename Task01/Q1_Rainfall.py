import random
import time

def weekly_totals(readings):
    return [sum(readings[i:i+7]) for i in range(0, len(readings), 7)]

def moving_average_naive(readings, window=7):
    if window <= 0 or len(readings) < window:
        return []
    return [sum(readings[i:i+window]) / window
            for i in range(len(readings)-window+1)]

def moving_average_running(readings, window=7):
    if window <= 0 or len(readings) < window:
        return []
    total = sum(readings[:window])
    result = [total / window]
    for i in range(window, len(readings)):
        total += readings[i] - readings[i-window]
        result.append(total / window)
    return result

def analyse(readings):
    if not readings:
        raise ValueError("Readings list is empty")
    return {
        "weekly_totals": weekly_totals(readings),
        "maximum": (max(readings), readings.index(max(readings)) + 1),
        "minimum": (min(readings), readings.index(min(readings)) + 1),
        "moving_average": moving_average_running(readings),
        "dry_days": [i for i, value in enumerate(readings, 1) if value == 0]
    }

def experiment():
    random.seed(10)
    for n in (365, 36500, 365000):
        data = [random.randint(0, 80) for _ in range(n)]
        start = time.perf_counter()
        moving_average_naive(data)
        naive = time.perf_counter() - start
        start = time.perf_counter()
        moving_average_running(data)
        running = time.perf_counter() - start
        print(f"{n} readings: naive={naive:.6f}s, running-sum={running:.6f}s")

if __name__ == "__main__":
    sample = [0, 12, 8, 0, 20, 15, 10, 5, 0, 7, 14, 9, 11, 0]
    print(analyse(sample))
    print("readings[7:14]:", sample[7:14])
    print("readings[-7:]:", sample[-7:])
    print("readings[::7]:", sample[::7])
    print("Short list average:", moving_average_running([1, 2, 3]))
    try:
        analyse([])
    except ValueError as error:
        print("Empty list test:", error)
    experiment()
# Task 01 - Execution verified
