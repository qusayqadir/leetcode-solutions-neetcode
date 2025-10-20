class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        
        mapping_s = {} 
        mapping_t = {} 
        if len(s) != len(t): 
            return False 

        for letter in s: 
            mapping_s[letter] = mapping_s.get(letter, 0 ) + 1 
        for letter in t: 
            mapping_t[letter] = mapping_t.get(letter, 0) + 1

        for key in mapping_s.keys(): 
            if mapping_t.get(key) != mapping_s.get(key):
                return False 
        
        return True 

# ------------------------------------------------------------------------------
#SOLN


# def isAnagram(s: str, t:str):
#     s = sorted(set(s))
#     s_count = []
#     t = sorted(set(t))
#     t_count = [] 

#     for i in s: 
#         s_count.append(s.count(i)) 

#     for j in t: 
#         t_count.append(t.count(j)) 

#     if s == t and s_count == t_count: 
#         return True 
#     return False