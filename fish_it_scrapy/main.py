import json


def main():

    # with open("ms-products-alsuper-2023-08-08.json", "r") as f:
    with open("products-alsuper-2023-08-08.json", "r") as f:
        data = json.loads(f.read())
        keys = set()
        num = 0
        for d in data:
            num += 1
            # for d in d.keys():
            for d in d['data'].keys():
                keys.add(d)
        with open("keys.txt", "w") as file:
            file.write(str(keys))
        print(num)
        print(str(sorted(keys)))


if __name__ == "__main__":
    main()
