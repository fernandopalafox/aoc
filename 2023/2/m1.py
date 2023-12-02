import re 

# Open file
with open('t1.txt', 'r') as file: 
    lines = file.readlines()

# Set ground truth number of cubes
n_cubes = [12, 13, 14]
valid_IDs = []

pattern_ID = r'(Game )(\d{1,3})'
for line in lines: 
    ID = re.findall(pattern_ID, line)[0][1]
    
    # Separate draws
    blocks = re.split(r';\s*', line)
    valid_draws = True
    for block in blocks: 
        red = re.findall(r'(\d{1,2})( red)', block)
        green = re.findall(r'(\d{1,2})( green)', block)
        blue = re.findall(r'(\d{1,2})( blue)', block)
        if len(red) > 0 and int(red[0][0]) > n_cubes[0]:
            valid_draws = False
            print(ID, red[0], valid_draws)
            break
        if len(green) > 0 and int(green[0][0]) > n_cubes[1]:
            valid_draws = False
            print(ID, green[0], valid_draws)
            break
        if len(blue) > 0 and int(blue[0][0]) > n_cubes[2]: 
            valid_draws = False
            print(ID, blue[0], valid_draws)
            break
        print(ID, red, green, blue, valid_draws)

    # Add game ID if all draws valid
    if valid_draws:
        valid_IDs.append(int(ID))
        print(valid_IDs)

print(sum([ID for ID in valid_IDs]))


    
        