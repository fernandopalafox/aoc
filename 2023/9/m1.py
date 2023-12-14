import re

hs = open(0).read().splitlines()

total = 0
for h in hs:
    ns = h.split()
    ds = list(map(int, ns))
    dn = []
    dns = [ds]

    compute_flag = True
    while compute_flag:
        for i, l in enumerate(ds[:-1]):
            dn.append(ds[i + 1] - ds[i])
        dns.append(dn)
        if len(set(dn)) == 1 and dn[0] == 0:
            compute_flag = False
        else: 
            ds = dn
            dn = []

    # Add zero to final sequence
    dns[-1].append(0)
    
    # Calculate new char
    dns.reverse()
    for i, dn in enumerate(dns[:-1]):
        dns[i+1].append(dn[-1] + dns[i+1][-1])

    total += dns[-1][-1]

print(total)
