import axelrod as axl

filterset = {
    'stochastic': True
}
strategies = axl.filtered_strategies(filterset)
filterset = {
    'min_memory_depth': 1,
    'max_memory_depth': 4
}

for i in strategies:
    print(i)