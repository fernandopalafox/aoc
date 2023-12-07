import re

lines = open(0).read().splitlines()
lines =  [line for line in lines if line.strip()] # remove empty lines
seed_numbers = list(map(int, re.findall(r'\d+', lines[0])))
seed_ranges = [range(seed_numbers[i],seed_numbers[i] + seed_numbers[i+1]) for i in range(0, len(seed_numbers), 2)]
# seed_ranges = [[seed_numbers[i]] for i in range(0, len(seed_numbers), 2)]


print(seed_ranges)

def query(s_query, ranges):
    for single_range in ranges:
        d, s, l = map(int, single_range)
        s_range = range(s, s + l)
        d_range = range(d, d + l)
        if s_query in s_range: 
            return d_range[s_range.index(s_query)]
    return s_query

def rev_query(d_query, ranges):
    for single_range in ranges: 
        d, s, l = map(int, single_range)
        s_range = range(s, s + l)
        d_range = range(d, d + l)
        if d_query in d_range: 
            return s_range[d_range.index(d_query)] 
    return d_query

def find_total_cat_range(cat_ranges): 
    upper = 0 
    lower = float('inf')
    for single_range in cat_ranges: 
        d, s, l = map(int, single_range)
        print(single_range)
        if d < lower: 
            lower = d
        if d + l > upper: 
            upper = d + l 
    return range(lower, upper)
    
def find_min(cat_ranges, seed_ranges): 
    # loc_range = find_total_cat_range(cat_ranges[-1])
    max_loc_num = float('inf')
    smallest_destination = 1
    i = len(cat_ranges) - 1
    # print("Max loc number", max_loc_num)
    while smallest_destination < max_loc_num:
        print("index = ", i, "smallest = ", smallest_destination)
        local_destination = smallest_destination
        while i >= 0: 
            required_source = rev_query(local_destination, cat_ranges[i])
            local_destination = required_source
            i -= 1
            # print("         ",i,"d", local_destination, "rs",required_source)
        # print("min loc.", smallest_destination, "rs", required_source)
        for seed_range in seed_ranges: 
            # print("    ", required_source, "in", seed_range, required_source in seed_range)
            if required_source in seed_range:
                return smallest_destination
        # print("Didn't work, resetting i and increasing smallest to", smallest_destination+1 )
        smallest_destination += 1
        i = len(cat_ranges) - 1

category_counter = 0
cat_ranges = []
for line in lines[1:]:
    if not line[0].isdigit():
        category_counter += 1
        cat_ranges.append([])
    else: 
        cat_ranges[category_counter - 1].append(re.findall(r'\d+', line))
        # if category_counter == 1: break
print(find_min(cat_ranges, seed_ranges))
    