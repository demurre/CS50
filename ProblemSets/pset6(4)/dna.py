import csv
import sys


def main():
    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py database.csv sequence.txt")
        return

    # Read command-line arguments
    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    # Read database file into a variable
    database = read_csv(database_file)

    # Read DNA sequence file into a variable
    sequence = read_sequence(sequence_file)

    # Find longest match of each STR in DNA sequence
    counts = find_str_counts(database, sequence)

    # Check database for matching profiles
    match = find_matching_profile(database, counts)

    # Print the result
    if match:
        print(match["name"])
    else:
        print("No match")


def read_csv(filename):
    """Reads a CSV file and returns a list of dictionaries representing the rows."""
    rows = []
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)
    return rows


def read_sequence(filename):
    """Reads a text file and returns its contents as a string."""
    with open(filename, "r") as file:
        sequence = file.read().replace("\n", "")
    return sequence


def find_str_counts(database, sequence):
    """Finds the longest match of each STR in the DNA sequence and returns a dictionary of the counts."""
    counts = {}
    for row in database:
        for str_name in row.keys():
            if str_name != "name":
                str_count = longest_match(sequence, str_name)
                counts[str_name] = str_count
    return counts


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length

            if sequence[start:end] == subsequence:
                count += 1
            else:
                break

        longest_run = max(longest_run, count)

    return longest_run


def find_matching_profile(database, counts):
    """Finds a matching profile in the database based on the STR counts."""
    for row in database:
        match = True
        for str_name, str_count in counts.items():
            if str_name != "name" and int(row[str_name]) != str_count:
                match = False
                break
        if match:
            return row
    return None


main()