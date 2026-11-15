import re
import time

contacts = [
    {"name": "Dr. Ravi", "phone": "+91 98400 12345", "email": "ravi@example.com"},
    {"name": "ravi kumar", "phone": "9840012345", "email": ""},
    {"name": "Ravi Kumar", "phone": "+91-98400-12345", "email": "ravi.k@example.com"},
    {"name": "Anita", "phone": "9876543210", "email": "anita@example.com"},
    {"name": "Anita S", "phone": "98765 43210", "email": ""}
]

def normalise_phone(phone):
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("91") and len(digits) == 12:
        digits = digits[2:]
    return digits

def normalise_name(name):
    name = re.sub(r"^(dr|mr|mrs|ms)\.?\s+", "", name.strip(), flags=re.I)
    return " ".join(name.lower().split())

def merge_contacts(records):
    merged = {}
    for person in records:
        phone = normalise_phone(person.get("phone", ""))
        key = phone if phone else "name:" + normalise_name(person.get("name", ""))
        if key not in merged:
            merged[key] = {"name": person.get("name", "").strip(),
                           "numbers": set(), "emails": set()}
        if person.get("phone"):
            merged[key]["numbers"].add(person["phone"].strip())
        if person.get("email"):
            merged[key]["emails"].add(person["email"].strip().lower())
        if len(person.get("name", "")) > len(merged[key]["name"]):
            merged[key]["name"] = person["name"].strip()
    return [{"name": item["name"], "numbers": sorted(item["numbers"]),
             "emails": sorted(item["emails"])} for item in merged.values()]

def pairwise_duplicate_checks(records):
    keys = [normalise_phone(x.get("phone", "")) for x in records]
    duplicates = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if keys[i] and keys[i] == keys[j]:
                duplicates.append((i, j))
    return duplicates

if __name__ == "__main__":
    print("Merged contacts:")
    for contact in merge_contacts(contacts):
        print(contact)
    print("Duplicate pairs:", pairwise_duplicate_checks(contacts))

    # Dictionary grouping measured at both requested sizes.
    for n in (1000, 100000):
        data = [{"name": f"Person {i}", "phone": f"90000{i:06d}",
                 "email": f"p{i}@example.com"} for i in range(n)]
        start = time.perf_counter()
        merge_contacts(data)
        dictionary_time = time.perf_counter() - start
        print(f"n={n}: dictionary grouping={dictionary_time:.6f}s")
    print("Pairwise comparison counts: n=1000 -> 499500; n=100000 -> 4999950000")
    print("Pairwise 100000 timing is not run because it would require about 5 billion comparisons.")
