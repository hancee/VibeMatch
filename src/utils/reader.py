def read_txt_to_list(fname):
    with open(fname, "r") as file:
        return [line.strip() for line in file.readlines()]
