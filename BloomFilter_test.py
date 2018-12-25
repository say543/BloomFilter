

import math
import time

import threading

from BloomFilter import BloomFilter 

from random import shuffle 

import multiprocessing as mp
from multiprocessing.managers import BaseManager


class MyManager(BaseManager):
    pass
MyManager.register('BloomFilter', BloomFilter)

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

    fp_cnt = 0
    total_cn = test_size *2

    for word in test_words:
        if bloom_filter.may_match(word):
            if word in word_absent:
                #print (f'false positive') 
                fp_cnt = fp_cnt + 1

    return  fp_cnt / total_cn

def evaluate_hash_Count_and_Array_size(items_count, fp_list):
    """
     evaluate hash Count and array size by given desgired false positive probability only
    """
    print(f'====================================================================================')
    print(f'evaluate hash Count and array size by given desgired false positive probability only')
    print(f'====================================================================================')

    for fp_prob in fp_list:
        size = BloomFilter.get_size(items_count,fp_prob)
        ratio = size / items_count
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

            # originla format
            #print(f'false_positive:{fp_prob} \t hash_count: {hash_cnt}\t ratio: {ratio}')

            print(f'false_positive:{fp_prob} \
                hash_count: {hash_cnt} \
                ratio: {format(ratio, ".2e")} \
                space(MB): {format(size / math.pow(2, 20) / 8, "f")}')

def test_real_fp_prob(filename, fp_prob=0.01, hash_cnt=3, iteration=30, test_size=10000):
    """
    # test false positive probability by given desgired false positive probability and given k hash function constraints
    """
    word_list = []
    int_file = None
    try:
        # use ISO for weird character
        int_file = open(filename, "r", encoding = "ISO-8859-1")
        while True:
            line = int_file.readline()
            if not line:
                break
            word_list.append(line)
    except ValueError as excep:
        print(f'input argument in valid:{excep}')
    except Exception:
        print (f'unknown exception, something wrong')
    finally:
        if int_file is not None:
            int_file.close()


    print(f'===============================================================================================================')
    print(f'test false positive probability by given desgired false positive probability and given k hash function constraints')
    print(f'===============================================================================================================')
    if test_size <= 1:
        raise ValueError("test_size must be at least 2")


    word_present_cnt = (int)(len(word_list)/2)
    word_absent_cnt = (int)(len(word_list)/2)

    word_present = word_list[:word_present_cnt]
    word_absent = word_list[word_present_cnt:]

    items_count = word_present_cnt # number of items being insert

    bloom_filter = BloomFilter(items_count, fp_prob, hash_cnt) 
    print(f'word_list size: {len(word_list)}')
    print(f'iteration: {iteration}')
    print(f'expected test size: {min(test_size, len(word_list))}')


    for iter in range(iteration):
        print (f'flase positive rate: \
            {format(evaluate_error_rate(word_present, word_absent, bloom_filter, min(test_size, len(word_list))), "f")}')


''''
class Producer(threading.Thread):
    def __init__(self, name, data):
        threading.Thread.__init__(self, name, bloom_filter)
        self.data = data
        self.bloom_filter = bloom_filter

    def run(self):
        bloom_filter.add(data)
        print (f'thread {name} add data:{data}')

class Consumer(threading.Thread):
    def __init__(self,name,queue):
        threading.Thread.__init__(self, name, bloom_filter)
        self.data = data
        self.bloom_filter = bloom_filter
    def run(self):
        res = bloom_filter.may_match(data)
        print (f'thread {name} look up data:{data} = {res}')
'''


def write_test(name, bloom_filter, data, lock):
    try:
        lock.acquire() 
        bloom_filter.add(data)
        print (f'{name} add data:{data}')
        print (f'Wlook up data:{data} = {bloom_filter.may_match(data)}')

    except Exception as e:
        raise
    finally:
        lock.release() 

def read_test(name, bloom_filter, data, lock):
    try:
        lock.acquire() 
        res = bloom_filter.may_match(data)
        print (f'{name} look up data:{data} = {res}')
    except Exception as e:
        raise
    finally:
        lock.release() 

def read_write_multithread_test(word):
    """
    test bloom filter multi thread testing
    """


    print(f'===============================================================================================================')
    print(f'read write test')
    print(f'===============================================================================================================')
    
    manager = MyManager()
    manager.start()


    # eg : items_count = 1000, fp_prob = 0.01, hash_cnt=3,
    bloom_filter = manager.BloomFilter(1000, 0.01, 2) 

    lock= mp.Lock() 


    t1 = mp.Process(target = write_test, args=("write", bloom_filter, word, lock))
    t2 = mp.Process(target = read_test, args=("read", bloom_filter, word, lock));

    #t1.start()
    t2.start()
    #t1.join()
    t2.join()

    
def read_write_test(word):
    # eg : items_count = 1000, fp_prob = 0.01, hash_cnt=3,
    bloom_filter = BloomFilter(1000, 0.01, 2) 
    bloom_filter.add(word)
    print (f'look up data:{word} = {bloom_filter.may_match(word)}')


if __name__ == '__main__':


    # single read write test
    #read_write_test("wordtest")

    # 10 million data 
    items_count = 10000000
    # false positive list
    fp_list = [0.1, 0.01, 0.001, 0.0001]
    # hash cnt list
    hash_cnt_list = [1, 2, 3, 4]

    """
    #evaluate hash Count and array size by given desgired false positive probability only
    evaluate_hash_Count_and_Array_size(items_count, fp_list)

    # evaluate array size by given desgired false positive probability and given k hash function constraints
    evaluate_fp_rate(items_count, fp_list, hash_cnt_list)

    # evaluate false positive rate by given desgired false positive probability and given k hash function constraints
    # eg: fp_prob = 0.01, hash_cnt=3, iteration=30, test_size=10000
    test_real_fp_prob("wordlist.txt", 0.01, 3, 30, 10000)
    """

    read_write_multithread_test("wordtest")