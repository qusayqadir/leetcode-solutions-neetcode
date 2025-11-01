class Solution(object):
    def lengthOfLongestSubstring(self, s: str) -> int:
        """
        :type s: str
        :rtype: int
        """
        l, r = 0,0 
        longestSubstring = 0 
        seen = set() 
        while r < len(s): 
            if s[r] not in seen:
                seen.add(s[r]) 
                longestSubstring = max(longestSubstring, (r-l)+1) 
                r += 1
            else: 
                while s[r] in seen: 
                    seen.remove(s[l])
                    l+=1
        return longestSubstring
