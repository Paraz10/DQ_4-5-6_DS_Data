

import datetime
from tqdm import tqdm

r12 = int('5D588B65', 16)
r14 = int('269EC3', 16)
base1 = 0x7e875695 # (Sometimes 7e875697 on my console) # Unique value used to generate the




# -----------------------------------------------------------------------------------------
# -------------------------------- Generic Functions --------------------------------------
# -----------------------------------------------------------------------------------------

"""
Calculate the next 'num' seeds given a seed 'x'
@param seed: the seed as an integer
@param num: the number of seeds to calculate
"""
def advance_rng(seed, num, display=False):
    rng = seed
    #r12 = int('5D588B65', 16)
    #r14 = int('269EC3', 16)

    if display:
        print("Starting seed : {:08X}".format(rng))

    for i in range(num):
        rng = (r12 * rng + r14) & 0xFFFFFFFF  # 32 bits mask
        if display:
            print(str(i+1) + " - RNG : {:08X}".format(rng) + " - Heal value: " + str(calculate_heal_value(rng)))

    return rng



"""
Calculate the previous 'num' seeds given a seed 'x'
@param seed: the seed as an integer
@param num: the number of seeds to calculate
"""
def reverse_rng(seed, num, display=False):
    #r12 = int('5D588B65', 16)  # multiplicateur
    #r14 = int('269EC3', 16)    # incrément
    mod = 0x100000000          # 2^32

    # Inverse modulaire de r12 modulo 2^32
    r12_inv = pow(r12, -1, mod)

    rng = seed
    if display:
        print("Starting seed : {:08X}".format(rng))

    for i in range(num):
        rng = (r12_inv * ((rng - r14) & 0xFFFFFFFF)) & 0xFFFFFFFF
        if display:
            print(str(-i-1) + " - RNG : {:08X}".format(rng))
    
    return rng


"""
Calculate the hoimi value that will come given a seed
@param seed: the seed as an integer
@param hoimi_mult: the multiplier for the hoimi value
"""
def calculate_hoimi_value(seed, hoimi_mult):
    rng = seed
    hoimi = rng >> 16
    hoimi2 = (hoimi * hoimi_mult) >> 16
    return hoimi2


"""
Calculate the heal value that will come given for a seed
@param seed: the seed as an integer
"""
def calculate_heal_value(seed):
    #hoimi_mult = int('B', base=16) # 02080D58
    heal_val = calculate_hoimi_value(seed, 0xB) + 30
    return heal_val



# -----------------------------------------------------------------------------------------
# -------------- Step 1 : Functions to find some of the seeds you hit  --------------------
# -----------------------------------------------------------------------------------------


"""
For a given seed, calculate the next num heal values and check if they match the given heal values
@param seed: the seed as an integer
@param num: the number of seeds to calculate
@param heal_lists_to_check: the list of list of num heal values to check
"""
def advance(seed, num, heal_lists_to_check):    
    rng = seed
    for i in range(0, num):
        rng = advance_rng(rng, 2)
        heal_val = calculate_heal_value(rng)

        j = 0
        while j < len(heal_lists_to_check):
            if heal_val != heal_lists_to_check[j][i]:
                heal_lists_to_check.pop(j)
                j -= 1
            j += 1
        if len(heal_lists_to_check) == 0:
            return None

        rng = advance_rng(rng, 2)

    print("\nSeed found : {:08X}".format(seed) + " for heal values " + str(heal_lists_to_check[0]))
    return seed



# -----------------------------------------------------------------------------------------
# ---------- Step 2 : Functions to find the unique value of your console  -----------------
# -----------------------------------------------------------------------------------------



"""
Process used to adjust the members of the dates and times in seed generation
@param value: the value as an integer
@return: the adjusted value as an integer
"""
def div_date_adjust(value):
    return value + (value // 0xA) * 6


"""
Encode a date into a 32-bit integer
@param year: the year as an integer
@param month: the month as an integer
@param day: the day as an integer
@return: the encoded date as a 32-bit integer
"""
def encode_date(year, month, day):
    if (year < 2000 or year > 2099):
        raise ValueError("Year must be between 2000 and 2099")
    if (month < 1 or month > 12):
        raise ValueError("Month must be between 1 and 12")
    if (day < 1 or day > 31):
        raise ValueError("Day must be between 1 and 31")
    if (month == 2 and day > 29):
        raise ValueError("February cannot have more than 29 days")
    if (month in [4, 6, 9, 11] and day > 30):
        raise ValueError("This month cannot have more than 30 days")
    
    date = datetime.datetime(year, month, day)
    weekday = date.weekday()
    weekday = (weekday + 1) % 7 # Sunday = 0, Monday = 1, ...

    year2 = year - 2000
    year2 = div_date_adjust(year2)
    month = div_date_adjust(month)
    day = div_date_adjust(day)

    encoded_date = (
        (year2 % 0xFF) << 0 |         # Store the last two digits of the year in the least significant byte
        (month & 0xFF) << 8 |         # Left shift month by 8 bits
        (day & 0xFF) << 16 |          # Left shift day by 16 bits
        (weekday & 0xFF) << 24        # Left shift weekday by 24 bits
    )

    return encoded_date


"""
Encode a time into a 32-bit integer
@param hour: the hour as an integer
@param minute: the minute as an integer
@param second: the second as an integer
@return: the encoded time as a 32-bit integer
"""
def encode_time(hour, minute, second):
    if not (0 <= hour <= 23 and 0 <= minute <= 59 and 0 <= second <= 59):
        raise ValueError("Invalid time input")

    encoded_time = 0

    # Hours encoding
    if hour <= 11:
        hour = div_date_adjust(hour)
        encoded_time |= hour  # Use adjusted hour directly
    elif hour <= 19:
        encoded_time |= (hour - 12 + 0x52)  # 0x52 = 82
    else:
        encoded_time |= (hour - 20 + 0x60)  # 0x60 = 96

    # Adjust minutes and seconds
    minute = div_date_adjust(minute)
    second = div_date_adjust(second)

    # Bit shifts
    encoded_time |= (minute << 8)   # Shift minutes to bits 8–15
    encoded_time |= (second << 16)  # Shift seconds to bits 16–23

    return encoded_time



"""
Generate a seed from a date
@param year: the year as an integer
@param month: the month as an integer
@param day: the day as an integer
@param hour: the hour as an integer
@param minute: the minute as an integer
@param second: the second as an integer
"""
def generate_seed_from_date(year, month, day, hour, minute, second):
    encoded_date = encode_date(year, month, day)
    encoded_time = encode_time(hour, minute, second)

    # Combine the encoded date and time with the base value
    seed = (base1 + encoded_date + encoded_time) & 0xFFFFFFFF  # Ensure the result is a 32-bit integer

    return seed


"""
Find the unique value of a console using a seed and the datetime used to hit it
@param seed : the seed as an integer that you get with the given date and time
@param year: the year as an integer
@param month: the month as an integer
@param day: the day as an integer
@param hour: the hour as an integer
@param minute: the minute as an integer
@param second: the second as an integer
"""
def find_base_from_seed(seed, year, month, day, hour, minute, second):
    encoded_date = encode_date(year, month, day)
    encoded_time = encode_time(hour, minute, second)
    base = (seed - encoded_date - encoded_time) & 0xFFFFFFFF  # Ensure the result is a 32-bit integer

    print("Base: " + hex(base).replace('0x','').zfill(8))
    return base



# -----------------------------------------------------------------------------------------
# -------------- Step 3 : Functions to manipulate RNG inside the game  --------------------
# -----------------------------------------------------------------------------------------





"""
Find the seeds that can win the casino, and find the ones reachable by a console with 50 less advance, filtered by the hitable seed prefixes
@param seed_prefixes: the seed prefixs as a list of integers
"""
def find_casino_wins(seed_prefixes):
    print("winning_seed,mother_seed,advance,startup_seed")
    #print("startup_seed,")
    for i in range(0, 0x10000000):
        seed2 = advance_rng(i, 1)
        # If the seed start with 0 (0x0XXXXXXXX), then it will be a winning seed and we continue
        if seed2 & 0xF0000000 == 0:

            seed3 = advance_rng(i, 2)
            if seed3 & 0xF0000000 == 0:

                seed4 = advance_rng(i, 3)
                if seed4 & 0xF0000000 == 0:

                    seed5 = advance_rng(i, 4)
                    if seed5 & 0xF0000000 == 0:

                        for j in range(0, 10):
                            startup_seed = reverse_rng(i, 50+j)
                            # If startup_seed has a prefix in the list of prefixes, print the seed
                            if startup_seed >> 24 in seed_prefixes: # (0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84)
                                print("{:08X}".format(i) + ",{:08X}".format(reverse_rng(i, 1)) + "," + str(50+j) + ",{:08X}".format(startup_seed))
                                print("0x{:08X}".format(startup_seed) + ",")
    



"""
Calculate all the initial seeds of the console and check if one of them match the given seeds
@param seeds: the list of seeds as integers
@return: the list of seeds and matched datetimes as strings
"""
def find_seeds_datetime(seeds):

    results = []

    for year in range(2000, 2100): # 2100
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    encoded_date = encode_date(year, month, day)
                except:
                    continue  # Invalid date

                partial_seed = (base1 + encoded_date) & 0xFFFFFFFF  # Ensure the result is a 32-bit integer

                # Try all possible hours, minutes, seconds
                for hour in range(24):
                    for minute in range(60):
                        for second in range(7,10):
                            try:
                                encoded_time = encode_time(hour, minute, second)
                            except:
                                continue # Invalid time
                            
                            generated_seed = (partial_seed + encoded_time) & 0xFFFFFFFF  # Ensure the result is a 32-bit integer
                            
                            has_matched = False
                            matched_seed = None
                            first_octet = (generated_seed >> 24) & 0xFF

                            for seed in seeds:
                                if generated_seed == seed:
                                    has_matched = True
                                    matched_seed = seed
                                    break
                            
                            if has_matched:
                                print(f"Found date for seed {matched_seed:08X} : {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
                                results.append(f"{matched_seed:08X} - {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")

    return results




