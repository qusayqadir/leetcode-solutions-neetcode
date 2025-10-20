class Solution(object):
    def search(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        l, r = 0, len(nums) - 1 
        m = (l + r) // 2 

        while l <= r: 
            if target == nums[m]:
                return m 
            elif target > nums[m]: 
                l = m + 1 
            elif target < nums[m]: 
                r = m - 1 

            m = (l + r) // 2     
            
        return -1 
