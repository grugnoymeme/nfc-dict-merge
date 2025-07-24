# nfc-dict-merge

A simple tool to merge different NFC dictionaries by removing duplicate keys and cleaning the data.

## Usage
```
python3 merge_nfc_dicts.py first_dict.keys second_dict.txt third... fourth....
```

You can use any file extension. The script will:
- Check that all keys are exactly 6 bytes long (12 hexadecimal characters).
- Invalid keys are skipped and listed at the end of the output.
- Automatically convert all letters to uppercase for consistency.
- Prompt you to confirm merging if duplicate keys are found.
- Let you choose where to save the merged file, and ensure the filename does not already exist.
