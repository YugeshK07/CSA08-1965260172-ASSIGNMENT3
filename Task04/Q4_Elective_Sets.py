import random
import time

ai_elective = {"192311001", "192311004", "192311007", "192311009"}
iot_elective = {"192311002", "192311004", "192311009", "192311010"}
all_students = {f"192311{i:03d}" for i in range(1, 11)}

both = ai_elective & iot_elective
exactly_one = ai_elective ^ iot_elective
neither = all_students - (ai_elective | iot_elective)

print("clash:", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither:", sorted(neither))
print("Method check:",
      both == ai_elective.intersection(iot_elective),
      exactly_one == ai_elective.symmetric_difference(iot_elective),
      neither == all_students.difference(ai_elective.union(iot_elective)))

def test_edge_cases():
    empty = set()
    same = {"A", "B"}
    print("Empty elective clash:", empty & ai_elective)
    print("Identical electives - exactly one:", same ^ same)
    print("Identical electives - both:", same & same)

def benchmark(n):
    random.seed(4)
    universe = [str(i) for i in range(n * 2)]
    left = random.sample(universe, n)
    right = random.sample(universe, n)
    probes = left[:100]

    start = time.perf_counter()
    list_hits = sum(1 for value in probes if value in right)
    list_time = time.perf_counter() - start

    right_set = set(right)
    start = time.perf_counter()
    set_hits = sum(1 for value in probes if value in right_set)
    set_time = time.perf_counter() - start

    # Nested-loop and set intersection comparison on the same first 1,000 values.
    small_left, small_right = left[:1000], right[:1000]
    start = time.perf_counter()
    nested_common = {x for x in small_left for y in small_right if x == y}
    nested_time = time.perf_counter() - start
    start = time.perf_counter()
    operator_common = set(small_left) & set(small_right)
    operator_time = time.perf_counter() - start

    start = time.perf_counter()
    full_common = set(left) & set(right)
    full_set_time = time.perf_counter() - start
    print(f"n={n}: list 100-membership checks={list_time:.6f}s; "
          f"set 100-membership checks={set_time:.6f}s; hits equal={list_hits == set_hits}")
    print(f"same 1000x1000 subset: nested={nested_time:.6f}s; "
          f"set &={operator_time:.6f}s; results equal={nested_common == operator_common}")
    print(f"full set intersection: {len(full_common)} common students in {full_set_time:.6f}s")

if __name__ == "__main__":
    test_edge_cases()
    for n in (10000, 100000, 1000000):
        benchmark(n)
          # Task 04 - Execution verified
