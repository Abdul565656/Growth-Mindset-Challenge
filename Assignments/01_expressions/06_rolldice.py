# Simulate rolling two dice, and prints results of each roll as well as the total.


import random  

def main():
    die1 = random.randint(1, 6)  
    die2 = random.randint(1, 6)  

   
    total = die1 + die2


    print("You rolled a", die1, "and a", die2)
    print("Total:", total)


if __name__ == "__main__":
    main()
