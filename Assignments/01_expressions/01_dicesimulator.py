

# Simulate rolling two dice, three times. Prints
# the results of each die roll. This program is used
# to show how variable scope works.

# Import the random library which lets us simulate random things like dice!
import random

NUM_SIDES = 6

def roll_dice():
    die1: int = random.randint(1, NUM_SIDES)  # Local scope
    die2: int = random.randint(1, NUM_SIDES)  # Local scope
    total: int = die1 + die2  # Local scope
    print(f"Rolled: Die 1 = {die1}, Die 2 = {die2}, Total = {total}")

def main():
    die1: int = 10  
    print("die1 in main() starts as:", die1)
    
    roll_dice()
    roll_dice()
    roll_dice()
    
    print("die1 in main() is:", die1)


if __name__ == '__main__':
    main()
