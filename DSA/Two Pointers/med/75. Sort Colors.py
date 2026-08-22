class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums) 
        l, r = 0, n-1
        i = 0
        while i <= r: 
            # if i sees a zero, switch it with l, and now u know that on the left of l there is a 0 
            if nums[i] == 0:
                nums[l], nums[i] = nums[i], nums[l] 
                l += 1 
                i += 1 

            # if there is a 2, then replace it with i, and move right inwards, everythihg to the right is not 2, do not replace it i, bc i could be another 2 that it was replaced with and it needs to check if it should be on the inside of r 
            elif nums[i] == 2: 
                nums[i], nums[r] = nums[r], nums[i] 
                r -= 1 
        
            #if you see a 1, then just move on  
            else: 
                i += 1

            print(nums)
            print(i, l, r)