import re

lines = open(0).read().splitlines()
lines =  [line for line in lines if line.strip()] # remove empty lines
seed_numbers = list(map(int, re.findall(r'\d+', lines[0])))

def query(s_query, ranges):
    for single_range in ranges:
        d, s, l = map(int, single_range)
        s_range = range(s, s + l)
        d_range = range(d, d + l)
        if s_query in s_range: 
            return d_range[s_range.index(s_query)]
    return s_query
        
category_counter = 0
category_ranges = []
for line in lines[1:]:
    if not line[0].isdigit():
        category_counter += 1
        category_ranges.append([])
    else: 
        category_ranges[category_counter - 1].append(re.findall(r'\d+', line))

lowest_location = float('inf')
for seed_number in seed_numbers:
    i_num = seed_number
    for category_range in category_ranges: 
        i_num = query(i_num, category_range)
        
    print(seed_number, i_num)
    if i_num < lowest_location: 
        lowest_location = i_num
print(lowest_location)