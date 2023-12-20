# Iterate through all tiles
# Dots in the border are not enclosed

# For each tile: 
# if not in loop, change to dot

# For each tile: 
    # if dot and if at border, 
        # run dfs and change to 'O'. This removes all non-enclosed stuff
    
# For each tile: 
    # If dot:  
        # For all neighbors
            # If a neighbor is squeezable L, J, 7, F
                # Run DFS and change to I 

# For each tile: 
    # count dots 

def dfs(cc, vs, tc, rc):
    if ls[cc[0]][cc[1]] == tc and cc not in vs:
        vs.add(cc)
        # print(cc)
        ll = list(ls[cc[0]])
        ll[cc[1]]= rc
        ls[cc[0]] = "".join(ll)
        # print(ll[cc[0]])
        if (cc[0] - 1, cc[1]) not in vs and cc[0] - 1 > 0: dfs((cc[0] - 1, cc[1]), vs, tc, rc) 
        if (cc[0] + 1, cc[1]) not in vs and cc[0] + 1 < dims[0]: dfs((cc[0] + 1, cc[1]), vs, tc, rc)
        if (cc[0], cc[1] - 1) not in vs and cc[1] - 1 > 0: dfs((cc[0], cc[1] - 1), vs, tc, rc)
        if (cc[0], cc[1] + 1) not in vs and cc[1] + 1 < dims[1]: dfs((cc[0], cc[1] + 1), vs, tc, rc)

    return None

# Find feasible directions
def find_fd(cc):
    r = cc[0]
    c = cc[1]
    fd = []
    h = ls[r][c]
    for i in range(4): # U, D, L, R
        # Check edges 
        if i == 0 and r == 0: 
            continue
        if i == 1 and r == len(ls) - 1:
            continue
        if i == 2 and c == 0:
            continue
        if i == 3 and c == len(ls[0]) - 1: 
            continue 

        # Query
        if i == 0:
            q = ls[r - 1][c]
        elif i == 1: 
            q = ls[r + 1][c]
        elif i == 2:
            q = ls[r][c - 1]
        else: 
            q = ls[r][c + 1]
        
        # Check compat (hacky and ugly)
        if h == '-' and q == '|' or h == '|' and q == '-':
            continue
        if h == '-' and (i == 0 or i == 1):
            continue
        if h == 'F' and (i == 0 or i == 2):
            continue
        if h == 'F' and i == 0 and q == '7':
            continue
        if h == 'J' and i == 1:
            continue
        if h == 'J' and i == 3 and q == 'J':
            continue
        if h == '7' and (i == 0 or i == 3):
            continue
        if h == 'F' and i == 0 and q == 'F':
            continue
        if h == '|' and i == 2 and q == 'F':
            continue
        if h == '|' and i == 2 and q == 'L':
            continue
        if h == 'L' and (i == 1 or i == 2):
            continue


        # Check order
        if i == 0 and q in set(['|', '7', 'F', 'S']):
            fd.append(i)
        if i == 1 and q in set(['|', 'L', 'J', 'S']):
            fd.append(i)
        if i == 2 and q in set(['-', 'L', 'F', 'S']): 
            fd.append(i)
        if i == 3 and q in set(['-', 'J', '7', 'S']):
            fd.append(i)  

    return fd

def step(cc, i): 
    c = cc[0]
    r = cc[1]
    if i == 0:
        return (c - 1, r)
    if i == 1:
        return (c + 1, r)
    if i == 2: 
        return (c, r - 1)  
    if i == 3:
        return (c, r + 1)
    
def select_d(prev, fds):
    if prev == 0:
        not_allowed = 1
    if prev == 1:
        not_allowed = 0
    if prev == 2:
        not_allowed = 3
    if prev == 3:
        not_allowed = 2

    for fd in fds: 
        if fd != not_allowed:
            return fd


ls = open(0).read().splitlines()
dims = [len(ls), len(ls[0])]
ps = ['|', '-', 'L', 'J', '7', 'F']

# Find start coordinates
sc = (0,0)
for r, l in enumerate(ls): 
    for c, char in enumerate(l):
        if char == 'S':
            sc = (int(r), int(c)) 

fds1 = find_fd(sc)
ds = {sc : 0}
for fd1 in fds1:
    step_counter = 1
    cc = step(sc, fd1)
    # print("  ", sc, cc, step_counter)
    prev_fd = fd1
    ds[cc] = step_counter
    # if cc in ds:
    #     if ds[cc] > step_counter:
    #         ds[cc] = step_counter
    #     else:
    #         ds[cc] = step_counter

    while cc != sc:
        fds = find_fd(cc)
        fd = select_d(prev_fd, fds)
        cc = step(cc, fd)
        prev_fd = fd
        step_counter += 1
        if cc in ds:
            if ds[cc] > step_counter:
                ds[cc] = step_counter
        else:
            ds[cc] = step_counter

dims = [len(ls), len(ls[0])]
sq = set(['L', 'J', '7', 'F'])
lsq = set(['L','F', ])
rsq = set(['J', '7', ])
vs = set()

# Junk pipe to dot
for row, l in enumerate(ls): 
    ll = list(l)
    for col, c in enumerate(l): 
        if (not (row, col) in ds) and c != '.':
            ll[col]= '.'
    ls[row] = "".join(ll)

# Remove all dot lines to reduce recursion depth
for row, l in enumerate(ls):
    if set(l) == {'.'}:
        ls[row] = "".join(['O'] * len(l))

for row, l in enumerate(ls):
    colmax = 0
    for col, c in enumerate(l):
        if l[0:col+1] == "".join(['.'] * (col + 1)):
            colmax = col
    ll = ['O'] * (colmax + 1)
    ll.append(l[colmax + 1:])
    ls[row] = "".join(ll)

# Border non-enclosed
for row, l in enumerate(ls):
    # 1 or last, check all cols
    if row == 0 or row == len(ls) - 1:
        for col, c in enumerate(l): 
            dfs((row,col), vs, '.', 'O')
    else: # check only first and last cols
        for col, c in [(0, l[0]), (len(l) - 1, l[-1])]: 
            dfs((row,col), vs, '.', 'O')

for row, l in enumerate(ls):
    for col, c in enumerate(l):
        if c == '.': 
            if ls[row - 1][col] == 'O':
                dfs((row,col), vs, '.', 'O')
            elif ls[row + 1][col] == 'O':
                dfs((row,col), vs, '.', 'O')
            elif ls[row][col - 1] == 'O':
                dfs((row,col), vs, '.', 'O')
            elif ls[row][col + 1] == 'O':
                dfs((row,col), vs, '.', 'O')



# Enclosed
for row, l in enumerate(ls): 
    for col, c in enumerate(l):
        sc = None
        id = None
        # If dot, look for squeezable pipes around
        if ls[row][col] == '.':
            if (row > 0 and ls[row - 1][col] in sq): 
                sc = (row - 1, col)
                if ls[row - 1][col]  == 'L':
                    id = 1 # left
                elif ls[row - 1][col] == 'J':
                    id = 1 # right
                else:
                    print('up')
                    assert False 
                print("up")
            elif (row < len(ls) - 1) and ls[row + 1][col] in sq:
                sc = (row + 1, col)
                if ls[row + 1][col] == '7':
                    id = 0 # right 
                elif ls[row + 1][col] == 'F':
                    id = 0 # left
                else:
                    print( ls[row][col], 'down',  ls[row + 1][col])
                    assert False 
                print("down")
            elif col > 0 and l[col - 1] in sq:
                sc = (row, col - 1)
                if l[col - 1] == '7':
                    id = 3 # up
                elif l[col - 1] == 'J':
                    id = 3 # down
                else:
                    print('left')
                    assert False
                print("left")
            elif col < len(l) - 1 and l[col + 1] in sq:
                sc = (row, col + 1)
                if l[col + 1] == 'F':
                    id = 2
                elif l[col + 1] == 'L':
                    id = 2
                else:
                    print('right')
                    assert False
                print("right")

            if id == None:
                continue

            # If squeezable pipe, follow pipe
            # Check presumed "inside" of loop 
            if not sc == None:
                prev_c = ls[sc[0]][sc[1]]
                print("start", sc, prev_c, id)
                fds = find_fd(sc)
                fd = fds[0]
                # cc = step(sc, fd)
                cc = sc
                prev_fd = fd
                nc = ls[cc[0]][cc[1]]

                run_flag = True

                while run_flag:
                    prev_c = ls[cc[0]][cc[1]]
                    fds = find_fd(cc)
                    fd = select_d(prev_fd, fds)
                    cc = step(cc, fd)
                    prev_fd = fd
                    nc = ls[cc[0]][cc[1]]

                    # So nasty fuck
                    if id == 0: 
                        if nc == '|' and (prev_fd == 0 or prev_fd == 1):
                            if prev_c == '7':
                                id = 2
                            elif prev_c == 'L':
                                id = 2
                            elif prev_c == 'F':
                                id = 3
                            elif prev_c == 'J':
                                id = 3
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == '7' and prev_fd == 0:
                            if prev_c == 'J':
                                id = 1
                            elif prev_c == 'L':
                                id = 0
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'J' and prev_fd == 1:
                            if prev_c == 'F':
                                id = 0
                            elif prev_c == '7':
                                id = 1
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'F' and prev_fd == 0:
                            if prev_c == 'J':
                                id = 0
                            elif prev_c == 'L':
                                id = 1
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'L' and prev_fd == 1:
                            if prev_c == 'F':
                                id = 1
                            elif prev_c == '7':
                                id = 0
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == '7' and prev_fd == 3:
                            id = 3
                        elif nc == 'J' and prev_fd == 3:
                            id = 2
                        elif nc == 'F' and prev_fd == 2:
                            id = 2
                        elif nc == 'L' and prev_fd == 2:
                            id = 3
                        elif nc == '-' and (prev_fd == 2 or prev_fd == 3):
                            id = 0
                        elif nc == 'S':
                            nf = select_d(prev_fd, find_fd(cc))
                            if nf == 0:
                                id = 3
                            if nf == 1:
                                id = 2
                            if nf == 2:
                                id = 0
                            if nf == 3:
                                id = 0
                        else: 
                            print(prev_fd, cc, nc, id)
                            assert False
                    elif id == 1:
                        if nc == '|' and (prev_fd == 0 or prev_fd == 1):
                            if prev_c == '7':
                                id = 2
                            elif prev_c == 'L':
                                id = 2
                            elif prev_c == 'F':
                                id = 3
                            elif prev_c == 'J':
                                id = 3
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == '7' and prev_fd == 0:
                            if prev_c == 'J':
                                id = 0
                            elif prev_c == 'L':
                                id = 1
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'J' and prev_fd == 1:
                            if prev_c == 'F':
                                id = 1
                            elif prev_c == '7':
                                id = 0
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'F' and prev_fd == 0:
                            if prev_c == 'J':
                                id = 1
                            elif prev_c == 'L':
                                id = 0
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'L' and prev_fd == 1:
                            if prev_c == 'F':
                                id = 0
                            elif prev_c == '7':
                                id = 1
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == '7' and prev_fd == 3:
                            id = 2
                        elif nc == 'J' and prev_fd == 3:
                            id = 3
                        elif nc == 'F' and prev_fd == 2:
                            id = 3
                        elif nc == 'L' and prev_fd == 2:
                            id = 2
                        elif nc == '-' and (prev_fd == 2 or prev_fd == 3):
                            id = 1
                        elif nc == 'S':
                            nf = select_d(prev_fd, find_fd(cc))
                            if nf == 0:
                                id = 2
                            if nf == 1:
                                id = 3
                            if nf == 2:
                                id = 1
                            if nf == 3:
                                id = 1
                        else: 
                            print(prev_fd, cc, nc, id)
                            assert False
                    elif id == 2:
                        if nc == '|' and (prev_fd == 0 or prev_fd == 1):
                            id = 2
                        elif nc == '7' and prev_fd == 0:
                            id = 1
                        elif nc == 'J' and prev_fd == 1:
                            id = 0
                        elif nc == 'F' and prev_fd == 0:
                            id = 0
                        elif nc == 'L' and prev_fd == 1:
                            id = 1
                        elif nc == '7' and prev_fd == 3:
                            if prev_c == 'F':
                                id = 3
                            elif prev_c == 'L':
                                id = 2
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'J' and prev_fd == 3:
                            if prev_c == 'F':
                                id = 2
                            elif prev_c == 'L':
                                id = 3
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'F' and prev_fd == 2:
                            if prev_c == '7':
                                id = 3
                            elif prev_c == 'J':
                                id = 2
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'L' and prev_fd == 2:
                            if prev_c == '7':
                                id = 2
                            elif prev_c == 'J':
                                id = 3
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == '-' and (prev_fd == 2 or prev_fd == 3):
                            if prev_c == '7':
                                id = 1
                            elif prev_c == 'L':
                                id = 1
                            elif prev_c == 'F':
                                id = 0
                            elif prev_c == 'J':
                                id = 0
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'S':
                            nf = select_d(prev_fd, find_fd(cc))
                            if nf == 0:
                                id = 2
                            if nf == 1:
                                id = 2
                            if nf == 2:
                                id = 0
                            if nf == 3:
                                id = 0
                        else: 
                            print(prev_fd, cc, nc, id)
                            assert False
                        # print(id)
                    elif id == 3:
                        if nc == '|' and (prev_fd == 0 or prev_fd == 1):
                            id = 3
                        elif nc == '7' and prev_fd == 0:
                            id = 0
                        elif nc == 'J' and prev_fd == 1:
                            id = 1
                        elif nc == 'F' and prev_fd == 0:
                            id = 1
                        elif nc == 'L' and prev_fd == 1:
                            id = 0
                        elif nc == '7' and prev_fd == 3:
                            if prev_c == 'F':
                                id = 2
                            elif prev_c == 'L':
                                id = 3
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'J' and prev_fd == 3:
                            if prev_c == 'F':
                                id = 3
                            elif prev_c == 'L':
                                id = 2
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'F' and prev_fd == 2:
                            if prev_c == '7':
                                id = 2
                            elif prev_c == 'J':
                                id = 3
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'L' and prev_fd == 2:
                            if prev_c == '7':
                                id = 3
                            elif prev_c == 'J':
                                id = 2
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == '-' and (prev_fd == 2 or prev_fd == 3):
                            if prev_c == '7':
                                id = 0
                            elif prev_c == 'L':
                                id = 0
                            elif prev_c == 'F':
                                id = 1
                            elif prev_c == 'J':
                                id = 1
                            else:
                                print(prev_fd, cc, nc, id)
                                assert False
                        elif nc == 'S':
                            nf = select_d(prev_fd, find_fd(cc))
                            if nf == 0:
                                id = 3
                            if nf == 1:
                                id = 3
                            if nf == 2:
                                id = 1
                            if nf == 3:
                                id = 1
                        else: 
                            print(prev_fd, cc, nc, id)
                            assert False
                        # print(id)
                    print(prev_fd, cc, nc, id)
                    assert not id == None

                    # Check inside
                    vc = None
                    if id == 0:
                        vc = ls[cc[0] - 1][cc[1]]   
                    elif id == 1:
                        vc = ls[cc[0] + 1][cc[1]]
                    elif id == 2:
                        if cc[1] - 1 >= 0:
                            vc = ls[cc[0]][cc[1] - 1]
                    else:
                        if cc[1] + 1 < len(ls[0]):
                            vc = ls[cc[0]][cc[1] + 1]
                    
                    # If "inside" is O, run dfs on start
                    if vc == 'O':
                        print('ding', cc, nc, id)
                        dfs((row,col), vs, '.', 'O')
                        run_flag = False

                    if cc == sc:
                        run_flag = False

# Replace all remaining dots with I
for row, l in enumerate(ls): 
    for col, c in enumerate(l):
        if c == '.':
            dfs((row,col), vs, '.', 'I')
                    

# Print and total
for l in ls:
    print(l)

total = 0
for row, l in enumerate(ls): 
    for col, c in enumerate(l): 
        if c == 'I': total += 1
print(total)

# Functions 
