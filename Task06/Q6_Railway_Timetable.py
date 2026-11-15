import random
import sys
import time

timetable = {
    "12601": {"name": "Chennai Mail",
              "stops": [("Chennai Central","06:00","06:10"),("Arakkonam","07:20","07:22"),("Katpadi","08:15","08:20")],
              "days": {"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}},
    "12602": {"name": "Bengaluru Express",
              "stops": [("Chennai Central","07:00","07:15"),("Katpadi","09:10","09:15"),("Jolarpettai","10:30","10:35")],
              "days": {"Mon","Tue","Wed","Thu","Fri"}},
    "16089": {"name": "Yelagiri Express",
              "stops": [("Chennai Central","08:00","08:10"),("Arakkonam","09:25","09:27"),("Jolarpettai","11:00","11:05")],
              "days": {"Sat","Sun"}},
    "12007": {"name": "Shatabdi",
              "stops": [("Chennai Central","05:50","06:00"),("Katpadi","07:35","07:37")],
              "days": {"Mon","Tue","Wed","Thu","Fri","Sat"}},
    "12675": {"name": "Kovai Express",
              "stops": [("Chennai Central","06:10","06:20"),("Arakkonam","07:30","07:32"),("Katpadi","08:25","08:30")],
              "days": {"Mon","Tue","Wed","Thu","Fri","Sat","Sun"}}
}

def station_query(data, station, day):
    found = []
    for number, train in data.items():
        if day in train["days"]:
            for name, arrival, departure in train["stops"]:
                if name == station:
                    found.append((number, train["name"], arrival, departure))
    return sorted(found, key=lambda row: row[3])

def build_index(data):
    index = {}
    for number, train in data.items():
        for station, arrival, departure in train["stops"]:
            index.setdefault(station, []).append((number, arrival, departure, train["days"]))
    return index

def indexed_query(index, station, day):
    return [row for row in index.get(station, []) if day in row[3]]

def experiment():
    random.seed(3)
    stations = [f"Station{i}" for i in range(100)]
    for n in (100, 1000, 10000):
        data = {}
        for i in range(n):
            chosen = random.sample(stations, 5)
            data[str(i)] = {"name": f"Train{i}",
                            "stops": [(s, "08:00", "08:05") for s in chosen],
                            "days": {"Mon", "Wed", "Fri"}}
        start = time.perf_counter()
        station_query(data, "Station10", "Mon")
        scan_time = time.perf_counter() - start
        start = time.perf_counter()
        index = build_index(data)
        build_time = time.perf_counter() - start
        start = time.perf_counter()
        indexed_query(index, "Station10", "Mon")
        lookup_time = time.perf_counter() - start
        print(f"trains={n}: scan={scan_time:.6f}s index-build={build_time:.6f}s "
              f"indexed-query={lookup_time:.6f}s index-size={sys.getsizeof(index)} bytes")

if __name__ == "__main__":
    print("Katpadi on Mon:", station_query(timetable, "Katpadi", "Mon"))
    print("Third stop departure for 12601:", timetable["12601"]["stops"][2][2])
    print("Unknown station:", station_query(timetable, "Unknown", "Mon"))
    print("Train not running on Sunday:", station_query(timetable, "Katpadi", "Sun"))
    index = build_index(timetable)
    print("Indexed Katpadi:", indexed_query(index, "Katpadi", "Mon"))
    experiment()
