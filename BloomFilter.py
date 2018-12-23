import math


# bit array
from bitarray import bitarray 

# hash function

import mmh3 



class BloomFilter(object): 
  
    ''' 
    Class for Bloom filter, using murmur3 hash function 
    '''
  
    def __init__(self, items_count, fp_prob): 
        ''' 
        items_count : int 
            Number of items expected to be stored in bloom filter 
        fp_prob : float 
            False Positive probability in decimal 
        '''
        # False posible probability in decimal 
        self.fp_prob = fp_prob 
  

        # OPTION ONE
        ''' 
        # Size of bit array to use 
        self.size = self.get_size(items_count,fp_prob) 
  
        # number of hash functions to use 
        self.hash_count = self.get_hash_count(self.size, items_count)
        '''

        # OPTION TWO
        self.hash_count = self.get_hash_count_by_prob(fp_prob)
        self.size = self.get_size(items_count,fp_prob)

        print(f'Shape hash_count: {self.get_hash_count(self.size, items_count)}')
        print(f'Shape hash_countByProb: {self.get_hash_count_by_prob(fp_prob)}') 
  
        # Bit array of given size 
        self.bit_array = bitarray(self.size) 
  
        # initialize all bits as 0 
        self.bit_array.setall(0) 
  
    def add(self, item): 
        ''' 
        Add an item in the filter 
        '''
        digests = [] 
        for i in range(self.hash_count): 
  
            # create digest for given item. 
            # i work as seed to mmh3.hash() function 
            # With different seed, digest created is different 
            digest = mmh3.hash(item,i) % self.size 
            digests.append(digest) 
  
            # set the bit True in bit_array 
            self.bit_array[digest] = True
  
    def check(self, item): 
        ''' 
        Check for existence of an item in filter 
        '''
        for i in range(self.hash_count): 
            digest = mmh3.hash(item,i) % self.size 
            if self.bit_array[digest] == False: 
  
                # if any of bit is False then,its not present 
                # in filter 
                # else there is probability that it exist 
                return False
        return True
  
    @classmethod
    def get_size(self,n,p): 
        ''' 
        Return the size of bit array(m) to used using 
        following formula 
        m = -(n * lg(p)) / (lg(2)^2) 
        n : int 
            number of items expected to be stored in filter 
        p : float 
            False Positive probability in decimal 
        '''
        m = -(n * math.log(p))/(math.log(2)**2) 
        return int(m) 
  
    @classmethod
    def get_hash_count(self, m, n): 
        ''' 
        Return the hash function(k) to be used using 
        following formula 
        k = (m/n) * lg(2) 
  
        m : int 
            size of bit array 
        n : int 
            number of items expected to be stored in filter 
        '''
        k = (m/n) * math.log(2) 
        return int(k) 

    @classmethod
    def get_hash_count_by_prob(self, fp_prob): 
        ''' 
        Return the optimized hash function(k) to be used based on fp_prob
        k = (1/ fp_prob )/ lg(2) 
  
        fp_prob : float 
            False Positive probability in decimal 
        '''
        k = math.log( 1/fp_prob) / math.log(2) 
        return int(k) 





