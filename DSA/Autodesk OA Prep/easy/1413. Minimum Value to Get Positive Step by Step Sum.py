class Solution:
    def minStartValue(self, nums: list[int]) -> int:
        foundMin = False 
        startVal = 1
        while not foundMin: 
            currTotal = startVal 
            for num in nums: 
                currTotal += num 
                if currTotal < 1: 
                    startVal += 1 
                    break
            if currTotal >= 1: 
                foundMin = True 

        return startVal 

        
