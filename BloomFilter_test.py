

import math

from BloomFilter import BloomFilter 

from random import shuffle 

def evaluate_error_rate(word_present, word_absent, bloom_filter):
	for item in word_present:
		bloom_filter.add(item)
  
	# random shuffle
	shuffle(word_present) 
	shuffle(word_absent) 

	#test_words = word_present[:(int)(len(word_present)/2)] + word_absent[:(int)(len(word_absent)/2)]

	test_words = word_present[:10000] + word_absent[:10000]

	fp_cnt = 0
	total_cn = len(test_words)

	for word in test_words:
		if bloom_filter.check(word):
			if word in word_absent:
				print (f'false positive') 
				fp_cnt = fp_cnt + 1

	return  fp_cnt / total_cn


if __name__ == '__main__':
	#=======================
	# evaluate hash Count and array size by given desgired false positive probability only
	#=======================
	"""
	# 10 million data 
	items_count = 10000000
	fp_list = [0.1, 0.01, 0.001, 0.0001]
	for fp_prob in fp_list:
		size = BloomFilter.get_size(items_count,fp_prob)
		ratio = size / items_count
		# two options for calculation
		print(f'hash_count: {BloomFilter.get_hash_count_by_array_size_and_element_size(size, items_count)} \
	 		ratio: {format(ratio, ".2e")}')
		print(f'hash_countByProb: {BloomFilter.get_hash_count_by_fp_prob(fp_prob)} \
	 		ratio: {format(ratio, ".2e")}') 
	"""


	#=======================
	# evaluate array size by given desgired false positive probability and given k hash function constraints
	#=======================
	"""
	# 10 million data 
	items_count = 10000000
	fp_list = [0.1, 0.01, 0.001, 0.0001]
	hash_cnt_list = [1, 2, 3, 4]
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
	"""




	#=======================
	# evaluate false positive rate by given desgired false positive probability and given k hash function constraints
	#=======================
	items_count = 10000000 #no of items to add 
	fp_prob = 0.01 #false positive probability

	hash_cnt = 3 

	iteration = 30
 
	bloom_filter = BloomFilter(items_count, fp_prob, hash_cnt)  

	word_list = []
	int_file = None
	try:
		# use ISO for weird character
		int_file = open("wordlist.txt", "r", encoding = "ISO-8859-1")
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

	print(f'word_list size :{len(word_list)}')

	middle_index= (int)(len(word_list)/2)

	word_present = word_list[: middle_index]
	word_absent = word_list[middle_index:]

	for iter in range(iteration):
		print (f'flase positive rate: \
			{format(evaluate_error_rate(word_present, word_absent, bloom_filter), "f")}')


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
  


'''
