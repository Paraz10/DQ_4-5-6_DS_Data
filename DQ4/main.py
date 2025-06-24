import DQ4_RNG_Functions as DQ
import datetime
from tqdm import tqdm



# heal_lists_data is a list of dictionaries containing heal values and their corresponding date and time
heal_lists_data = [
    {'heal_values' : [36,40,33,40,40,36,34,33,30,33], 'year': 2000, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 7},
    {'heal_values' : [35,37,34,36,39,30,38,38,32,35], 'year': 2000, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 8},
    {'heal_values' : [40,40,37,37,36,35,40,30,39,35], 'year': 2000, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 9},
    
    {'heal_values' : [31,34,30,35,32,38,30,31,34,39], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 8},
    {'heal_values' : [33,40,38,36,34,39,39,36,31,32], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 8}, # Anomaly
    {'heal_values' : [31,37,39,32,33,33,31,40,33,34], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 9}, # Anomaly
    {'heal_values' : [30,31,31,30,31,31,34,36,36,30], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 9},
    {'heal_values' : [33,37,35,30,34,30,32,37,38,39], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 10},
    {'heal_values' : [30,38,31,36,32,31,40,36,34,31], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 10}, # Anomaly
    {'heal_values' : [32,34,36,36,33,35,36,30,40,31], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 11}, # 1/2
    {'heal_values' : [30,39,39,35,31,33,38,36,32,37], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 11}, # 1/2
]




"""
Run a range of seeds and calculate the next 10 heal values for each seed
@param start_seed: the starting seed as an integer
@param end_seed: the ending seed as an integer
"""
def start_run(start_seed, end_seed):
    found_seeds = []

    for seed in tqdm(range(start_seed, end_seed)):
        matched_heal_values = DQ.advance(seed, 10, heal_lists_data)

        if matched_heal_values:
            seed_data = matched_heal_values.copy()
            seed_data['seed'] = seed
            # Reversing the seed to find the seed generated at the game boot
            seed_data['mother_seed'] = DQ.reverse_rng(seed, 6)
            found_seeds.append(seed_data)
    
    for seed_data in found_seeds:
        unique_base = DQ.find_base_from_seed(seed_data['mother_seed'], seed_data['year'], seed_data['month'], seed_data['day'], seed_data['hour'], seed_data['minute'], seed_data['second'])
        seed_data['unique_base'] = unique_base
    
    print("\n\nFinal result:")
    for seed_data in found_seeds:
        print(f"Seed: {seed_data['seed']:08X} - Mother seed : {seed_data['mother_seed']:08X} - Heal values: {seed_data['heal_values']} - Date: {seed_data['year']:04d}-{seed_data['month']:02d}-{seed_data['day']:02d} {seed_data['hour']:02d}:{seed_data['minute']:02d}:{seed_data['second']:02d} - Unique base: {seed_data['unique_base']:08X}")

    return found_seeds


start_run(0x00000000, 0x100000000)  # Run from seed 0 to 2^32 (0xFFFFFFFF)

