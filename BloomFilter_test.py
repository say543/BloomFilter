



from BloomFilter import BloomFilter 

from random import shuffle 


#=======================
# test by given desgired false positive probability only
#=======================
'''
items_count = 10000000
fp_list = [0.1, 0.01, 0.001, 0.0001]
for fp_prob in fp_list:

	size = BloomFilter.get_size(items_count,fp_prob)

	ratio = size / items_count

	# two options for calculation
	print(f'hash_count: {BloomFilter.get_hash_count_by_array_size_and_element_size(size, items_count)}\t ratio: {ratio}')
	print(f'hash_countByProb: {BloomFilter.get_hash_count_by_fp_prob(fp_prob)}\t ratio: {ratio}') 
'''

#=======================
# test by given desgired false positive probability and given k hash function constraints
#=======================
items_count = 10000000
fp_list = [0.1, 0.01, 0.001, 0.0001]
hash_cnt_list = [1, 2, 3, 4]
for fp_prob in fp_list:
	for hash_cnt in hash_cnt_list:

		size = BloomFilter.get_size_by_fp_prob_and_hash_count(hash_cnt, fp_prob)

		ratio = size / items_count

		# originla format
		print(f'false_positive:{fp_prob} \t hash_count: {hash_cnt}\t ratio: {ratio}')
		
		# beauti format
		print(f'false_positive:{fp_prob} \t hash_count: {hash_cnt}\t ratio: {format(ratio, "2.6f")}')




'''
n = 20 #no of items to add 
p = 0.05 #false positive probability 
  
bloomf = BloomFilter(n,p) 
'''

'''
print("Size of bit array:{}".format(bloomf.size)) 
print("False positive Probability:{}".format(bloomf.fp_prob)) 
print("Number of hash functions:{}".format(bloomf.hash_count)) 
'''

'''
# words to be added 
word_present = ['abound','abounds','abundance','abundant','accessable', 
                'bloom','blossom','bolster','bonny','bonus','bonuses', 
                'coherent','cohesive','colorful','comely','comfort', 
                'gems','generosity','generous','generously','genial'] 
  
# word not added 
word_absent = ['bluff','cheater','hate','war','humanity', 
               'racism','hurt','nuke','gloomy','facebook', 
               'geeksforgeeks','twitter'] 
  
for item in word_present: 
    bloomf.add(item) 
  
shuffle(word_present) 
shuffle(word_absent) 
  
test_words = word_present[:10] + word_absent 
shuffle(test_words) 
for word in test_words: 
    if bloomf.check(word): 
        if word in word_absent: 
            print("'{}' is a false positive!".format(word)) 
        else: 
            print("'{}' is probably present!".format(word)) 
    else: 
        print("'{}' is definitely not present!".format(word)) 

'''