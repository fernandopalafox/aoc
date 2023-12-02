with open('input.txt', 'r') as file: 
    lines = [line.rstrip('\n') for line in file.readlines()]

def convert_to_nums(line):
    nums = []
    strings = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    strings_dict = dict(zip(strings,['1','2','3','4','5','6','7','8','9']))

    sorted_strings = sorted(strings, key=len)
    
    # Iterate through all elements of string 
    i = 0
    while i < len(line):
        char = line[i]
        found_number = False
        if char.isdigit(): # If number, add to list
            nums.append(char)
            i += 1
            found_number = True
        else: # else, add to string 
            for num_string in sorted_strings:
                if num_string in line[i:i+5]:
                    if line[i:i+len(num_string)] == num_string:
                        found_number = True
                        nums.append(strings_dict[num_string])
                        i += len(num_string) - 1 # -1 in case overlap e.g., "oneight"
        if not(found_number): 
            i += 1
        # print(char, nums)

    return nums

total = 0.0
for index, line in enumerate(lines): 
    line_nums = convert_to_nums(line)

    summed_num = 0.0
    if len(line_nums) == 1:
        summed_num = int(line_nums[0]+line_nums[0])
    else: 
        summed_num = int(line_nums[0]+line_nums[-1])

    total += summed_num

    print(index, line, line_nums, summed_num, total)

print(total)
