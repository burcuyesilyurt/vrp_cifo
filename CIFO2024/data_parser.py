FILE_PATH = 'goeke-2018/c103C6.txt'

data = []


def parse_single_line(line):
    """
    Parses a single line of text by splitting it into segments and filtering out empty strings and newline characters.

    Args:
        line (str): A single line of text to be parsed.

    Returns:
        list: A list of non-empty string segments obtained from the input line.
    """
    segments = line.split(' ')
    segments = list(filter(lambda x: x != '' and x != '\n', segments))
    return segments


def parse_file(file_path):
    """
    Parses a file by reading its contents and processing each line except the first one.
    Empty lines or lines containing only a newline character terminate the reading process.

    Args:
        file_path (str): The path to the file to be parsed.

    Returns:
        list: A list of lists, where each sublist contains segments of a line parsed from the file.
    """
    with open(FILE_PATH, 'r') as f:
        next(f)  # Skip the first line
        lines = f.readlines()
        for line in lines:
            if line == '\n':
                break

            data.append(parse_single_line(line))

    return data

print(parse_file(FILE_PATH))