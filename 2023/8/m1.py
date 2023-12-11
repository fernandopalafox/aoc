lines = open(0).read().splitlines()
i = lines[0] # instructions

map_dict = {}
for line in lines[2:]:
    key, val = line.split(' = ')
    map_dict[key] = [val[1:4], val[6:9]]

c = 0
x = 'AAA'
while not x == 'ZZZ':
    m = 0 if i[c % len(i)] == 'L' else 1
    x = map_dict[x][m]
    c += 1
    print(m, x, c)

print(c)