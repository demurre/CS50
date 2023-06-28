def main():
    while True:
        try:
            height_input = input("Height: ")
            if height_input == "":
                raise ValueError("No input provided")
            n = int(height_input)
            if n <= 0:
                raise ValueError("Height must be a positive integer")
            if n > 8:
                raise ValueError("Maximum height allowed is 8")
            break
        except ValueError:
            print("Invalid input: ")

    for i in range(1, n + 1):
        for j in range(1, n - i + 1):
            print(" ", end="")
        for j in range(1, i + 1):
            print("#", end="")
        print()


main()
