
if __name__ == '__main__':
    corp_list: list[list[str]] = [[], [], [], [], []]

    with open("../include/data.txt", 'r') as file:
        idx: int = 0

        while True:
            line = file.readline()

            if not line:
                break

            corp_list[idx % 5].append(line)
            idx += 1

    for i in range(5):
        with open(f"../include/group{i + 1}.txt", 'w') as file:
            for corp_name in corp_list[i]:
                file.write(corp_name)