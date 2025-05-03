# Ask the user for two numbers, one at a time, and then print the result of dividing the first number by the second and also the remainder of the division.


def main():
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    if num2 == 0:
        print("Cannot divide by zero!")
    else:
        quotient = num1 / num2
        remainder = num1 % num2

        print("Quotient (result of division):", quotient)
        print("Remainder:", remainder)


if __name__ == "__main__":
    main()
