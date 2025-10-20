class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums) 
        nums_map = {} 
        for num in nums: 
            nums_map[num] = nums_map.get(num, 0) + 1 

        for key in nums_map.keys(): 
            if nums_map.get(key) > (n/2):
                return key
        

# -----------------------------
# SOLN2:

#     nums.sort() 
#     n = len(nums) 
#     return nums[n//2] 