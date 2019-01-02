Bloom filter module
	required pythom package
		mmh3 : hash function
		bitArray : the array to sotre bloom filter hash record
	notations
		items_count : number of items will be stored in this module
		fp_prob : desired false positve probability
		hash_count : numner has hfunctions
		ratio : number of desired items_count to number of bits to store
		space(MB) : bit array byte size 

	This python design has three files required:
	Bloomfilter.py
		the module for BloomFilter. 

		
		This module is not a thread-safety bloomfilter. in Bloomfilter_test, there is an routine with lock to do multiprocess read/write test and this is thw wrapper behavior to support it
		This module does not support delete operation. To support it, we can extend it by using  count bloom filter.
		This module supports configuration through two ways
			Provide items_count, fp_prob
			Provide items_count, fp_prob and hash_count (this option is to constraint what number of hash functions being used)

		Another option to provide  items_count and ratio for configuration is not supported. this 

		Future items can be suppported in the future for scalability is
			reduce number of hash functions being used.
			Another option to provide items_count and ratio for configuration.  

	Bloomfilter_test.py
		five routines
		===============================================================================================================
		single write and read test
		===============================================================================================================
			this routine performs a single write then read test given a configuration for bloom filter module

		===============================================================================================================
		test read write  random multithread test
		===============================================================================================================
			this routine serves as wrapper with lock to perfrom multiprocess read and write 
			in python it has global lock for multithread so using multiprocess here as demonstration
		====================================================================================
		evaluate hash Count and items_count / array size ratio
		====================================================================================
			this routine performs configuration evaluation to verify bloom filter configuration
			becasue of applying probability model, there are two ways to calculate optimized number of hash functions by providing items_count and fp_prob
			it outputs result by
			hash_count: 3.321928094887362              ratio: 4.79e+00
			hash_countByProb: 3.321928094887362              ratio: 4.79e+00

		===============================================================================================================
		evaluate false positive probailitiy by given desgired false positive probability and given k hash function constraints
		===============================================================================================================
			this rotuine perofrms configuration testing.
			the purpose of it is to tell by given different fp_prob , hash_count and items_count how much space(MB) is needed for bloom filter
			this can be a guideline for users to decide what kind of configuration is better with respect to space concern 

		===============================================================================================================
		test false positive probability by given desgired false positive probability and given k hash function constraints 
		===============================================================================================================
			this routine will use wordlist.txt.
			it randomly add new element or test element might be existed or not and calulate false positive probability
			this is to check if read false positive probability constrainted by desired false positive probability 
			it will run many iterations(default is 30).
			false_positive:0.01             hash_count: 3             array_size: 4259949             space(MB): 0.507825
			word_list size: 677763
			iteration: 30
			expected test size: 10000
			test false positive rate:             0.250500
			test false positive rate:             0.245600
			.....
	wordlist.txt
		this is word list file for testing
		it has one word per line
		