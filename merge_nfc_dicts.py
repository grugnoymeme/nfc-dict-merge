#!/usr/bin/env python3

import sys
import os
import re

COL = 6

def read_and_validate_keys(file_path, invalid_keys_details, duplicates_tracker, file_tag):
    """
    Legge un file di chiavi NFC, trasforma tutte le lettere in maiuscolo,
    rimuove le stringhe che non sono di lunghezza 12 caratteri,
    rimuove quelle che contengono caratteri NON esadecimali (cioè, solo 0-9 e A-F),
    e gestisce i duplicati all'interno del file.

    Args:
        file_path (str): Il percorso del file di input contenente le chiavi NFC.
        invalid_keys_details (list): Lista per raccogliere i dettagli delle chiavi non valide.
        duplicates_tracker (set): Set per tracciare i duplicati trovati all'interno dei file.
        file_tag (str): Un tag descrittivo per il file (es. "file1", "file2", "File N").

    Returns:
        list: Una lista di chiavi valide e uniche estratte dal file.
    """
    seen_in_file = set()
    valid_keys = []

    
    valid_hex_pattern = re.compile(r'^[0-9A-F]{12}$')

    try:
        with open(file_path, 'r', encoding="utf-8") as fd:
            for line_num, line in enumerate(fd, 1):
                original_line = line.strip()
                if not original_line or original_line.startswith("#"):
                    continue
                
                key = original_line.upper()

                if len(key) != 12:
                    invalid_keys_details.append((file_tag, line_num, original_line, "lunghezza non 12"))
                    continue

                if not valid_hex_pattern.match(key):
                    invalid_keys_details.append((file_tag, line_num, original_line, "caratteri non esadecimali"))
                    continue

                if key in seen_in_file:
                    duplicates_tracker.add(key)
                    invalid_keys_details.append((file_tag, line_num, original_line, "duplicato interno al file"))
                    continue

                seen_in_file.add(key)
                valid_keys.append(key)
    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non è stato trovato. Verrà ignorato.")
    except Exception as e:
        print(f"Errore durante la lettura del file '{file_path}': {e}")

    return valid_keys

def print_key_block(title, keys):
    """Stampa un blocco di chiavi formattato."""
    print("-------")
    print(f"{title} = {len(keys)}")
    if keys:
        for i in range(0, len(keys), COL):
            print(" ".join(keys[i:i+COL]))
    else:
        print("Nessuna chiave.")

def main():
    """Funzione principale per unire e pulire i dizionari di chiavi."""
    if len(sys.argv) < 3:
        print(f"Uso: {sys.argv[0]} <file1> <file2> [file3 ... fileN]")
        sys.exit(1)

    input_files = sys.argv[1:]
    print(f"Unione dizionari:")
    for f in input_files:
        print(f"- '{f}'")

    invalid_keys_details = []
    duplicates_found_in_files = set()

    all_valid_keys_sets = []

    for i, file_path in enumerate(input_files):
        current_valid_keys = read_and_validate_keys(file_path, invalid_keys_details, duplicates_found_in_files, f"File {i+1} ('{os.path.basename(file_path)}')")
        all_valid_keys_sets.append(set(current_valid_keys))

    print("\n-------")
    print("Riepilogo chiavi valide caricate (dopo pulizia interna ai file):")
    for i, file_set in enumerate(all_valid_keys_sets):
        print(f"File {i+1} ('{os.path.basename(input_files[i])}'): {len(file_set)} chiavi uniche e valide.")

    if len(all_valid_keys_sets) > 0:
        merged_set = all_valid_keys_sets[0].copy()
        common_keys_across_all = all_valid_keys_sets[0].copy()

        for i in range(1, len(all_valid_keys_sets)):
            merged_set.update(all_valid_keys_sets[i])
            common_keys_across_all.intersection_update(all_valid_keys_sets[i])

        if len(all_valid_keys_sets) >= 2:
            set_A = all_valid_keys_sets[0]
            set_B = all_valid_keys_sets[1]
            diff_AB = sorted(list(set_A - set_B))
            diff_BA = sorted(list(set_B - set_A))
            common_first_two = sorted(list(set_A & set_B))

            print_key_block(f"Chiavi uniche solo in '{os.path.basename(input_files[0])}' (rispetto al secondo file)", diff_AB)
            print_key_block(f"Chiavi uniche solo in '{os.path.basename(input_files[1])}' (rispetto al primo file)", diff_BA)
            print_key_block(f"Chiavi comuni tra i primi due file", common_first_two)
        
        print_key_block(f"Chiavi comuni a TUTTI i file di input", sorted(list(common_keys_across_all)))

    else:
        merged_set = set()

    while True:
        directory = input("\nInserisci la directory dove salvare il file unito: ").strip()
        if os.path.isdir(directory):
            break
        else:
            print(f"Errore: la directory '{directory}' non esiste. Riprova.")

    while True:
        filename = input("Inserisci il nome del file (es. merged_dict.nfc): ").strip()
        full_path = os.path.join(directory, filename)
        if os.path.exists(full_path):
            print(f"Errore: il file '{full_path}' esiste già. Scegli un nome diverso.")
        else:
            break

    merged_list = sorted(list(merged_set))

    try:
        with open(full_path, 'w', encoding="utf-8") as f:
            for key in merged_list:
                f.write(key + "\n")
        print(f"\nFile unito salvato in '{full_path}' con {len(merged_list)} chiavi uniche, valide e in maiuscolo.")
        print("Nota: La validazione (lunghezza e caratteri esadecimali) è stata applicata a ciascun file di input.")
        print("Il file finale contiene solo chiavi che hanno superato questi controlli e sono state rese uniche.")

    except Exception as e:
        print(f"Errore durante il salvataggio del file: {e}")
        sys.exit(1)

    if duplicates_found_in_files:
        print("\n-------")
        print("Chiavi duplicate trovate all'interno degli stessi file di input e rimosse:")
        duplicates_list = sorted(list(duplicates_found_in_files))
        for i in range(0, len(duplicates_list), COL):
            print(" ".join(duplicates_list[i:i+COL]))
    else:
        print("\n-------")
        print("Nessuna chiave duplicata trovata all'interno degli stessi file di input.")

    if invalid_keys_details:
        print("\n-------")
        print("Chiavi ignorate a causa di lunghezza non 12 o caratteri non esadecimali:")
        for tag, line_num, line, reason in invalid_keys_details:
            print(f"'{tag}', riga {line_num}: '{line}' (Motivo: {reason})")
    else:
        print("\n-------")
        print("Nessuna chiave ignorata per lunghezza o caratteri non esadecimali.")

if __name__ == "__main__":
    main()
