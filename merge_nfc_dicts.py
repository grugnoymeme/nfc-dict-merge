#!/usr/bin/env python3

import sys
import os

COL = 6  # colonne per stampa ordinata

def read_and_validate_keys(file_path, invalid_keys, duplicates_tracker, file_tag):
    seen = set()
    valid_keys = []

    with open(file_path, 'r', encoding="utf-8") as fd:
        for line_num, line in enumerate(fd, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key = line.upper()
            if len(key) != 12:
                invalid_keys.append((file_tag, line_num, line))
                continue
            if key in seen:
                duplicates_tracker.add(key)
                continue
            seen.add(key)
            valid_keys.append(key)

    return valid_keys

def print_key_block(title, keys):
    print("-------")
    print(f"{title} = {len(keys)}")
    for i in range(0, len(keys), COL):
        print(" ".join(keys[i:i+COL]))

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file1> <file2>")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    print(f"Merging:\n- {file1}\n- {file2}")

    invalid_keys = []
    duplicates_found = set()

    list_A = read_and_validate_keys(file1, invalid_keys, duplicates_found, "file1")
    list_B = read_and_validate_keys(file2, invalid_keys, duplicates_found, "file2")

    print("-------")
    print("Valid keys loaded:")
    print(f"{file1}: {len(list_A)} keys")
    print(f"{file2}: {len(list_B)} keys")

    set_A, set_B = set(list_A), set(list_B)

    # Differenze tra i due file
    diff_AB = sorted(set_A - set_B)
    diff_BA = sorted(set_B - set_A)
    common_keys = set_A & set_B

    print_key_block(f"Unique to {file1}", diff_AB)
    print_key_block(f"Unique to {file2}", diff_BA)

    print("-------")
    print(f"Found {len(common_keys)} common keys.")

    # Chiedi directory valida per il file finale
    while True:
        directory = input("Enter the directory where to save the merged file: ").strip()
        if os.path.isdir(directory):
            break
        else:
            print(f"Error: directory '{directory}' does not exist. Please try again.")

    # Chiedi filename fino a che non è valido e non esiste
    while True:
        filename = input("Enter the filename (e.g. merged_dict.nfc): ").strip()
        full_path = os.path.join(directory, filename)
        if os.path.exists(full_path):
            print(f"Error: file '{full_path}' already exists. Choose a different name.")
        else:
            break

    # Unione e scrittura
    merged_set = (set_A | set_B) - duplicates_found
    merged_list = sorted(merged_set)

    try:
        with open(full_path, 'w', encoding="utf-8") as f:
            for key in merged_list:
                f.write(key + "\n")
        print(f"\nMerged file saved to '{full_path}' with {len(merged_list)} unique 12-char uppercase keys.\n")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)

    # Elenco chiavi duplicate
    if duplicates_found:
        print("-------")
        print("These keys were found duplicated in the same input file and have been removed from the final output:")
        duplicates_list = sorted(duplicates_found)
        for i in range(0, len(duplicates_list), COL):
            print(" ".join(duplicates_list[i:i+COL]))

    # Elenco chiavi non valide
    if invalid_keys:
        print("-------")
        print("These keys were ignored due to invalid length (not 12 characters):")
        for tag, line_num, line in invalid_keys:
            print(f"{tag}, line {line_num}: '{line}'")

if __name__ == "__main__":
    main()
