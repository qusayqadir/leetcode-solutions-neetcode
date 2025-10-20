class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """

        prefix = ""

        #outer loop 
        for i in range(len(strs[0])):
            for j in range(len(strs)):
                if i >= len(strs[j]):
                    return prefix 
                elif strs[j][i] != strs[0][i]: 
                    return prefix 
            prefix += strs[0][i]

        return prefix 
        # O(n * m ) 
        # where n is the length of the first string str[0] and m is the number of elements in the len(str)
        

# -----------------------
# SOLN2: 
#     class Solution(object):
#     def longestCommonPrefix(self, strs):
#         """
#         :type strs: List[str]
#         :rtype: str
#             """
#         prefix = ""
#         for i in range (len(strs[0])): 
#             for s in strs: // THIS WAS THE KEY TO THE SOLN 
#                 if i == len(s) or s[i] != s[0][i]: 
#                     return prefix 
            
#             prefix += strs[0][i]