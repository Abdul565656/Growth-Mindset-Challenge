# Write a program that continually reads in mass from the user and then outputs the equivalent energy using Einstein's mass-energy equivalence formula (E stands for energy, m stands for mass, and C is the speed of light:

# E = m * c**2

# Almost 100 years ago, Albert Einstein famously discovered that mass and energy are interchangeable and are related by the above equation. You should ask the user for mass (m) in kilograms and use a constant value for the speed of light -- C = 299792458 m/s.


C: int = 299792458  # speed of light in m/s

def main():
    while True:
        mass_in_kg: float = float(input("Enter kilos of mass (0 to quit): "))
        
        if mass_in_kg == 0:
            break

        energy_in_joules: float = mass_in_kg * (C ** 2)

        print("e = m * (c^2)...")
        print("m = " + str(mass_in_kg) + " kg")
        print("c = " + str(C) + " m/s")
        print(str(energy_in_joules) + " joules of energy!\n")


if __name__ == "__main__":
    main()


