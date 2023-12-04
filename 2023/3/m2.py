import re 

with open('i1.txt', 'r') as file:
    lines = [line.strip() for line in file.readlines()]

def find_num_blocks(line):
    blocks = []
    in_block = False
    block_start = 0
    block_end = 0
    for line_num, char in enumerate(line): 
        if char.isdigit() and not in_block: 
            block_start = line_num
            in_block = True
        elif not char.isdigit() and in_block: 
            block_end = line_num - 1
            in_block = False
            blocks.append((block_start, block_end))
    if in_block: 
        block_end = len(line) - 1 # 0 indexing 
        blocks.append((block_start, block_end))

    return blocks

def find_sym_blocks(line):
    blocks = []
    in_block = False
    block_start = 0
    block_end = 0
    for line_num, char in enumerate(line): 
        if not char.isalnum() and not in_block and char == '*': 
            block_start = line_num
            in_block = True
        elif (char.isalnum() or char == '.') and in_block: # REPLACE THIS
            block_end = line_num - 1
            in_block = False
            blocks.append(block_start)
    if in_block:  
        block_end = len(line) - 1 # 0 indexing 
        blocks.append(block_start)
    return blocks

def check_adjacency(block_num, blocks_sym): 
    for block_sym in blocks_sym:
        if block_num[0]-1 <= block_sym <= block_num[1]+1:
            return True, block_sym
    
    return False, None
        


total = 0
part_dict = {}
for line_num, line in enumerate(lines): 
    # find number blocks for this line
    blocks_num = find_num_blocks(line)

    # If first line only check next line
    for block_num in blocks_num:
        # If last line only check before 
        if line_num == 0:
            below, sym_index_below = check_adjacency(block_num, find_sym_blocks(lines[line_num+1]))
            same,  sym_index_same =  check_adjacency(block_num, find_sym_blocks(lines[line_num]))
            if below:
                if not (line_num+1,sym_index_below) in part_dict:
                    part_dict[(line_num+1,sym_index_below)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num+1,sym_index_below)] * int(line[block_num[0]:block_num[1]+1])
            if same: 
                if not (line_num,sym_index_same) in part_dict:
                    part_dict[(line_num,sym_index_same)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num,sym_index_same)] * int(line[block_num[0]:block_num[1]+1])

        elif line_num == len(lines) - 1:
            above, sym_index_above = check_adjacency(block_num, find_sym_blocks(lines[line_num-1]))
            same, sym_index_same =  check_adjacency(block_num, find_sym_blocks(lines[line_num]))
            if above: 
                if not (line_num-1,sym_index_above) in part_dict:
                    part_dict[(line_num-1,sym_index_above)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num-1,sym_index_above)] * int(line[block_num[0]:block_num[1]+1])
            if same: 
                if not (line_num,sym_index_same) in part_dict:
                    part_dict[(line_num,sym_index_same)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num,sym_index_same)] * int(line[block_num[0]:block_num[1]+1])
        else:
            above, sym_index_above = check_adjacency(block_num, find_sym_blocks(lines[line_num-1]))
            below, sym_index_below = check_adjacency(block_num, find_sym_blocks(lines[line_num+1]))
            same, sym_index_same =  check_adjacency(block_num, find_sym_blocks(lines[line_num]))
            if above: 
                if not (line_num-1,sym_index_above) in part_dict:
                    part_dict[(line_num-1,sym_index_above)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num-1,sym_index_above)] * int(line[block_num[0]:block_num[1]+1])
            if below:
                if not (line_num+1,sym_index_below) in part_dict:
                    part_dict[(line_num+1,sym_index_below)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num+1,sym_index_below)] * int(line[block_num[0]:block_num[1]+1])
            if same: 
                if not (line_num,sym_index_same) in part_dict:
                    part_dict[(line_num,sym_index_same)] = int(line[block_num[0]:block_num[1]+1])
                else:
                    total += part_dict[(line_num,sym_index_same)] * int(line[block_num[0]:block_num[1]+1])
    
print(total)
            

