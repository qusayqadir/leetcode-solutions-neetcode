class Solution(object):
    def getConcatenation(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        ans = [0] * 2*len(nums) 
        n = len(nums)
        for i in range (0, n): 
            ans[i] = nums[i] 
            ans[i + n] = nums[i]

        return ans

        # return nums*2 
        # return (nums+nums)


        