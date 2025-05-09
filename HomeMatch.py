from real_estate_listing_generator import generate_real_estate_listings

def main():
    generate_new = input("Do you want to generate new real estate listings? (yes/no): ").strip().lower()
    
    if generate_new == "yes":
        try:
            num_properties = int(input("How many properties do you want to generate? "))
            temperature = float(input("What temperature value do you want to use? (0.0-2.0): "))

            # Validate inputs
            if num_properties <= 0:
                print("Number of properties must be positive. Using default value of 10.")
                num_properties = 10

            if temperature < 0 or temperature > 2:
                print("Temperature must be between 0 and 2. Using default value of 1.")
                temperature = 1

            result = generate_real_estate_listings(num_properties, temperature)
            print(result)
        except ValueError:
            print("Invalid input. Using default values: 10 properties with temperature 1.")
            result = generate_real_estate_listings()
            print(result)
    else:
        print("No new listings generated.")

if __name__ == "__main__":
    main()