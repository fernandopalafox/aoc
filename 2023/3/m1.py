import re 

with open('i1.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

def find_num_blocks(line):
    blocks = []
    in_block = False
    block_start = 0
    block_end = 0
    for index, char in enumerate(line): 
        if char.isdigit() and not in_block: 
            block_start = index
            in_block = True
        elif not char.isdigit() and in_block: 
            block_end = index - 1
            in_block = False
            blocks.append((block_start, block_end))
    if in_block: 
        block_end = len(line) - 1 # 0 indexing and ignore newline
        blocks.append((block_start, block_end))

    return blocks

def find_sym_blocks(line):
    blocks = []
    in_block = False
    block_start = 0
    block_end = 0
    for index, char in enumerate(line): 
        if not char.isalnum() and not in_block and not char == '.': 
            block_start = index
            in_block = True
        elif (char.isalnum() or char == '.') and in_block: 
            block_end = index - 1
            in_block = False
            blocks.append(block_start)
    if in_block:  
        block_end = len(line) - 1 # 0 indexing and ignore newline
        blocks.append(block_start)
    return blocks

def check_adjacency(block_num, blocks_sym): 
    return any(block_num[0]-1 <= sym_index <= block_num[1]+1 for sym_index in blocks_sym)

total = 0
for index, line in enumerate(lines): 
    # find blocks
    blocks_num = find_num_blocks(line)
    blocks_sym = find_sym_blocks(line)

    # print(line,  end="")

    # If first line only check next line
    for block_num in blocks_num:
        # If last line only check before 
        if index == 1:
            below = check_adjacency(block_num, find_sym_blocks(lines[index+1]))
            same =  check_adjacency(block_num, find_sym_blocks(lines[index]))
            is_part = below or same
        elif index == len(lines) - 1:
            above = check_adjacency(block_num, find_sym_blocks(lines[index-1]))
            same =  check_adjacency(block_num, find_sym_blocks(lines[index]))
            is_part = above or same
        else:
            above = check_adjacency(block_num, find_sym_blocks(lines[index-1]))
            below = check_adjacency(block_num, find_sym_blocks(lines[index+1]))
            same =  check_adjacency(block_num, find_sym_blocks(lines[index]))
            is_part = above or below or same
            
        # print("  ",line[block_num[0]:block_num[1]+1], is_part, end=" ")
        
        if is_part: 
            total += int(line[block_num[0]:block_num[1]+1]) # check inclusiveness

    
    # print("")
    
print(total)
            

