import DQ_RNG_Functions_Generic
import datetime
from tqdm import tqdm

def start_run(start_seed, end_seed):
    start = datetime.datetime.now()
    print("Start time: " + str(start))
    for i in tqdm(range(int(start_seed, base=16), int(end_seed, base=16))): 
        #print("----" + hex(i) + "_" + str(i) + "----")
        DQ_RNG_Functions_Generic.advance(hex(i), 10, [[33,30,40,33,40,40,32,30,32,30],[30,36,34,30,39,35,31,34,39,34]])
    
    end = datetime.datetime.now()
    print("End time: " + str(end))
    print("Runtime in seconds: " + str((end-start).total_seconds()))

def start_run_2():
    start = datetime.datetime.now()
    print("Start time: " + str(start))
    final_seed = None
    for i in tqdm(range(int('00000000', base=16), int('FFFFFFFF', base=16))):
        final_seed = advance(hex(i), 10)
        if final_seed != None:
            print("MATCH: " + final_seed + " | " + hex(int(final_seed, base=16)))
            print("MATCH: " + i + " | " + hex(int(i, base=16)))
            break
    end = datetime.datetime.now()
    print("End time: " + str(end))
    print("Runtime in seconds: " + str((end-start).total_seconds()))


def advance(seed, num):
    heal_lists_to_check = [[33,30,40,33,40,40,32,30,32,30], [30,36,34,30,39,35,31,34,39,34], [37,37,32,37,38,40,39,30,31,36], [40,31,39,38,39,34,40,37,35,36], [30,37,31,40,32,37,32,39,38,37]]
    rng = int(seed, base=16)
    rng_hex = hex(rng).replace('0x','').zfill(8)
    for i in range(0, num):
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
        rng = int(rng_hex, base=16)

        j = 0
        while j < len(heal_lists_to_check):
            if heal_val != heal_lists_to_check[j][i]:
                if i >= 8:
                    print("Heal values in common : " + str(i-1) + " for heal values " + str(heal_lists_to_check[j]) + ", seed : " + seed + " | " + str(int(seed, base=16)))
                heal_lists_to_check.pop(j)
                j -= 1
            j += 1
        if len(heal_lists_to_check) == 0:
            return None

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

    return seed


def main():
    #start_run('40000000', '4FFFFFFF') # EE5A9B48 - EE5A9B68 # 0-4 + A-F Done
    start_run_2() # A6000000





    

if __name__ == "__main__":
    main()