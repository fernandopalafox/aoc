import re

ls = open(0).read().splitlines()
dims = [len(ls), len(ls[0])]

ps = ['|', '-', 'L', 'J', '7', 'F']

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
    print("  ", sc, cc, step_counter)
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
        print(ls[cc[0]][cc[1]], cc, ds[cc])

print(ds[max(ds, key=ds.get)])
                     
