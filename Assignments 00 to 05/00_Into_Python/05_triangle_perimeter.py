# Prompt the user to enter the lengths of each side of a triangle and then calculate and print the perimeter of the triangle (the sum of all of the side lengths).


def main():
    length1: float = float(input("Enter the first side "))
    length2: float = float(input("Enter your second side "))
    length3: float = float(input("Enter the third side "))
    perimeter = length1 + length2 + length3
    print(f"The Perimeter of the traingle is {perimeter}")

if __name__ == '__main__':
    main()
