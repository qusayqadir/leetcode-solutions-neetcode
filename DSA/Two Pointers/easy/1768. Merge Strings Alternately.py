#--------------------------------------------NOT TWO POINTER --------------------------------------------
class Solution: 
    def mergeAlternate(self, word1: str, word2: str) -> str: 
        result = "" 
        i, j = 0, 0 
        # could just use one pointer? 
        while i < len(word1) and j < len(word2): 
            result += word1[i] 
            result += word2[j] 
            i += 1 
            j += 1 
        result.append(word1[i:])
        result.append(word2[j:])
        return "".join(result)

#-------------------------------------------- ONE POINTER --------------------------------------------
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        result = [] 
        i = 0
        while i < len(word1) and i < len(word2): 
            result += word1[i]
            result += word2[i]
            i += 1 
        result.append(word1[i:])
        result.append(word2[i:])
        return "".join(result)
        
#--------------------------------------------NOT TWO POINTER --------------------------------------------
# This Python class contains a method that merges two input strings alternately.
class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        merged_word = ""

        for i in range(0, len(word1) + 1):
            if i == len(word1): 
                merged_word += word2[i:]
                break
            elif i == len(word2): 
                merged_word += word1[i:]
                break
        
            merged_word += word1[i] 
            merged_word += word2[i]


        return merged_word
            

        
