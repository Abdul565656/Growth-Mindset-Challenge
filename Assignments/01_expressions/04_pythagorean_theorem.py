# Write a program that asks the user for the lengths of the two perpendicular sides of a right triangle and outputs the length of the third side (the hypotenuse) using the Pythagorean theorem!

# The Pythagorean theorem, named after the ancient Greek thinker, Pythagoras, is a fundamental relation in geometry. It states that in a right triangle, the square of the hypotenuse is equal to the sum of the square of the other two sides.



import math  

def main():
    side_a = float(input("Enter length of the first side (a): "))
    side_b = float(input("Enter length of the second side (b): "))


    hypotenuse = math.sqrt(side_a**2 + side_b**2)


    print("The length of the hypotenuse is:", hypotenuse)

if __name__ == "__main__":
    main()
