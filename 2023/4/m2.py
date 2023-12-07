import re

# To run this in Windows, type `Get-Content t1.txt | python m1.py`

og_lines = open(0).read().splitlines()

# 2 matches 
# 1 match 
# 0 matches

def find_card_numbers(lines):
    card_nums = []
    for line in lines:   
        card_nums.append(int(re.findall(r'\d+', line.split(':')[0])[0]))
    return card_nums

def find_num_matches(line):
    line_blocks = line.split(':')[1].split('|')
    num_w = set(re.findall(r'\d+', line_blocks[0]))
    num_m = set(re.findall(r'\d+', line_blocks[1]))
    return len(num_m.intersection(num_w))

# def find_cards(cards): 
#     all_cards = []
#     for card in cards:         
#         num_matches = find_num_matches(card)
#         card_num = find_card_numbers([card])[0]
#         if not num_matches == 0: all_cards += [card]
#         print("num:", card_num, " matches: ", num_matches, " copies:", find_card_numbers(og_lines[card_num:(card_num+num_matches)]), "stack: ", find_card_numbers(all_cards))
#         if num_matches == 0: print("return ", find_card_numbers(all_cards))
#         if num_matches == 0: return all_cards
#         card_copies = find_cards(og_lines[card_num:card_num+num_matches])
#         all_cards += card_copies
#     return all_cards
    
# def find_cards(cards): 
#     all_cards = []
#     for card in cards:         
#         num_matches = find_num_matches(card)
#         card_num = find_card_numbers([card])[0]
#         new_copies = og_lines[card_num:card_num+num_matches]
#         all_cards += new_copies

#         if num_matches == 0: 
#             return []
#         else: 
#             print("current", find_card_numbers(all_cards), "recursive", find_card_numbers(find_cards(new_copies)))
#             all_cards += find_cards(new_copies)
#             return all_cards

counter = [1 for _ in range(len(og_lines))]
for card_index, card in enumerate(og_lines):
    card_num = card_index + 1
    num_matches = find_num_matches(card)
    new_copies = og_lines[card_num:card_num+num_matches]
    for _ in range(counter[card_index]):  
        for copy in new_copies:
            counter[find_card_numbers([copy])[0] - 1] += 1 
    # print(card_num, find_card_numbers(og_lines[card_num:card_num+num_matches]), counter)

print(sum(counter))

