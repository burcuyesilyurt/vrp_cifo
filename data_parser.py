FILE_PATH = './CIFO2024/goeke-2018/c103C6.txt'

data = []


def parse_single_line(line):
    segments = line.split(' ')
    segments = list(filter(lambda x: x != '' and x != '\n', segments))
    return segments


def parse_file(file_path):
    with open(FILE_PATH, 'r') as f:
        next(f)  # Skip the first line
        lines = f.readlines()
        for line in lines:
            if line == '\n':
                break

            data.append(parse_single_line(line))

    return data

print(parse_file(FILE_PATH))