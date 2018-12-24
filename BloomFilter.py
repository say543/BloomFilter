import math

# bit array
from bitarray import bitarray 

# hash function
import mmh3 

class BloomFilter(object): 
    """
    Bloom Filter module
    using  Murmur3  as hash function
    """
    def __init__(self, items_count, fp_prob, hash_count = None): 
        """
        Args:
            items_count(int):  number of items expected to be stored in filter 
            fp_prob (float): False Positive probability in decimal, optional argument
            hash_count(int):  number of hash function cnt will be used

        """
        if items_count <= 0:
            raise ValueError("items_count must be bigger than 0")
        if fp_prob <= 0:
            raise ValueError("fp_prob must be bigger than 0")
        if hash_count != None and  hash_count <=0:
            raise ValueError("hash_count must be bigger than 0")

        if hash_count != None:

            # False posible probability in decimal 
            self.fp_prob = fp_prob 

            # OPTION TWO
            self.hash_count = hash_count
            self.size = (int)(self.get_size_by_hash_count_and_fp_prob(items_count, hash_count, fp_prob))

        else: 
            # False posible probability in decimal 
            self.fp_prob = fp_prob 

            #if self.fp_prob == 0:
            #    self.hash_count = (int)(self.get_hash_count_by_array_size_and_element_size(self.size, items_count))
            #else:
            #    self.hash_count = (int) (self.get_hash_count_by_fp_prob(fp_prob))

  
            # OPTION ONE 
            # number of hash functions to use 
            #self.hash_count = (int)(self.get_hash_count_by_array_size_and_element_size(self.size, items_count))
            

            # OPTION TWO
            # number of hash functions to use 
            self.hash_count = (int) (self.get_hash_count_by_fp_prob(fp_prob))

            self.size = (int )( self.get_size(items_count, fp_prob))
            
        # outout initlization information
        print(f'false_positive:{fp_prob} \
            hash_count: {self.hash_count} \
            array_size: {self.size} \
            space(MB): {format(self.size / math.pow(2, 20) / 8, "f")}')
  
        # Bit array of given size 
        self.bit_array = bitarray(self.size) 
        # initialize all bits as 0 
        self.clear_all() 
  
    def add(self, item): 
        """
        Add an item in the filter 
        Args:
            items (string):  an item to insert
        """
        for i in range(self.hash_count): 
  
            # create digest for given item. 
            # i work as seed to mmh3.hash() function 
            # With different seed, digest created is different 
            array_index = mmh3.hash(item,i) % self.size 
  
            # set the bit True in bit_array 
            self.bit_array[array_index] = True
  
    def check(self, item): 
        """
        Check for existence of an item in filter 
        Args:
            items (string):  an item to insert

        """
        for i in range(self.hash_count): 
            array_index = mmh3.hash(item,i) % self.size 
            if self.bit_array[array_index] == False: 
  
                # if any of bit is False then,its not present 
                return False
        return True

    def clear_all(self): 
        """
        clear all items in bloom filter

        """
        self.bit_array.setall(0)
  
    @classmethod
    def get_size(self, items_count, fp_prob): 
        """
        array_size = -(items_count * lg(fp_prob)) / (lg(2)^2) 

        Args:
            items_count(int):  number of items expected to be stored in filter 
            fp_prob (float): False Positive probability in decimal .
        Returns:
            float: Return the size of bit array(m) to used

        """
        array_size = -(items_count * math.log(fp_prob))/(math.log(2)**2) 
        return array_size 
  
    @classmethod
    def get_hash_count_by_array_size_and_element_size(self, array_size, items_count): 
        """

        hash_count = (array_size / items_count) * ln(2) 
  
        fp_prob : float 
            False Positive probability in decimal 

        Args:
            array_size (int): size of bit array  wiil be used
            items_count(int):  number of items expected to be stored in filter 


        Returns:
            float: Return the optimized hash cnt to be used
        """

        hash_count = (array_size/items_count) * math.log(2) 
        return hash_count 

    @classmethod
    def get_hash_count_by_fp_prob(self, fp_prob): 
        """
        hash_count =  (-1) log2(desired probability) 
  
        fp_prob : float 
            False Positive probability in decimal 

        Args:
            fp_prob (float): False Positive probability in decimal .

        Returns:
            float: Return the optimized hash cnt to be used based on fp_prob
        """
        hash_count = (-1) * math.log(fp_prob, 2) 
        return hash_count 

    
    @classmethod
    def get_size_by_hash_count_and_fp_prob(self, items_count, hash_count, fp_prob): 
        """

        array_size =  items_count * 2 * hash_count / (2* fp_prob^(1/hash_count) + fp_prob^(1/hash_count) * fp_prob^(1/hash_count))

        Args:
            items_count(int):  number of items expected to be stored in filter 
            hash_count(int):  number of hash function cnt will be used
            fp_prob (float): False Positive probability in decimal .

        Returns:
            float: return optimized array size to be used based on fp_prob and hash count
        """
        fp_prob_with_power = math.pow(fp_prob, 1/hash_count)
        ratio = 2 * hash_count / (2* fp_prob_with_power + fp_prob_with_power * fp_prob_with_power)
        array_size = ratio * items_count
        return array_size
    




