import os, re, json

print("Brute force results")
for f in sorted(int(re.search("(\d+).", i.name).group(1)) for i in os.scandir("logs-bruteforce/data")):
    res = json.loads(open("logs-bruteforce/data/" + str(f) + ".json", "r").read())
    res = {int(i): res[i] for i in res}
    print(f"f({f}) = {min(res)}, {", ".join(str(i) for i in res[min(res)])}")

print("\nGeometric mean heuristic results")
for f in sorted(int(re.search("(\d+).", i.name).group(1)) for i in os.scandir("logs-geometric-mean/data")):
    res = json.loads(open("logs-geometric-mean/data/" + str(f) + ".json", "r").read())
    res = {int(i): res[i] for i in res}
    print(f"f({f}) = {min(res)}, {", ".join(str(i) for i in res[min(res)])}")