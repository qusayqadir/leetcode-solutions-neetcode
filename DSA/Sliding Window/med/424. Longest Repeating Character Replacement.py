from collections import defaultdict
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        
        #sliding window approach 
        #hashmap to keep the count of how many i have seen
        seen = defaultdict(int)
        l, r = 0, 0 
        maxlen = maxfreq = 0 
        while r <= len(s)-1: 
            print(l,r)
            print(maxlen)
            seen[s[r]] += 1    
            maxfreq = max(maxfreq, seen[s[r]])
            while r-l+1 - maxfreq > k: 
                seen[s[l]] -= 1 
                l+=1 
            maxlen = max(maxlen, r-l+1)
            r+=1 
        return maxlen 
            








