import math

race_time = 71530
record_distance = 940200


race_time = 45977295
record_distance = 305106211101695

t_lo = (race_time - (race_time**2 - 4* record_distance) ** (1/2))/2
t_hi = (race_time + (race_time**2 - 4* record_distance) ** (1/2))/2

num_wins = math.floor(t_hi) - math.floor(t_lo)

print(num_wins)