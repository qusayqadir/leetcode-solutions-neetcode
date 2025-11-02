class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        res = [] 
        l = 1 
        # O(n^2)? < O(n^3)
        # this works for continous arrays not seperate 
        while l < len(nums) - 1: 
            curSum = nums[l-1] + nums[l] 
            r = l + 1 
            while r < len(nums): 
                if nums[r]  == -1 * curSum: 
                    res.append([nums[l-1], nums[l], nums[r]])
                
                r += 1 

            l += 1 
        return res 

#======INCORRECT ^^^ 
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        res = [] 
        nums.sort()

        for i in range(len(nums)): 
            if i > 0 and nums[i] == nums[i-1]:
                continue

            target = -(nums[i]) 
            l, r = i+1, len(nums)-1

            while l < r: 
                if nums[l] + nums[r] == target: 
                    res.append([nums[i], nums[l], nums[r]])
                    while l < r and nums[l] == nums[l+1]:
                        l += 1
                    while l < r and nums[r] == nums[r-1]: 
                        r -= 1 
                    r -= 1 
                    l += 1 
                    
                elif nums[l] + nums[r] > target: 
                    r -= 1 
                elif nums[l] + nums[r] <= target: 
                    l += 1 
        
        return res 



