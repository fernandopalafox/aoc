# Open file
with open('input.txt', 'r') as file: 
    lines = file.readlines()

# Parse input
total = 0.0
newdigit = ""
for i in range(len(lines)): 
    digits = [char for char in lines[i] if char.isdigit()]
    
    if len(digits) == 1:
        newdigit = digits[0] + digits[0]
    else:
        newdigit = digits[0] + digits[-1]
    print(digits, newdigit)
    total += int(newdigit)

print(total)
    
