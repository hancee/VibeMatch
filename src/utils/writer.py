import os
import csv


def _file_exists(fname):
    return os.path.isfile(fname)


def write_list_to_txt(lst, fname):
    with open(fname, "w") as file:
        for item in lst:
            file.write(item + "\n")


def write_record_to_csv(records, fname, headers, encoding="utf-8"):
    # Check if file exists, if not write header
    file_exists = _file_exists(fname)

    with open(fname, mode="a", newline="", encoding=encoding) as file:
        writer = csv.writer(file)

        if not file_exists:
            # Write the headers only if the file doesn't exist yet
            writer.writerow(headers)

        # Write each perfume's data row
        writer.writerow(records)


def write_list_to_file(file_name, list_name, list_values):
    with open(file_name, "a") as f:
        f.write(f"{list_name} = {list_values}\n")


def write_dict_to_file(file_name, dict_name, dict_values):
    with open(file_name, "a") as f:
        f.write(f"{dict_name} = {dict_values}\n")
