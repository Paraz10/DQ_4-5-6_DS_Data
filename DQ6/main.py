import DQ6_RNG_Functions as DQ
import datetime


heal_lists_to_check = [
        [37,38,40,35,30,30,30,38,34,34], 
        [33,38,30,32,37,33,37,40,31,34], 
        [30,37,31,40,32,37,32,31,39,33], 
        [37,36,34,37,30,31,33,36,35,39], 
        [40,40,40,40,31,36,34,34,37,35],
        [34,35,35,34,36,35,40,38,32,38],
        [30,35,36,31,32,38,36,40,30,38],
        [33,40,31,34,32,32,37,38,31,34]
    ]




"""
Run a range of seeds and calculate the next 10 heal values for each seed
@param start_seed: the starting seed as a hex string
@param end_seed: the ending seed as a hex string
"""
def start_run(start_seed, end_seed):
    for i in tqdm(range(int(start_seed, base=16), int(end_seed, base=16))): 
        #print("----" + hex(i) + "_" + str(i) + "----")
        advance(i, 10)












