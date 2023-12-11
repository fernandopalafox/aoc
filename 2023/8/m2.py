lines = open(0).read().splitlines()
i = lines[0] # instructions

map_dict = {}
ps = []
for idx, line in enumerate(lines[2:]):
    key, val = line.split(' = ')
    map_dict[key] = [val[1:4], val[6:9]]
    ps.append(key) if key[2] == 'A' else None

print(ps)

c = 0 
all_ps = 0
while all_ps < len(ps):
    all_ps = 0
    for j, p in enumerate(ps):
        a = 0 if i[c % len(i)] == 'L' else 1
        ps[j] = map_dict[p][a]
        # print(c, p, a, ps[j])
        if ps[j][2] == 'Z':
            all_ps += 1
    c += 1
    print(c, ps) if c % 10000000 == 0 else None
print(c)