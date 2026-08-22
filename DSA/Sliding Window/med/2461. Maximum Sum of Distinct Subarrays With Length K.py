class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:

        l, r = 0,0 
        seen = set()
        maxSum, tempSum = 0, 0

        while r <= len(nums)-1:     

            tempSum += nums[r] 
            if nums[r] in seen: 
                while nums[r] in seen: 
                    seen.remove(nums[l])
                    tempSum -= nums[l]
                    l += 1
            seen.add(nums[r])

            if r - l + 1 == k:
                maxSum=max(tempSum, maxSum)
                tempSum -= nums[l]
                seen.remove(nums[l])
                l+=1 

            
            r+=1 

        return maxSum

