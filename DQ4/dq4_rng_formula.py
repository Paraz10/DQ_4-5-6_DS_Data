"""
@author: cleartonic
@editor: Paraz10
"""


import datetime

"""
Calculate the next 'num' values of normal heal given a seed 'x'
@param x: the seed
@param num: the number of values to calculate
@author: cleartonic
"""
def advance(x,num):
    heal_list = []
    checked_heal_lists = []
    rng = int(x, base=16)
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

    print(str(heal_list))
    for checked_heal_list in checked_heal_lists:
        if heal_list == checked_heal_list:
            print("MATCH: Starting RNG: " + x + " | Heal value : " + str(heal_list[0]))
    
    return (heal_val)







"""
Calculate the next 'num' seeds given a seed 'x'
@param x: the seed
@param num: the number of seeds to calculate
@author: cleartonic
@editor: Paraz10
"""
def advance_rng(x, num, display=True):
    rng = int(x, base=16)
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

    return [x, rng_hex]


"""
Calculate the previous 'num' seeds given a seed 'x'
@author: Paraz10
"""
def reverse_rng(x, num, display=True):
    rng = int(x, base=16)
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

    return [x, rng_hex]



"""
For a list of seeds, check if one of them is reachable given a certain number of advances (6) and a range of seeds
@author: cleartonic
@editor: Paraz10
"""
def check_rng():
    checklist = ['EE5A9B58']
    for i in range(int('087c5500', base=16), int('0A7F5500', base=16)):
        check = advance_rng(hex(i).replace('0x','').zfill(8), 6, False)
        for c in checklist:
            if c == check[1]:
                print("MATCH: " + check[0] + " | " + check[1])





"""
Run a range of seeds and calculate the next 10 heal values for each seed
@author: cleartonic
@editor: Paraz10
"""
def start_run():
    start = datetime.datetime.now()
    print("Start time: " + str(start))
    for i in range(int('EE5A9B48', base=16), int('EE5A9B68', base=16)):
        print("----" + hex(i) + "_" + str(i) + "----")
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




def main():
    RNG = 'EDF5A839' #'ADEFD53A' #'EE5A9B58'

    adv1 = '74D008F2'
    adv2 = 'A5BFC367'

    advance_rng(RNG, 20)
    
    reverse_rng("74D008F2", 6)
    reverse_rng("A5BFC367", 6)

    #advance(RNG, 10)

    #random_example = '9AB89A68'
    #advance(random_example, 10)

    #start_run()


if __name__ == "__main__":
    main()