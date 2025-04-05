# Write a program which asks the user what their favorite animal is, and then always responds with "My favorite animal is also ___!" (the blank should be filled in with the user-inputted animal, of course).


def main():
    var1 = input("What's your favourite animal")
    var2 = f'My favourite animal is also {var1}'
    print(var2)

if __name__ == '__main__':
  main()