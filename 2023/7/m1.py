import re 

lines = open(0).read().splitlines()
hands = []
bids = []
for line in lines: 
    hand, bid = line.split()
    hands.append(hand)
    bids.append(bid)

def find_rank(hand):
    us = set(hand)
    uc = {c : 0 for c in us}
    for c in hand: 
        uc[c] += 1
    if 5 in uc.values(): # 5ok
        return 8
    if 4 in uc.values(): #4ok
        return 7
    if 3 in uc.values() and 2 in uc.values(): # fh
        return 5
    if 3 in uc.values(): 
        return 4
    if list(uc.values()).count(2) == 2:
        return 3
    if list(uc.values()).count(2) == 1:
        return 2
    else: 
        assert len(us) == 5
        return 1    

def find_char_rank(c):
    labels =  ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    labels.reverse() # too lazy to do it manually
    return labels.index(c) # higher better

def rank_by_char(hands, start_idx):
    return [find_char_rank(hand[start_idx]) for hand in hands]

# Find ranks
ranks_1 = []
for hand in hands:
    ranks_1.append(find_rank(hand))

# Sort hands via first ranking rule
sorted_hands_1 = [tup[1] for tup in sorted(zip(ranks_1, hands))]
sorted_ranks_1 = sorted(ranks_1)

# Sort hands via second rule. Lo to high, recursively
def sort_by_char(sorted_hands, start_idx, ranks=None):
    if ranks == None: ranks = rank_by_char(sorted_hands, start_idx)
    final_sort = []
    for rank in sorted(set(ranks)):
        hands_w_this_rank = [hand for idx, hand in enumerate(sorted_hands) if ranks[idx] == rank] 
        if len(hands_w_this_rank) > 1: 
            # new_sorted_hands = sort_by_char(hands_w_this_rank, start_idx + 1)
            final_sort = final_sort + sort_by_char(hands_w_this_rank, start_idx + 1)
        else:
            hands_w_this_rank.reverse()
            final_sort.append(hands_w_this_rank[0])
    print(start_idx, final_sort)
    return final_sort
    
hands_sorted_final = sort_by_char(sorted_hands_1, -1, ranks=sorted_ranks_1)

# Sort bids 
bids_sorted = [] 
for hand in hands_sorted_final: 
    [bids_sorted.append(bid) for idx, bid in enumerate(bids) if hands[idx] == hand]

print(hands)
print(bids)
print(hands_sorted_final)
print(bids_sorted)

# sum em up
total = 0 
for idx, bid in enumerate(bids_sorted):
    print(hands_sorted_final[idx], bid)
    total += (idx + 1) * int(bid)
print(total)