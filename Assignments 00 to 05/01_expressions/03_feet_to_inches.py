# Converts feet to inches. Feet is an American unit of measurement. There are 12 inches per foot. Foot is the singular, and feet is the plural.


inchesInFoot: int = 12

def main():
    feet: float = float(input("Enter The Number Of Feet"))
    inches: float  = feet * inchesInFoot 
    print(f"That is {inches} inches")


if __name__ == "__main__":
    main()