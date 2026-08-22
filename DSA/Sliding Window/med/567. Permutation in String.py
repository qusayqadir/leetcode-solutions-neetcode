from collections import Counter
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        
        s1map = Counter(s1)
        #2
        n = len(s1)
        #8
        m = len(s2)  
        s2map = defaultdict(int)
        l, r = 0, 0 

        while r < m:
            s2map[s2[r]] += 1 
            if r - l + 1 == n: 
                if s1map==s2map: 
                    return True 
                else: 
                    s2map[s2[l]] -= 1 
                    if s2map[s2[l]] == 0: 
                        del s2map[s2[l]]
                    l += 1
            
            r += 1 
            
        
        return False 