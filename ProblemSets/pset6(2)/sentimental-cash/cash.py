from cs50 import get_float

def get_cents():
    while True:
        n = get_float("Change owed: ")
        if n >= 0:
            break
        else:
            print("Please enter a non-negative value.")
    return round(n * 100)

def calculate_coins(cents, denomination):
    coins = cents // denomination
    cents = cents % denomination
    return coins, cents

def main():
    cents = get_cents()

    quarters, cents = calculate_coins(cents, 25)
    dimes, cents = calculate_coins(cents, 10)
    nickels, cents = calculate_coins(cents, 5)
    pennies = cents

    total_coins = quarters + dimes + nickels + pennies
    print(total_coins)


main()
