import json

with open("hui.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for i in data.values():
        for x in i:
            print(x)