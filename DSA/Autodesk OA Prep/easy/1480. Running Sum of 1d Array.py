class Solution:
    def runningSum(self, nums: list[int]) -> list[int]:
        result = []
        total = 0
        for i in range(len(nums)): 
            total += nums[i]
            result.append(total)
        
        return result
