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


def main():
    start_run('E0000000', 'EFFFFFFF') # EE5A9B48 - EE5A9B68 # 0-3 + F Done





    

if __name__ == "__main__":
    main()