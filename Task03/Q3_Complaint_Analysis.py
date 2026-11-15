import random
import re
import time
from collections import Counter

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received"
]
STOP = {"not", "high"}

def frequencies(texts, stop):
    counts = {}
    for text in texts:
        for word in re.findall(r"[a-z]+", text.lower()):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts

def frequencies_setdefault(texts, stop):
    counts = {}
    for text in texts:
        for word in re.findall(r"[a-z]+", text.lower()):
            if word not in stop:
                counts.setdefault(word, 0)
                counts[word] += 1
    return counts

def group_by_district(records):
    district_complaints = {}
    for district, complaint in records:
        district_complaints.setdefault(district, []).append(complaint)
    return district_complaints

def top(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]

def benchmark():
    random.seed(5)
    vocabulary = ["seed", "price", "water", "crop", "loan", "fertiliser",
                  "subsidy", "farmer", "rain", "pest", "market", "soil"]
    for n in (1000, 10000, 100000):
        words = [random.choice(vocabulary) for _ in range(n)]
        start = time.perf_counter()
        counts = {}
        for word in words:
            counts[word] = counts.get(word, 0) + 1
        dict_time = time.perf_counter() - start
        start = time.perf_counter()
        distinct = set(words)
        list_counts = {word: words.count(word) for word in distinct}
        list_time = time.perf_counter() - start
        start = time.perf_counter()
        counter_counts = Counter(words)
        counter_time = time.perf_counter() - start
        print(f"n={n}: dictionary={dict_time:.6f}s list.count={list_time:.6f}s Counter={counter_time:.6f}s")

if __name__ == "__main__":
    counts = frequencies(calls, STOP)
    print(top(counts, 3))
    print("setdefault gives same counts:", frequencies_setdefault(calls, STOP) == counts)
    district_records = [
        ("Chittoor", "seeds not received"),
        ("Vellore", "water supply problem"),
        ("Chittoor", "fertiliser price high")
    ]
    print("District groups:", group_by_district(district_records))
    print("Empty input:", frequencies([], STOP))
    print("Case and punctuation:", frequencies(["SEEDS, seeds!"], STOP))
    benchmark()
