class Solution(object):
    def twoSum(self, nums, target):

        for i in range(len(nums)): 
            if target - nums[i] in nums and nums.index(target - nums[i]) != i: 
                return [i, nums.index(target - nums[i])]

#------------- 
# def twoSum(self, nums, target): 
    
#     map = {} 
    
#     for i in range(0, len(nums)): 
#         if target - nums[i] in map: 
#             return [i, map[target - nums[i]]] 
#         else: 
#             map[nums[i]] = i 