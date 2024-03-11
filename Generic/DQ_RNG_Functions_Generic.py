"""
@author: cleartonic
@editor: Paraz10
"""


import datetime
from tqdm import tqdm

"""
Calculate the next 'num' values of normal heal given a seed 'x'
@param seed: the seed as a hex string
@param num: the number of values to calculate
@param heal_lists_to_check: the list of heal values to check for, as lists of "num" integers
@author: cleartonic
"""
def advance(seed, num, heal_lists_to_check):
    heal_list = []
    heal_lists_to_check = [[33,30,40,33,40,40,32,30,32,30],[30,36,34,30,39,35,31,34,39,34]]
    rng = int(seed, base=16)
    rng_hex = hex(rng).replace('0x','').zfill(8)
    for i in range(0, num):
        starting_rng = rng_hex
        r12 = int('5D588B65', base=16)
        r14 = int('269EC3', base=16)
        rng = ((rng * r12) + r14)
        rng_hex = hex(rng).replace('0x','')
        if len(rng_hex) > 8:
            rng_hex = rng_hex[(len(rng_hex)-8):]
        #print(rng_hex)
            
        rng = int(rng_hex, base=16)
        hoimi = rng >> 16
        hoimi_mult = int('B', base=16) # 02080D58
        hoimi2 = (hoimi * hoimi_mult) >> 16
        heal_val = hoimi2 + 30
        heal_list.append(heal_val)
        rng = int(rng_hex, base=16)

        rng = ((rng * r12) + r14)
        rng_hex = hex(rng).replace('0x','')
        if len(rng_hex) > 8:
            rng_hex = rng_hex[(len(rng_hex)-8):]
        rng = int(rng_hex, base=16)

        rng = ((rng * r12) + r14)
        rng_hex = hex(rng).replace('0x','')
        if len(rng_hex) > 8:
            rng_hex = rng_hex[(len(rng_hex)-8):]
        rng = int(rng_hex, base=16)




        rng_hex = rng_hex[6:8] + rng_hex[4:6] + rng_hex[2:4] + rng_hex[0:2]

        #print("DEBUG: Starting RNG: " + starting_rng + "| Heal Value: " + str(heal_val) + "| Ending RNG: " + rng_hex)

    #print(str(heal_list))
    for heal_list_to_check in heal_lists_to_check:
        if heal_list == heal_list_to_check:
            print("MATCH: Starting RNG: " + seed + " | Heal value : " + str(heal_list[0]))
    
    return (heal_val)







"""
Calculate the next 'num' seeds given a seed 'x'
@param seed: the seed as a hex string
@param num: the number of seeds to calculate
@author: cleartonic
@editor: Paraz10
"""
def advance_rng(seed, num, display=True):
    rng = int(seed, base=16)
    rng_hex = hex(rng).replace('0x','**').zfill(8)
    if display:
        print("Starting seed : " + rng_hex)
    for i in range(0, num):
        r12 = int('5D588B65', base=16)
        r14 = int('269EC3', base=16)
        rng = ((rng * r12) + r14)
        rng_hex = hex(rng).replace('0x','')
        if len(rng_hex) > 8:
            rng_hex = rng_hex[(len(rng_hex)-8):]
        rng = int(rng_hex, base=16)

        if display:
            print("%s RNG : %s" % ("{:3}".format(str(i+1)), rng_hex))

    return [seed, rng_hex]


"""
Calculate the previous 'num' seeds given a seed 'x'
@param seed: the seed as a hex string
@param num: the number of seeds to calculate
@author: Paraz10
"""
def reverse_rng(seed, num, display=True):
    rng = int(seed, base=16)
    rng_hex = hex(rng).replace('0x','').zfill(8)
    for i in range(0, num):
        r12 = int('5D588B65', base=16)
        r14 = int('269EC3', base=16)
        rng = ((rng - r14) * pow(r12, -1, 2**32))
        rng_hex = hex(rng).replace('0x','')
        if len(rng_hex) > 8:
            rng_hex = rng_hex[(len(rng_hex)-8):]
        rng = int(rng_hex, base=16)

        if display:
            print("%s RNG : %s" % ("{:3}".format(str(-(i+1))), rng_hex))

    return [seed, rng_hex]



"""
For a list of seeds, check if one of them is reachable given a certain number of advances (6) and a range of seeds
@param start_seed: the starting seed as a hex string
@param end_seed: the ending seed as a hex string
@param checklist: the list of seeds to check for, as hex strings
@param nb_advances: the number of advances to check for each seed (default is 6)
@author: cleartonic
@editor: Paraz10
"""
def check_rng(start_seed, end_seed, checklist, nb_advances=6):
    #checklist = ['EE5A9B58']
    for i in range(int(start_seed, base=16), int(end_seed, base=16)):
        check = advance_rng(hex(i).replace('0x','').zfill(8), nb_advances, False)
        for c in checklist:
            if c == check[1]:
                print("MATCH: " + check[0] + " | " + check[1])





"""
Run a range of seeds and calculate the next 10 heal values for each seed
@param start_seed: the starting seed as a hex string
@param end_seed: the ending seed as a hex string
@author: cleartonic
@editor: Paraz10
"""
def start_run(start_seed, end_seed):
    start = datetime.datetime.now()
    print("Start time: " + str(start))
    for i in tqdm(range(int(start_seed, base=16), int(end_seed, base=16))): 
        #print("----" + hex(i) + "_" + str(i) + "----")
        advance(hex(i), 10)
    
    end = datetime.datetime.now()
    print("End time: " + str(end))
    print("Runtime in seconds: " + str((end-start).total_seconds()))

    







#WIP
"""
Calculate the previous 'num' seeds given a seed 'x' (not working)
@param x: the seed
@param num: the number of seeds to calculate
@author: cleartonic
@editor: Paraz10
"""
def reverse_advance(x, num=1):
    rng = x[4:]
    print("Seed : " + rng)
    rng = int(x, base=16)
    tmp0 = rng * int('8965', base=16)
    sd_tmp0 = tmp0 & int('FFFF', base=16)
    carry = tmp0
    carry = carry >> 16
    print(str(rng) + " | " + str(tmp0) + " | " + str(sd_tmp0) + " | " + str(carry))
    print(hex(rng) + " | " + hex(tmp0) + " | " + hex(sd_tmp0) + " | " + hex(carry))



