# Get the number of semesters from the user
try:
    num_semesters = int(input("Enter the number of semesters: "))
except ValueError:
    print("Invalid input. Please enter a number.")
    exit()

# Initialize lists to store SGPA and credits
sgpa_list = []
credits_list = []

# Get SGPA and credits for each semester
for i in range(num_semesters):
    while True:
        try:
            sgpa = float(input(f"Enter SGPA for semester {i+1}: "))
            if 0 <= sgpa <= 10:
                break
            else:
                print("SGPA must be between 0 and 10.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            credits = int(input(f"Enter credits for semester {i+1}: "))
            if credits > 0:
                break
            else:
                print("Credits must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    sgpa_list.append(sgpa)
    credits_list.append(credits)

# Calculate CGPA
total_credits = sum(credits_list)
weighted_sgpa_sum = sum(sgpa * credit for sgpa, credit in zip(sgpa_list, credits_list))

if total_credits == 0:
    cgpa = 0
else:
    cgpa = weighted_sgpa_sum / total_credits

# Print the result
print(f"\nYour CGPA is: {cgpa:.2f}")