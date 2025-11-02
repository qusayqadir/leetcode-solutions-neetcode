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

#================#================#================#================#================
class Solution2(object):
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        currSum = 0 
        prefix = {
            0 : 1 
        } 
        
        res = 0 
        # O(n)
        for i in range(len(nums)): 
            currSum += nums[i] 

            if currSum - k in prefix: 
                res += prefix[currSum - k]
            
            prefix[currSum] = prefix.get(currSum, 0) + 1 


        return res 
        


            

