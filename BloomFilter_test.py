

import math

from BloomFilter import BloomFilter 

from random import shuffle 

"""
class BloomFilterThread(threading.Thread):
	 def __init__(self, bl`):
"""

def evaluate_error_rate(word_present, word_absent, bloom_filter, test_size = 10000):
	for item in word_present:
		bloom_filter.add(item)
  
	# random shuffle
	shuffle(word_present) 
	shuffle(word_absent) 

	#test_words = word_present[:(int)(len(word_present)/2)] + word_absent[:(int)(len(word_absent)/2)]

	test_words = word_present[:test_size] + word_absent[:test_size]

	fp_cnt = 0
	total_cn = test_size *2

	for word in test_words:
		if bloom_filter.check(word):
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
	print(f'evaluate false positive rate by given desgired false positive probability and given k hash function constraints')
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

if __name__ == '__main__':


	# 10 million data 
	items_count = 10000000
	# false positive list
	fp_list = [0.1, 0.01, 0.001, 0.0001]
	# hash cnt list
	hash_cnt_list = [1, 2, 3, 4]

	#evaluate hash Count and array size by given desgired false positive probability only
	evaluate_hash_Count_and_Array_size(items_count, fp_list)

	# evaluate array size by given desgired false positive probability and given k hash function constraints
	evaluate_fp_rate(items_count, fp_list, hash_cnt_list)

	"""
	# evaluate false positive rate by given desgired false positive probability and given k hash function constraints
	"""
	"""
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



	word_present_cnt = (int)(len(word_list)/2)
	word_absent_cnt = (int)(len(word_list)/2)

	word_present = word_list[:word_present_cnt]
	word_absent = word_list[word_present_cnt:]

	items_count = word_present_cnt # number of items being insert
	#fp_prob = 0.01 #false positive probability
	fp_prob = 0.00 #false positive probability
	hash_cnt = 3 
	iteration = 30
	bloom_filter = BloomFilter(items_count, fp_prob, hash_cnt) 

	'''
	iteration = 30
	for iter in range(iteration):
		print (f'flase positive rate: \
			{format(evaluate_error_rate(word_present_cnt, word_absent_cnt, word_list, bloom_filter), "f")}')
	'''
	iteration = 30
	for iter in range(iteration):
		print (f'flase positive rate: \
			{format(evaluate_error_rate(word_present, word_absent, bloom_filter), "f")}')
	"""
