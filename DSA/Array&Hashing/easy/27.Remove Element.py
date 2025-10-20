class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """

        k = 0 
        l, r = 0, len(nums) 

        while l < r: 
            if nums[l] == val: 
                nums[l] = nums[r-1] 
                # not a swap operation just a need value that may or may not be the val 
                r -= 1 
            else:
                l += 1 

        return l 

#--------------------------
# SOLN2
# index = 0
# for i in nums: 
#     if i != val: 
#         nums[index] = i 
#         index +=1 

# return index