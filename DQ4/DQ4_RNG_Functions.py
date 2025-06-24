

import datetime

r12 = int('5D588B65', 16)
r14 = int('269EC3', 16)
 # Unique value used to generate the seeds when booting the game
base1 = 0x7E7D555F # (Sometimes 0x7E7D5560 on my console, depends of the datetimes and the Modulo 2 of the number of times I changed the date or time on my console)




# -----------------------------------------------------------------------------------------
# -------------------------------- Generic Functions --------------------------------------
# -----------------------------------------------------------------------------------------

"""
Calculate the next 'num' seeds given a seed 'x'
@param seed: the seed as an integer
@param num: the number of seeds to calculate
"""
def advance_rng(seed: int, num: int, display: bool = False) -> int:
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
def reverse_rng(seed: int, num: int, display: bool = False) -> int:
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
def calculate_hoimi_value(seed: int, hoimi_mult: int) -> int:
    rng = seed
    hoimi = rng >> 16
    hoimi2 = (hoimi * hoimi_mult) >> 16
    return hoimi2


"""
Calculate the heal value that will come given for a seed
@param seed: the seed as an integer
"""
def calculate_heal_value(seed: int) -> int:
    #hoimi_mult = int('B', base=16) # 02080D58
    heal_val = calculate_hoimi_value(seed, 0xB) + 30
    return heal_val


"""
Calculate the amount of stat gained from a Seed of Strength or Wisdom for a given seed
@param seed: the seed as an integer
"""
def calculate_life_seed_value_1(seed: int) -> int:
    seed_val = calculate_hoimi_value(seed, 0x3) + 1
    return seed_val


"""
Calculate the amount of stat gained from a Seed of Magic or Resilience for a given seed
@param seed: the seed as an integer
"""
def calculate_life_seed_value_2(seed: int) -> int:
    seed_val = calculate_hoimi_value(seed, 0x3) + 3
    return seed_val


"""
Calculate the amount of stat gained from a Seed of Life for a given seed
@param seed: the seed as an integer
"""
def calculate_life_seed_value_3(seed: int) -> int:
    seed_val = calculate_hoimi_value(seed, 0x3) + 4
    return seed_val

"""
Calculate the amount of stat gained from a Seed of Agility for a given seed
@param seed: the seed as an integer
"""
def calculate_life_seed_value_4(seed: int) -> int:
    seed_val = calculate_hoimi_value(seed, 0x2) + 1
    return seed_val


"""
Check if a seed will drop an item with a given drop rate (works for recruitment and item drops)
@param seed: the seed as an integer of 32 bits
@param drop_rate: the power of 2 of the drop rate (e.g. 1/64 = 2^6 = 6 -> 6)
"""
def will_seed_drop_item(seed: int, drop_rate: int) -> bool:
    rng = seed
    # Ensure drop_rate is between 0 and 31
    if drop_rate < 0 or drop_rate > 31:
        raise ValueError("drop_rate must be between 0 and 31")
    
    # Check if the first drop_rate bits of the seed are 0
    for i in range(32, 32-drop_rate-1, -1):
        # check the i-th bit of the seed
        if (rng >> i) != 0:
            return False
    return True  # If all bits are 0, the item will drop




# -----------------------------------------------------------------------------------------
# -------------- Step 1 : Functions to find some of the seeds you hit  --------------------
# -----------------------------------------------------------------------------------------


"""
For a given seed, calculate the next num heal values and check if they match the given heal values
@param seed: the seed as an integer
@param nb_heal_values: the number of heal values to check
@param heal_lists_to_check: the dictionary containing the heal values to check against
"""
def advance(seed: int, nb_heal_values: int, heal_lists_to_check: list) -> dict:   
    rng = seed
    # Generate a list of indexes to store wich heal list to continue to check
    index_list = []
    for nb_heal_list in range(len(heal_lists_to_check)):
        index_list.append(nb_heal_list)

    for i in range(0, nb_heal_values):
        rng = advance_rng(rng, 1)
        heal_val = calculate_heal_value(rng)

        j = 0
        while j < len(index_list):
            if heal_val != heal_lists_to_check[index_list[j]]['heal_values'][i]:
                index_list.pop(j)
                j -= 1
            j += 1
        if len(index_list) == 0:
            return None

        rng = advance_rng(rng, 2)

    print("\nSeed found : {:08X}".format(seed) + " for heal data : " + str(heal_lists_to_check[index_list[0]]))
    return heal_lists_to_check[index_list[0]]  # Return the first element of the list, which is the one that matches the seed's heal values



# -----------------------------------------------------------------------------------------
# ---------- Step 2 : Functions to find the unique value of your console  -----------------
# -----------------------------------------------------------------------------------------



"""
Process used to adjust the members of the dates and times in seed generation
@param value: the value as an integer
@return: the adjusted value as an integer
"""
def div_date_adjust(value: int) -> int:
    return value + (value // 0xA) * 6


"""
Encode a date into a 32-bit integer
@param year: the year as an integer
@param month: the month as an integer
@param day: the day as an integer
@return: the encoded date as a 32-bit integer
"""
def encode_date(year: int, month: int, day: int) -> int:
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
def encode_time(hour: int, minute: int, second: int) -> int:
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
def generate_seed_from_date(year: int, month: int, day: int, hour: int, minute: int, second: int) -> int:
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
def find_base_from_seed(seed: int, year: int, month: int, day: int, hour: int, minute: int, second: int) -> int:
    encoded_date = encode_date(year, month, day)
    encoded_time = encode_time(hour, minute, second)
    base = (seed - encoded_date - encoded_time) & 0xFFFFFFFF  # Ensure the result is a 32-bit integer

    # print("Base: " + hex(base).replace('0x','').zfill(8))
    return base



# -----------------------------------------------------------------------------------------
# -------------- Step 3 : Functions to manipulate RNG inside the game  --------------------
# -----------------------------------------------------------------------------------------


"""
Generate the card value at the poker for a given seed
@param seed: the seed as an integer
@return: the card value as an integer
"""
def generate_card_for_seed(seed: int) -> int:
    card_val = calculate_hoimi_value(seed, 0x35)
    return card_val



"""
Find the seeds that will generate a Royal Slime Flush in Poker (only in the first draw). The Royal Slime Flush must be 10 J Q K A of slime and exclude the Joker
Card values are genrated in order from As to King for each color, in the order Blue, Red, Green, Yellow. The Joker is card 52.
@param seed_prefixes: the list of prefixes to check for the seed (e.g. [0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84])
@param minimum_advance: the minimum advance to apply to the seed (default is 50)
@param maximum_advance: the maximum advance to apply to the seed (default is 60)
@return: the list of seeds that will generate a Royal Flush
"""
def find_poker_royal_flush_first_draw(seed_prefixes: list, minimum_advance: int = 50, maximum_advance: int = 60) -> list:
    winning_combinaison = [0, 9, 10, 11, 12]  # Royal Slime Flush combination
    results = []
    for seed in range(0x00000000, 0x100000000):  # 0x00000000 to 0xFFFFFFFF
        rng = seed
        first_draw = []

        # Genrate the first 5 cards
        while len(first_draw) < 5:
            rng = advance_rng(rng, 1)
            card_value = generate_card_for_seed(rng)
            if card_value not in winning_combinaison:
                break # If the card is not in the winning combination, break the loop
            if card_value not in first_draw:
                first_draw.append(card_value)
            
        if len(first_draw) == 5:
            for advance in range(minimum_advance, maximum_advance + 1):
                startup_seed = reverse_rng(seed, advance)
                # If startup_seed has a prefix in the list of prefixes, print the seed
                if startup_seed >> 24 in seed_prefixes: # (0x7E, 0x7F, 0x80, 0x81, 0x82, 0x83, 0x84)
                    results.append(startup_seed)

    return results


"""
Calculate all the initial seeds of the console and check if one of them match the given seeds
@param seeds: the list of seeds as integers
@return: the list of seeds and matched datetimes as strings
"""
def find_seeds_datetime(seeds: list) -> list:

    results = []

    for year in range(2000, 2100): # 2000, 2100
        for month in range(1, 13): # 1, 13
            for day in range(1, 32): # 1, 32
                try:
                    encoded_date = encode_date(year, month, day)
                except:
                    continue  # Invalid date

                partial_seed = (base1 + encoded_date) & 0xFFFFFFFF  # Ensure the result is a 32-bit integer

                # Try all possible hours, minutes, seconds
                for hour in range(24):
                    for minute in range(60):
                        for second in range(7,8):
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
                                #print(f"Found date for seed 0x{matched_seed:08X} {matched_seed} : {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")
                                results.append(f"0x{matched_seed:08X} {matched_seed} - {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}")

    results.sort()  # Sort results by seed value
    return results




