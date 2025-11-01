class Solution(object):
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        # attempt to solve using the brute force solution 
        currSum = 0 
        numSA = 0 
        for i in range(0,len(nums)): 
            currSum = 0
            for j in range(i, len(nums)): 
                currSum += nums[j] 
                if currSum == k: 
                    numSA += 1 


        
        return numSA