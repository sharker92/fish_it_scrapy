import json


def main():
    with open("2023-08-05-full_alsuper.json", "r") as f:
        data = json.loads(f.read())
        keys = set()
        num = 0
        for d in data:
            num += 1
            for d in d.keys():
                keys.add(d)
        with open("keys.txt", "w") as file:
            file.write(str(keys))
        print(num)
        print(str(keys))


if __name__ == "__main__":
    main()
