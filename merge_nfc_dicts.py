#!/usr/bin/env python3

import sys
import os

COL = 6

def read_and_validate_keys(file_path):
    with open(file_path, 'r', encoding="utf-8") as fd:
        lines = []
        for line_num, line in enumerate(fd, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = line.upper()  # convert to uppercase
            if len(line) != 12:
                print(f"Errore: la chiave alla riga {line_num} di '{file_path}' non è lunga 12 caratteri: '{line}'")
                sys.exit(1)
            lines.append(line)
    return lines

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1.nfc> <file2.nfc>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    print(file1, file2)

    list_A = read_and_validate_keys(file1)
    list_B = read_and_validate_keys(file2)

    print("list_A", len(list_A), file1)
    print("list_B", len(list_B), file2)

    set_A = set(list_A)
    set_B = set(list_B)

    diff_AB = set_A.difference(set_B)
    print("-------")
    print("diff list_A - list_B =", len(diff_AB))
    print(f"Unique to {file1}")
    list_AB = sorted(diff_AB)
    for X in range(0, len(list_AB), COL):
        print(" ".join(list_AB[X:X + COL]))

    diff_BA = set_B.difference(set_A)
    print("-------")
    print("diff list_B - list_A =", len(diff_BA))
    print(f"Unique to {file2}")
    list_BA = sorted(diff_BA)
    for X in range(0, len(list_BA), COL):
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

    # Ask for directory until valid
    while True:
        directory = input("Enter the directory where to save the merged file: ").strip()
        if os.path.isdir(directory):
            break
        else:
            print(f"Error: directory '{directory}' does not exist. Please try again.")

    # Ask for filename until valid and not existing
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
        print(f"Merged file saved to '{full_path}' with {len(union_list)} unique 12-char uppercase keys.")
    except Exception as e:
        print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()
