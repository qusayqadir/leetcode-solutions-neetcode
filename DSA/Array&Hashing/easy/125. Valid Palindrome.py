class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """

        s2 = ""
        for c in s: 
            if c.isalnum(): 
                s2 += c 
        s2 = s2.lower() 
        s2.replace(" ", "")
    
        return s2 == s2[::-1]
