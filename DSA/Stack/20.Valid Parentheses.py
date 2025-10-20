class Solution:
    def isValid(self, s: str) -> bool:
        closeParent = [')', '}', ']'] 
        validParentMap = { ")" : "(",  "}" : "{", "]" : "["}

        stack = [] 
        for p in s: 
            if p in closeParent and len(stack) > 0: 
                openParent = stack.pop()
                if validParentMap[p] != openParent:
                    return False 
            else: 
                stack.append(p)
                
        #edge case that the stack has open parentheses that don't have matching closing parentheses
        if stack:
            return False 
        return True 
