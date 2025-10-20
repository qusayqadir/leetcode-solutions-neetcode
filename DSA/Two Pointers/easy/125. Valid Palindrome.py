class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        s = s.replace(" ", "")
        fixed_s = ""
        for c in s: 
            if c.isalnum(): 
                fixed_s += c 
        
        fixed_s = fixed_s.lower()
        return fixed_s[::-1] == fixed_s
