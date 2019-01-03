import math
import time

from BloomFilter import BloomFilter 

from random import shuffle 
from random import randrange

import multiprocessing as mp
from multiprocessing.managers import BaseManager

class MyManager(BaseManager):
    pass

def evaluate_error_rate(word_present, word_absent, bloom_filter, test_size):
    """
     evaluate error rate by randomly accesing  by given test_size
    """
    for item in word_present:
        bloom_filter.add(item)
  
    # random shuffle
    shuffle(word_present) 
    shuffle(word_absent) 

    present_size = (int)(test_size / 2)
    absent_size = test_size - present_size

    test_words = word_present[:present_size] + word_absent[:absent_size]
    word_absent_set = set(word_absent[:absent_size])
   

    fp_cnt = 0
    total_cn = test_size *2

    for word in test_words:
        if bloom_filter.may_match(word):
            if word in word_absent_set:
                fp_cnt = fp_cnt + 1

    return  fp_cnt / total_cn

def evaluate_hash_count_and_ratio(items_count, fp_list):
    """
     evaluate hash Count and array size by given desgired false positive probability only
    """
    print(f'====================================================================================')
    print(f'evaluate hash Count and items_count / array size ratio ')
    print(f'====================================================================================')

    for fp_prob in fp_list:
        size = BloomFilter.get_size(items_count,fp_prob)
        ratio = size / items_count
        print(f'false_positive: {fp_prob} \
             array_size: {size}')
        # two options for calculation
        print(f'hash_count: {BloomFilter.get_hash_count_by_array_size_and_element_size(size, items_count)} \
             ratio: {format(ratio, ".2e")}')
        print(f'hash_countByProb: {BloomFilter.get_hash_count_by_fp_prob(fp_prob)} \
             ratio: {format(ratio, ".2e")}')

def evaluate_fp_rate(items_count, fp_list, hash_cnt_list):
    """
     evaluate false positive rate by given desgired false positive probability and given k hash function constraints
    """

    print(f'===============================================================================================================')
    print(f'evaluate false positive probailitiy by given desgired false positive probability and given k hash function constraints')
    print(f'===============================================================================================================')

    for fp_prob in fp_list:
        for hash_cnt in hash_cnt_list:

            size = BloomFilter.get_size_by_hash_count_and_fp_prob(items_count, hash_cnt, fp_prob)
    
            ratio = size / items_count

            print(f'false_positive:{fp_prob} \
                array_size: {size} \
                hash_count: {hash_cnt} \
                ratio: {format(ratio, ".2e")} \
                space(MB): {format(size / math.pow(2, 20) / 8, "f")}')

def test_real_fp_prob(filename, fp_prob=0.01, hash_cnt=3, iteration=30, test_size=10000):
    """
    test false positive probability by given desgired false positive probability and given k hash function constraints
    """
    word_list = []
    int_file = None
    try:
        # use ISO for weird character
        int_file = open(filename, "r", encoding = "ISO-8859-1")
        while True:
            line = int_file.readline().replace('\n','')
            if not line:
                break
            word_list.append(line)
    except Exception as excep:
        raise
    finally:
        if int_file is not None:
            int_file.close()

    print(f'===============================================================================================================')
    print(f'test false positive probability by given desgired false positive probability and given k hash function constraints')
    print(f'===============================================================================================================')
    if test_size <= 0:
        raise ValueError("test_size must bigger than zero")
    if len(word_list) <= 1:
        raise ValueError("word_list_size must be at least 2")

    word_present_cnt = (int)(len(word_list)/2)
    word_absent_cnt = len(word_list) - word_present_cnt

    word_present = word_list[:word_present_cnt]
    word_absent = word_list[word_present_cnt:]

    # number of items being insert
    items_count = word_present_cnt

    bloom_filter = BloomFilter(items_count, fp_prob, hash_cnt) 
    print(f'word_list size: {len(word_list)}')
    print(f'iteration: {iteration}')
    print(f'input test size: {test_size}')

    # use smaller cnt as possible test_size
    test_size = min(test_size, len(word_list))
    print(f'adjusted test size: {test_size}')

    for iter in range(iteration):
        print (f'test false positive rate: \
            {format(evaluate_error_rate(word_present, word_absent, bloom_filter, min(test_size, len(word_list))), "f")}')

def write_test(name, bloom_filter, data, lock):
    try:
        lock.acquire() 
        bloom_filter.add(data)
        print (f'{name} add data: {data}')
    except Exception as e:
        raise
    finally:
        lock.release() 

def read_test(name, bloom_filter, data, lock):
    try:
        lock.acquire() 
        res = bloom_filter.may_match(data)
        print (f'{name} look up data: {data} = {res}')
    except Exception as e:
        raise
    finally:
        lock.release() 

def read_write_multiprocess_test(num_of_process, items_count, fp_rpob, hash_cnt):
    """
    test read write  random multiprocess test'
    """
    print(f'===============================================================================================================')
    print(f'test read write  random multiprocess test')
    print(f'===============================================================================================================')
    if num_of_process <= 0:
        raise ValueError("num_of_process must bigger than zero")

    
    MyManager.register('BloomFilter', BloomFilter)

    manager = MyManager()
    manager.start()

    word_list = ['gems','generosity','generous','generously','genial', 'racism','hurt','nuke','gloomy','facebook']

    # eg : items_count = 1000, fp_prob = 0.01, hash_cnt=3,
    bloom_filter = manager.BloomFilter(items_count, fp_rpob, hash_cnt) 

    lock= mp.Lock() 

    shuffle(word_list)
    processes = []
    for i in range(num_of_process):
        mode = randrange(3)
        word_index = randrange(len(word_list));
        if mode == 0 :
            processes.append(mp.Process(target = write_test, args=(f'write_{i}', bloom_filter, word_list[word_index], lock)))
        else:
            processes.append(mp.Process(target = read_test, args=(f'read_{i} ', bloom_filter, word_list[word_index], lock)));

    for process in processes:
        process.start()
    for process in processes:
        process.join()        

    manager.shutdown()
    manager.join()

    
def read_write_test(word, items_count, fp_rpob, hash_cnt):
    """
    test single write and read test
    """
    print(f'===============================================================================================================')
    print(f'single write and read test')
    print(f'===============================================================================================================')   
    # eg : items_count = 1000, fp_prob = 0.01, hash_cnt=3,
    bloom_filter = BloomFilter(items_count, fp_rpob, hash_cnt) 
    bloom_filter.add(word)
    print (f'add data: {word}')
    print (f'look up data: {word} = {bloom_filter.may_match(word)}')

if __name__ == '__main__':
    # single read write test
    # eg : testword ="wordtest", items_count = 1000, fp_prob = 0.01, hash_cnt=3,
    read_write_test("wordtest", 1000, 0.01, 3)

    # random read write test with process management
    # eg number of process = 8, items_count = 1000, fp_prob = 0.01, hash_cnt=3,
    read_write_multiprocess_test(8, 1000, 0.01, 3)

    # 10 million data 
    items_count = 10000000
    # false positive list
    fp_list = [0.1, 0.01, 0.001, 0.0001]
    # hash cnt list
    hash_cnt_list = [1, 2, 3, 4]

    #evaluate hash Count and ratio by providng  items_count and false positive probability
    evaluate_hash_count_and_ratio(items_count, fp_list)

    # evaluate array size by given desired false positive probability and given k hash function constraints
    evaluate_fp_rate(items_count, fp_list, hash_cnt_list)

    # evaluate false positive rate by given desired false positive probability and given k hash function constraints
    # wordlist.txt IS REQUIRED at the folder for this test 
    # eg: filename = "wordlist.txt", fp_prob = 0.01, hash_cnt=3, iteration=30, test_size=10000
    test_real_fp_prob("wordlist.txt", 0.01, 3, 30, 10000)
