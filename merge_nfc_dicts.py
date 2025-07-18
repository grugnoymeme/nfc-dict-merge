#!/usr/bin/env python3

import sys
import os

COL = 6

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1.nfc> <file2.nfc>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    print(file1, file2)

    with open(file1, 'r', encoding="utf-8") as fd:
        list_A = [line.strip() for line in fd if line and line[0] != '#' and len(line) > 4]
    print("list_A", len(list_A), file1)
    set_A = set(list_A)

    with open(file2, 'r', encoding="utf-8") as fd:
        list_B = [line.strip() for line in fd if line and line[0] != '#' and len(line) > 4]
    print("list_B", len(list_B), file2)
    set_B = set(list_B)

    diff_AB = set_A.difference(set_B)
    print("-------")
    print("diff list_A - list_B =", len(diff_AB))
    print(f"Unique to {file1}")
    len_AB = len(diff_AB)
    list_AB = sorted(list(diff_AB))
    for X in range(0, len_AB, COL):
        print(" ".join(list_AB[X:X + COL]))

    diff_BA = set_B.difference(set_A)
    print("-------")
    print("diff list_B - list_A =", len(diff_BA))
    print(f"Unique to {file2}")
    len_BA = len(diff_BA)
    list_BA = sorted(list(diff_BA))
    for X in range(0, len_BA, COL):
        print(" ".join(list_BA[X:X + COL]))

    common_keys = set_A.intersection(set_B)
    num_common = len(common_keys)

    print("-------")
    print(f"Found {num_common} common keys.")

    if num_common > 0:
        answer = input("Proceed to create a merged file without duplicates? (y/n): ").strip().lower()
        if answer not in ['y', 'yes']:
            print("Thanks, goodbye.")
            sys.exit(0)
    else:
        print("No duplicate keys found, proceeding to create the merged file.")

    while True:
        directory = input("Enter the directory where to save the merged file: ").strip()
        if os.path.isdir(directory):
            break
        else:
            print(f"Error: directory '{directory}' does not exist. Please try again.")

    while True:
        filename = input("Enter the filename (e.g. merged_dict.nfc): ").strip()
        full_path = os.path.join(directory, filename)
        if os.path.exists(full_path):
            print(f"Error: file '{full_path}' already exists. Choose a different name.")
        else:
            break

    union_set = set_A.union(set_B)
    union_list = sorted(union_set)

    try:
        with open(full_path, 'w', encoding="utf-8") as f:
            for line in union_list:
                f.write(line + "\n")
        print(f"Merged file saved to '{full_path}' with {len(union_list)} unique lines.")
    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    main()
