import DQ6_RNG_Functions as DQ
import datetime
from tqdm import tqdm



# heal_lists_data is a list of dictionaries containing heal values and their corresponding date and time
heal_lists_data = [
    {'heal_values' : [37,38,40,35,30,30,30,38,34,34], 'year': 2000, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 10},
    {'heal_values' : [33,38,30,32,37,33,37,40,31,34], 'year': 2000, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 11},
    {'heal_values' : [30,37,31,40,32,37,32,31,39,33], 'year': 2000, 'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 12},
    
    {'heal_values' : [37,36,34,37,30,31,33,36,35,39], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 10},
    {'heal_values' : [40,40,40,40,31,36,34,34,37,35], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 10},
    {'heal_values' : [34,35,35,34,36,35,40,38,32,38], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 11},
    {'heal_values' : [30,35,36,31,32,38,36,40,30,38], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 12},
    {'heal_values' : [33,40,31,34,32,32,37,38,31,34], 'year': 2004, 'month': 3, 'day': 25, 'hour': 0, 'minute': 0, 'second': 12},
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
            seed_data = matched_heal_values
            seed_data['seed'] = seed
            # Reversing the seed to find the seed generated at the game boot
            seed_data['mother_seed'] = DQ.reverse_rng(seed, 3)
            found_seeds.append(seed_data)
    
    for seed_data in found_seeds:
        unique_base = DQ.find_base_from_seed(seed_data['mother_seed'], seed_data['year'], seed_data['month'], seed_data['day'], seed_data['hour'], seed_data['minute'], seed_data['second'])
        seed_data['unique_base'] = unique_base
    
    print("\n\nFinal result:")
    for seed_data in found_seeds:
        print(f"Seed: {seed_data['seed']:08X} - Mother seed : {seed_data['mother_seed']:08X} - Heal values: {seed_data['heal_values']} - Date: {seed_data['year']:04d}-{seed_data['month']:02d}-{seed_data['day']:02d} {seed_data['hour']:02d}:{seed_data['minute']:02d}:{seed_data['second']:02d} - Unique base: {seed_data['unique_base']:08X}")

    return found_seeds


start_run(0x00000000, 0x100000000)  # Run from seed 0 to 2^32 (0xFFFFFFFF)

