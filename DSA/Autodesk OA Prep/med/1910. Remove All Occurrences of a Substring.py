class Solution:
    def removeOccurrences(self, s: str, part: str) -> str:
        #stack appraoch 
        partlen = len(part)
        lastchar = part[-1] 
        stack = [] 

        for char in s: 
            stack.append(char)
            if char == lastchar and len(stack) >= partlen: 
                if ''.join(stack[-partlen:]) == part: 
                    for _ in range(partlen): 
                        stack.pop() 

        return ''.join(stack) 
