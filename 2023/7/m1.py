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
    if 5 in uc.values():
        return 6
    if 4 in uc.values():
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

def higher_rank(c1, c2):
    labels =  ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    if c1 == c2: 
        return -1
    elif labels.index(c1) < labels.index(c2):
        return 0
    else:
        return 1

def find_char_rank(c):
    labels =  ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    labels.reverse() # too lazy to do it manually
    return labels.index(c) # higher better

def break_ties(ties, start_idx): 
    indices = [i for i in range(len(ties))]
    new_order = []

    char_ranks = [find_char_rank(hand[start_idx]) for hand in ties]
    char_ranks_set = list(set(char_ranks))
    while len(new_order) < len(ties): 
        max_rank = max(char_ranks_set)
        highest_ties = [hand for idx, hand in enumerate(ties) if char_ranks[idx] == max_rank]
        highest_ties_indices = [idx for idx in indices if char_ranks[idx] == max_rank]
        # print(start_idx, max_rank, highest_ties)

        if len(highest_ties) == 1:
            new_order.append(indices[char_ranks.index(max_rank)])
        else:
            local_ranks = break_ties(highest_ties, start_idx + 1)
            local_ranks.reverse()
            for local_rank in local_ranks:
                new_order.append(highest_ties_indices[local_rank])
        
        char_ranks_set.remove(max_rank)

    new_order.reverse() 
    return new_order # low to high rank


def rank_by_char(hands, start_idx):
    return [find_char_rank(hand[start_idx]) for hand in hands]


# Find ranks
ranks = []
for hand in hands:
    ranks.append(find_rank(hand))

# Sort hands via first ranking rule
sorted_hands_1 = [tup[1] for tup in sorted(zip(ranks, hands))]
sorted_ranks_1 = sorted(ranks)


# # Sort hands via second ranking rule. Low to high 
# hands_sorted_final = []
# for rank in set(ranks):
#     hands_w_rank_sorted = [tup[1] for tup in hands_sorted_1 if tup[0] == rank] # unsorted at start
#     hands_w_rank_indices = [idx for idx in range(len(hands)) if hands_sorted_1[idx][0] == rank]
#     # Rank by char 
#     print(rank, hands_w_rank_sorted)
#     for start_idx in range(len(hands_w_rank_sorted[0])):
#         char_ranks = rank_by_char(hands_w_rank_sorted, start_idx)
#         hands_w_rank_sorted = [tup[1] for tup in sorted(zip(char_ranks, hands_w_rank_sorted))]
#         print(start_idx, hands_w_rank_sorted)
#     [hands_sorted_final.append(hand) for hand in hands_w_rank_sorted] # lo to hi 

    
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

print(hands, bids)
print(hands_sorted_final, bids_sorted)

# sum em up
total = 0 
for idx, bid in enumerate(bids_sorted):
    total += (idx + 1) * int(bid)
print(total)


# # Break ties
# for ri, rank in enumerate(ranks):
#     if ranks.count(rank) > 1: 
#         indices = [i for i in range(len(ranks)) if ranks[i] == rank]
#         tied_hands = [hands[i] for i in indices]
#         new_order = break_ties(tied_hands.copy(), 0)
#         print(tied_hands, new_order)
#         for idx, el in enumerate(new_order):
#             # guarantees same rank relative to non-ties but reshuffles ties
#             ranks[indices[el]] += (idx + 1) * 1/(ranks.count(rank) + 2) 

# # Sort according to ranks (low to high)
# sorted_hands =  [tup[1] for tup in sorted(zip(ranks,hands))]
# sorted_bids  =  [tup[1] for tup in sorted(zip(ranks,bids))]

# # Compute total winnings
# total_winnings = sum([(idx + 1) * int(sorted_bids[idx]) for idx in range(len(hands))])
# print(total_winnings)
