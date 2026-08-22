import math 
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        
        def validK(mid:int) -> bool: 
            time = 0 
            for pile in piles: 
                time += ceil(pile/mid)
            
            return True if time <= h else False 


        piles.sort()
        k = piles[-1] 
        l, r = 1, k 

        while l < r: 
            mid = (l+r) // 2 

            if validK(mid): 
                r = mid 
            else: 
                l = mid + 1 

        return l 