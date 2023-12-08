import re 

lines = open(0).read().splitlines()
race_times = list(map(int, re.findall(r'\d+', lines[0])))
record_distances = list(map(int, re.findall(r'\d+', lines[1])))

full_product = 1
for race_index, race_time in enumerate(race_times):
    button_times = range(1,race_time + 1)
    num_beats = 0
    for button_time in button_times:
        remaining_time = race_time - button_time
        distance = button_time * remaining_time
        if distance > record_distances[race_index]:
            num_beats += 1 
    full_product *= num_beats
print(full_product)