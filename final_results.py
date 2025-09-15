import os
import re
import json

# print brute results
print("Brute force results")
for f in os.scandir("logs-bruteforce/data"):
    res = json.loads(open("logs-bruteforce/data/" + f.name, "r").read())
    # get one result, could be more
    # dict key is a string
    print(f"f({re.search("(\d+).", f.name).group(1)}) = {min(res)}, {list(res[min(res)].keys())[0]}")

print("\nGeometric mean heuristic results")
for f in os.scandir("logs-geometric-mean/"):
    # forgot to save in data directory
    if f.name.endswith(".txt") or f.is_dir(): continue
    res = json.loads(open("logs-geometric-mean/" + f.name, "r").read())
    # get one result, could be more
    # dict key is a string
    print(f"f({re.search("(\d+).", f.name).group(1)}) = {min(res)}, {res[min(res)][0]}")