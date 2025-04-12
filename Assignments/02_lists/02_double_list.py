# Write a program that doubles each element in a list of numbers. For example, if you start with this list:

# numbers = [1, 2, 3, 4]


def main():
    Number: list[int] = [2 , 3 , 4 , 5]
    for i in range(len(Number)):  # Loop through the indices of the list
        elem_at_index = Number[i]  # Get the element at index i in the numbers list
        Number[i] = elem_at_index * 2
    print(Number)

if __name__ ==  "__main__":
    main()