class Solution:
    # Linear Time Solution - O(n)
    def maxArea(self, height: List[int]) -> int:
        n = len(height) 
        l, r = 0, n-1 
        max_water = 0 
        lower_end = height[l]

        while l < r: 
            # logic cal water
            lower_end = min(height[l], height[r]) 
            max_water = max(max_water, (r-l)*(lower_end)) 

            # logic move pointer

            if height[l] == lower_end: 
                l += 1 
            if height[r] == lower_end: 
                r -= 1 

        return max_water
    
# need to make a change 
            
