import re 

# Open file
with open('input1.txt', 'r') as file: 
    lines = file.readlines()

# Set ground truth number of cubes
n_cubes = [12, 13, 14]
powers = []

pattern_ID = r'(Game )(\d{1,3})'
for line in lines: 
    ID = re.findall(pattern_ID, line)[0][1]
    
    # Separate draws
    blocks = re.split(r';\s*', line)
    valid_draws = True
    max_r = 0
    max_g = 0
    max_b = 0 
    for block in blocks: 
        red = re.findall(r'(\d{1,2})( red)', block)
        green = re.findall(r'(\d{1,2})( green)', block)
        blue = re.findall(r'(\d{1,2})( blue)', block)
        if len(red) > 0 and int(red[0][0]) > max_r:
            max_r = int(red[0][0])
        if len(green) > 0 and int(green[0][0]) > max_g:
            max_g = int(green[0][0])
        if len(blue) > 0 and int(blue[0][0]) > max_b:
            max_b = int(blue[0][0])
    
    # Print and multiply
    powers.append(max_r * max_g * max_b)
    print(line, max_r, max_g, max_b)

print(sum([power for power in powers]))


    
        